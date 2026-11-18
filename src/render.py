import ships

def displayMessage(message:str) -> None:
	print(f"\n--- {message} ---\n")

def displayShipSetup(cmanifest:list[ships.Ship]) -> None:
	# Initialize a 10x10 grid with water (Rows A-J, Cols 1-10)
	grid = [["~" for _ in range(10)] for _ in range(10)]
	
	for ship in cmanifest:
		if ship.valid and ship.inPlay:
			# Plot true coordinates of the ship
			for pt in ship.trueCoords():
				if 1 <= pt.x <= 10 and 1 <= pt.y <= 10:
					# x corresponds to columns (horizontal 1-10), y corresponds to rows (vertical A-J)
					grid[pt.y - 1][pt.x - 1] = "S"
					
	# Print horizontal numbers header (1 to 10)
	print("   " + " ".join(str(i) for i in range(1, 11)))
	for i, row in enumerate(grid):
		row_label = chr(ord('A') + i)
		print(f"{row_label}  " + " ".join(row))

def displayHitmap(content:list[ships.Hit]) -> None: #Map should use H M .
	# Initialize a 10x10 grid with unexplored dots (Rows A-J, Cols 1-10)
	grid = [["." for _ in range(10)] for _ in range(10)]
	
	for h in content:
		if 1 <= h.location.x <= 10 and 1 <= h.location.y <= 10:
			if h.hit:
				grid[h.location.y - 1][h.location.x - 1] = "H"
			else:
				grid[h.location.y - 1][h.location.x - 1] = "M"
				
	# Print horizontal numbers header (1 to 10)
	print("   " + " ".join(str(i) for i in range(1, 11)))
	for i, row in enumerate(grid):
		row_label = chr(ord('A') + i)
		print(f"{row_label}  " + " ".join(row))
