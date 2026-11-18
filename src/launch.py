import game
import gamemp
def _menu() -> int:
	while 1:
		print("1) Play Battleship")
		print("2) Play Battleship (Experimental)")
		print("0) Quit")
		line = input(">> ")
		try:
			nline:int = int(line)
			if not 0 <= nline <= 2: continue
			return nline
		except ValueError: continue

if __name__ == "__main__":
	try:
		match _menu():
			case 1: game.main()
			case 2: gamemp.main()
			case 0: exit(0)
			case _: exit(1)
	except KeyboardInterrupt:
		exit(0)
	except:
		exit(1)