import core

def main():
	core.render.displayMessage("Welcome to Battleship!")

	player:core.Actor = core.PlayerTerminal("Player 1")
	enemy:core.Actor = core.SimpleNPC()
	
	# Setup Phase
	fleet_manifest:list[core.ships.ShipData] = [core.ships.ShipData(core.ships.shipLength[key],key) for key in core.ships.shipLength.keys()]
	
	for s_data in fleet_manifest:
		# Create dummy ships to pass into placeShip (Matzu's methods overwrite position/direction based on input/randomness)
		dummy_ship:core.ships.Ship = core.ships.Ship(core.ships.Point(1,1), s_data, core.ships.Point(1,0))
		player.placeShip(dummy_ship)
		dummy_ship = core.ships.Ship(core.ships.Point(1,1), s_data, core.ships.Point(1,0))
		enemy.placeShip(dummy_ship)
		
	core.render.displayMessage("Setup Complete. Commencing Battle!")
	
	# Game Loop
	while True:
		# Player Turn
		core.render.displayMessage(f"{player.label}'s Turn")
		core.render.displayShipSetup(player.userShips)
		player.userHits.append(enemy.opponentHit(player.pickHit()))
		
		# Check Win Condition
		if enemy.noActiveShips():
			core.render.displayMessage(f"{player.label} wins!")
			break
			
		# Enemy Turn
		core.render.displayMessage(f"{enemy.label}'s Turn")
		enemy.userHits.append(player.opponentHit(enemy.pickHit()))
		
		# Check Loss Condition
		if player.noActiveShips():
			core.render.displayMessage(f"{enemy.label} wins!")
			break

if __name__ == "__main__":
	main()
