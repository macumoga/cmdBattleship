import core

def main():

	nhuman:int = 1
	nrobot:int = 1

	while 1:
		try:
			nhuman = int(input("How many humans will be playing?: "))
			nrobot = int(input("How many robots are requested?: "))
			break
		except ValueError:
			continue


	core.render.displayMessage("Welcome to Battleship.")

	playerlist:list[core.Actor] = list()
	for _ in range(nhuman): playerlist.append(core.PlayerTerminal(input("HUMAN! Your name: ")))
	for _ in range(nrobot): playerlist.append(core.SimpleNPC())

	for player in playerlist:
		for ship in [core.ships.ShipData(core.ships.shipLength[key],key) for key in core.ships.shipLength.keys()]:
			cand = core.ships.Ship(core.ships.Point(1,1), ship, core.ships.Point(1,0))
			player.placeShip(cand)
		
	core.render.displayMessage("Begin warfare.")

	active:int = -1
	next:int = 0
	
	# Game Loop
	while len(playerlist) > 1:

		active = next % len(playerlist)
		next = (active + 1) % len(playerlist)

		playerlist[active].userHits.append(playerlist[next].opponentHit(playerlist[active].pickHit()))
		if playerlist[next].noActiveShips():
			core.render.displayMessage(f"{playerlist[next].label} is out of play.")
			playerlist.pop(next)

	core.render.displayMessage(f"{playerlist[0].label} wins.")

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt: exit(0)
