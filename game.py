import ships
import render
from random import randint

def parseCoord(raw:str) -> ships.Point | None:
	raw = raw.strip().upper()
	if not raw: return None
	parts = raw.split()
	if len(parts) >= 2:
		col_str, row_str = parts[0], parts[1]
	elif len(raw) >= 2 and raw[0].isalpha():
		col_str, row_str = raw[0], raw[1:]
	else:
		return None
	if len(col_str) != 1 or not col_str.isalpha():
		return None
	try:
		# Letters (A-J) correspond to y, numbers (1-10) correspond to x
		y = ord(col_str) - ord('A') + 1
		x = int(row_str)
	except ValueError:
		return None
	return ships.Point(x, y)

class Actor:

	userShips:list[ships.Ship]
	userHits:list[ships.Hit]
	label:str

	def __init__(self,label:str):
		self.userHits = list()
		self.userShips = list()
		self.label = label
		return

	def pickHit(self) -> ships.Point: raise NotImplemented()

	def placeShip(self,tShip:ships.Ship) -> None: raise NotImplemented()

	def opponentHit(self,attack:ships.Point) -> ships.Hit:
		for i in range(len(self.userShips)):
			pts:list[ships.Point] = self.userShips[i].trueCoords()
			if attack in pts:
				render.displayMessage(f"{self.label}: Your {self.userShips[i].beenHit()} has been hit.")
				if not self.userShips[i].inPlay: render.displayMessage(f"Your {self.userShips[i].info.label} is sunk.")
				return ships.Hit(attack,True)
		render.displayMessage(f"{self.label}: No ship of yours was hit.")
		return ships.Hit(attack,False)

	def noActiveShips(self) -> bool:
		for ship in self.userShips:
			if ship.inPlay: return False
		return True


class PlayerTerminal(Actor):

	def __init__(self,label:str) -> None:
		super().__init__(label)
		return

	def pickHit(self) -> ships.Point:
		rtv:ships.Point | None

		render.displayHitmap(self.userHits)

		while 1:
			rtv = parseCoord(input("y x (A-J 1-10): "))
			if rtv is None: continue
			if rtv.x != ships.clamp(rtv.x,1,10) or rtv.y != ships.clamp(rtv.y,1,10):
				col_label = chr(ord('A') + rtv.x - 1) if 1 <= rtv.x <= 26 else str(rtv.x)
				render.displayMessage(f"Point [{col_label}, {rtv.y}] is not in play.")
				continue
			if ships.Hit(rtv,True) in self.userHits or ships.Hit(rtv,False) in self.userHits:
				col_label = chr(ord('A') + rtv.x - 1)
				render.displayMessage(f"Point [{col_label}, {rtv.y}] was already hit.")
				continue
			break
		
		return rtv

	def placeShip(self,tShip:ships.Ship) -> None:

		render.displayMessage(f"{self.label}: Placing ship {tShip.info.label}.")

		while 1:
			rtv:ships.Point | None = parseCoord(input("y x (A-J 1-10): "))
			if rtv is None: continue

			sdir:ships.Point
			sdat:ships.ShipData = tShip.info
			dir_raw:str = input("dir (n,w,s,e): ").strip().lower()
			if not dir_raw: continue
			argc:str = dir_raw[0]
			match argc:
				case "n": sdir = ships.Point(0,-1)
				case "w": sdir = ships.Point(-1,0)
				case "s": sdir = ships.Point(0,1)
				case "e": sdir = ships.Point(1,0)
				case _: continue

			tShip = ships.Ship(rtv,sdat,sdir)
			if not tShip.valid:
				render.displayMessage("Ship is not of range.")
				continue

			if ships.shipOverlap(tShip,self.userShips):
				render.displayMessage("Ship will collide with another ship.")
				continue

			break
		
		self.userShips.append(tShip)
		return

class SimpleNPC(Actor):

	def __init__(self) -> None:
			super().__init__(f"NPC {id(self)}")
			return
	
	def pickHit(self) -> ships.Point:
		rtv:ships.Point
		while 1:
			rtv = ships.Point(randint(1,10),randint(1,10))
			if ships.Hit(rtv,True) in self.userHits or ships.Hit(rtv,False) in self.userHits: continue
			break
		
		return rtv

	def placeShip(self,tShip:ships.Ship) -> None:

		render.displayMessage(f"{self.label}: Placing ship {tShip.info.label}.")

		while 1:
			rtv:ships.Point = ships.Point(randint(1,10),randint(1,10))
			sdir:ships.Point
			sdat:ships.ShipData = tShip.info
			argn:int = randint(0,3)
			match argn:
				case 0: sdir = ships.Point(0,-1)
				case 1: sdir = ships.Point(-1,0)
				case 2: sdir = ships.Point(0,1)
				case 3: sdir = ships.Point(1,0)
				case _: continue
			tShip = ships.Ship(rtv,sdat,sdir)
			if not tShip.valid: continue
			if ships.shipOverlap(tShip,self.userShips): continue
			break
		
		self.userShips.append(tShip)
		return

def main():
	render.displayMessage("Welcome to Battleship!")

	player = PlayerTerminal("Player 1")
	enemy = SimpleNPC()
	
	# Setup Phase
	fleet_manifest = [
		ships.ShipData(5, "Carrier"),
		ships.ShipData(4, "Battleship"),
		ships.ShipData(3, "Destroyer"),
		ships.ShipData(3, "Submarine"),
		ships.ShipData(2, "Tugboat")
	]
	
	for s_data in fleet_manifest:
		# Create dummy ships to pass into placeShip (Matzu's methods overwrite position/direction based on input/randomness)
		dummy_player_ship = ships.Ship(ships.Point(1,1), s_data, ships.Point(1,0))
		player.placeShip(dummy_player_ship)
		
		dummy_npc_ship = ships.Ship(ships.Point(1,1), s_data, ships.Point(1,0))
		enemy.placeShip(dummy_npc_ship)
		
	render.displayMessage("Setup Complete. Commencing Battle!")
	
	# Game Loop
	while True:
		# Player Turn
		render.displayMessage(f"{player.label}'s Turn")
		render.displayShipSetup(player.userShips)
		
		target = player.pickHit()
		result = enemy.opponentHit(target)
		player.userHits.append(result)
		
		# Check Win Condition
		if enemy.noActiveShips():
			render.displayMessage(f"Congratulations! {player.label} wins!")
			break
			
		# Enemy Turn
		render.displayMessage(f"{enemy.label}'s Turn")
		enemy_target = enemy.pickHit()
		enemy_result = player.opponentHit(enemy_target)
		enemy.userHits.append(enemy_result)
		
		# Check Loss Condition
		if player.noActiveShips():
			render.displayMessage(f"Defeat! {enemy.label} wins!")
			break

if __name__ == "__main__":
	main()
