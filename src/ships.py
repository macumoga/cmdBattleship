from __future__ import annotations

class Point:

	x:int
	y:int

	def __init__(self,x:int,y:int) -> None:
		self.x = x
		self.y = y

	def __repr__(self) -> str:
		return f"({self.x}, {self.y})"

	def __eq__(self,other:object) -> bool:
		if type(other) == Point: return  self.x == other.x and self.y == other.y
		if type(other) == Hit: return  self.x == other.location.x and self.y == other.location.y
		if type(other) == Ship: return self in other.trueCoords()
		return False

class Hit:

	location:Point
	hit:bool

	def __init__(self,loc:Point,hit:bool) -> None:
		self.location = loc
		self.hit = hit

class ShipData:

	length:int
	label:str

	def __init__(self,length:int,label:str) -> None:
		self.length = max(min(length,5),2)
		self.label = label.title()

class Ship:

	pivot:Point
	info:ShipData
	facing:Point
	farpoint:Point
	health:int
	valid:bool = False
	inPlay:bool = True

	def __init__(self,origin:Point,info:ShipData,direction:Point) -> None:
		self.pivot = origin
		self.info = info
		self.facing = normal(direction)
		self.farpoint = Point(self.pivot.x + (self.info.length * self.facing.x),self.pivot.y + (self.info.length * self.facing.y))
		self.health = self.info.length
		self.valid = self.validate()
		self.inPlay = True
		return

	def validate(self) -> bool:
		#Exactly one 0
		if abs(self.facing.x) == abs(self.facing.y): return False
		#Pivot in bounds
		if (self.pivot.x != clamp(self.pivot.x,1,10)): return False
		if (self.pivot.y != clamp(self.pivot.y,1,10)): return False
		#End in bounds
		if (self.farpoint.x != clamp(self.farpoint.x,1,10)): return False
		if (self.farpoint.y != clamp(self.farpoint.y,1,10)): return False

		return True

	def trueCoords(self) -> list[Point]:
		wx:int = self.pivot.x
		wy:int = self.pivot.y
		lp:list[Point] = list()
		for _ in range(self.info.length):
			lp.append(Point(wx,wy))
			wx += self.facing.x
			wy += self.facing.y
		return lp

	def beenHit(self) -> None:
		self.health -= 1
		if self.health < 1: self.inPlay = False
		return

	def __repr__(self) -> str:
		chr:str

		#Did not cooperate with match statements
		if self.facing == Point(0,-1): chr = "North"
		elif self.facing == Point(-1,0): chr = "West"
		elif self.facing == Point(0,1): chr = "South"
		elif self.facing == Point(1,0): chr = "East"
		elif self.facing == Point(0,0): chr = "Up?"
		else: chr = "???"

		return f"{self.info.label} at {self.pivot.x},{self.pivot.y} facing {chr}"


def clamp(n:int,nmin:int=-1,nmax:int=1) -> int: return max(min(n,nmax),nmin)
def normal(pt:Point) -> Point: return Point(clamp(pt.x),clamp(pt.y))

shipLength:dict[str,int] = {
	"Carrier": 5,
	"Battleship": 4,
	"Destroyer": 3,
	"Submarine": 3,
	"Tugboat": 2
}

def shipOverlap(cShip:Ship,lShip:list[Ship]) -> bool:
	cPoints:list[Point] = cShip.trueCoords()
	for rShip in lShip:
		rPoints:list[Point] = rShip.trueCoords()
		for cpt in cPoints:
			if cpt in rPoints: return True
	return False
	
