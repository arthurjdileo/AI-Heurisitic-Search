#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from random import randint
import numpy as np
import queue
import math
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import pygame
import time

class Node:
	def __init__(self, position, parent):
		self.position = position
		self.parent = parent
		self.g = 0 #Distance to start
		self.h = 0 #Distance to goal
		self.f = 0 #total cost
	def __lt__(self, other):
		return self.f < other.f
	def __eq__(self, other):
		if not isinstance(other, Node):
			return NotImplemented
		return self.position == other.position
	def __ne__(self, other):
		return not self.__eq__(other)
	def __hash__(self):
		return hash(self.position)
	def __repr__(self):
		return "%d,%d" % (self.position[0], self.position[1])

class world:
	def __init__(self):
		self.data = np.chararray(shape=(120, 160))
		self.data[:] = '1'
		self.saved = 1
		randomize(self)
		self.start = start
		self.goal = goal
		self.hard_travers = hard_travers
		self.generateTexture()
		self.createHighways()
		self.highwaylist = highwaylist
		self.createBlocked()
		print(self.start, self.data[self.start[0], self.start[1]].decode(), self.goal, self.data[self.goal[0], self.goal[1]].decode())

	def callLoad(self):
		load(self)
		generateMap()

	def rotateSnG(self):
		self.data[self.start[0], self.start[1]] = '1'
		self.data[self.goal[0], self.goal[1]] = '1'

		#Defines start and Goal
		global start
		start = [None, None]
		global goal
		goal = [None, None]

		r1 = randint(0,3)
		#North
		if r1 == 0:
			rows = randint(0,19)
			cols = randint(0,159)
			rowg = randint(99,119)
			colg = randint(0,159)
			start = [rows, cols]
			goal = [rowg, colg]
		#South
		elif r1 == 1:
			rows = randint(99,119)
			cols = randint(0,159)
			rowg = randint(0,19)
			colg = randint(0,159)
			start = [rows, cols]
			goal = [rowg, colg]
		#East
		elif r1 == 2:
			rows = randint(0,119)
			cols = randint(139,159)
			rowg = randint(0,119)
			colg = randint(0,19)
			start = [rows, cols]
			goal = [rowg, colg]
		#West
		elif r1 == 3:
			rows = randint(0,119)
			cols = randint(0,19)
			rowg = randint(0,119)
			colg = randint(139,159)
			start = [rows, cols]
			goal = [rowg, colg]
		
		if self.data[start[0], start[1]] == '0' or self.data[goal[0], goal[1]] == '0' or self.data[start[0], start[1]] == 'a' or self.data[goal[0], goal[1]] == 'a' or self.data[start[0], start[1]] == 'b' or self.data[goal[0], goal[1]] == 'b':
			self.rotateSnG()
		self.setSnG()

	def setSnG(self):
		#assigns the start index
		self.data[start[0],start[1]] = 'S'
		#assigns the goal index
		self.data[goal[0],goal[1]] = 'G'
	
	def rotateSNGHandler(self):
		global start, goal
		self.rotateSnG()
		self.start = start
		self.goal = goal

	def printworld(self, force=False):
		if force:
			with open("world%d.txt" % self.saved, "w+") as f:
				for row in self.data:
					f.write(str(row, 'utf-8'))
					f.write('\n')
			self.saved += 1
			return

		with open(input("Please enter the path to output file: "), 'w') as f:
			for row in self.data:
				f.write(str(row, 'utf-8'))
				f.write('\n')

	def saveCurrentMap(self):
		self.printworld(True)

	def createBlocked(self):
		#assign 20% of total board to blocked
		for cell in range(3840):
			row = randint(0,119)
			col = randint(0,159)
			if(self.data[row,col].decode() == 'a' or self.data[row,col].decode() == 'b' or self.data[row,col].decode() == 'S' or self.data[row,col].decode() == 'G'):
				cell-=1
				continue
			else:
				self.data[row,col] = '0'

	def in_bounds(self, cell):
		x = cell[0]
		y = cell[1]
		if(0<=x<=119) and (0<=y<=159):
			return True
		else:
			return False

	def connected_cells(self, cell):
		#cell is a list [row, col]
		x = int(cell[0])
		y = int(cell[1])
		connected_cells = list()
		#Highway
		if self.data[x, y] == 'a' or self.data[x, y] == 'b':
			all_possible = [(x, y+1), (x, y-1), (x+1, y), (x-1, y)]
		#NotHighway
		else:
			all_possible = [(x, y+1), (x, y-1), (x+1, y+1), (x+1, y), (x+1, y-1), (x-1, y), (x-1, y+1), (x-1, y-1)]
		for (row, col) in all_possible:
			if self.in_bounds((row,col)) and self.data[row,col].decode() != '0' and self.data[row,col].decode() != 'S':
				connected_cells.append(tuple((row,col)))
		return connected_cells

	def generateTexture(self):
		#Start, Goal, and hard_travers can all be found in load as global variables
		#randonly assign hard to traverse cells to the 31x31 grid surrounding the centers in hard_travers
		for pair in hard_travers:
			for x in range(pair[0]-15, pair[0]+15):
				for y in range(pair[1]-15, pair[1]+15):
					if randint(0,1) == 1 and x>=0 and x<=119 and y>=0 and y<=159:
						if (start[0] == x and start[1] == y) or (goal[0] == x and goal[1] == y):
							continue
						else:
							self.data[x, y] = '2'

	def createHighways(self):
		global highwaylist
		highwaylist = [[], [], [], []]
		for number in range(4):
			s = randomHighwayStart()
			row = s[0]
			col = s[1]
			#North
			if s[2] == 0:
				highwaylist[number] = self.plotNorth(row, col)
				pass
			#South
			elif s[2] == 1:
				highwaylist[number] = self.plotSouth(row, col)
				pass

			#East
			elif s[2] == 2:
				highwaylist[number] = self.plotEast(row, col)
				pass

			#West
			elif s[2] == 3:
				highwaylist[number] = self.plotWest(row, col)
				pass
			if highwaylist[number] == None or len(highwaylist[number]) < 100:
				number-=1
			else:
				for pair in highwaylist[number]:
					if self.data[pair[0], pair[1]].decode() == '1':
						self.data[pair[0], pair[1]] = 'a'
					elif self.data[pair[0], pair[1]].decode() == '2':
						self.data[pair[0], pair[1]] = 'b'

	def plotNorth(self, row, col):
		curr = []
		curr.append([row, col])
		#First 20 extend perpendicular to border
		for _ in range(20):
			row+=1
			if self.data[row,col].decode() == 'a' or self.data[row,col].decode() == 'b' :
				return None
			else:
				curr.append([row,col])
		#Next 20 60% chance to go straight, 20% chance to diverge until over 100 or wall
		while len(curr) < 100:
			r2 = randint(0,7)
			for _ in range(20):
				#Goes Straight
				if 0<=r2<=5:
					row+=1
					if(not(self.in_bounds([row,col]))):
						return curr
					if self.data[row,col].decode() == 'a' or self.data[row,col].decode() == 'b' :
						return None
					else:
						curr.append([row,col])
				#Goes left
				elif r2 == 6:
					col+=1
					if(not(self.in_bounds([row,col]))):
						return curr
					if self.data[row,col].decode() == 'a' or self.data[row,col].decode() == 'b' :
						return None
					else:
						curr.append([row,col])
				#Goes right
				elif r2 == 7:
					col-=1
					if(not(self.in_bounds([row,col]))):
						return curr
					if self.data[row,col].decode() == 'a' or self.data[row,col].decode() == 'b' :
						return None
					else:
						curr.append([row,col])



		return curr

	def plotSouth(self, row, col):
		curr = []
		curr.append([row, col])
		#First 20 extend perpendicular to border
		for _ in range(20):
			row-=1
			if self.data[row,col].decode() == 'a' or self.data[row,col].decode() == 'b' :
				return None
			else:
				curr.append([row,col])
		#Next 20 60% chance to go straight, 20% chance to diverge until over 100 or wall
		while len(curr) < 100:
			r2 = randint(0,7)
			for _ in range(20):
				#Goes Straight
				if 0<=r2<=5:
					row-=1
					if(not(self.in_bounds([row,col]))):
						return curr
					if self.data[row,col].decode() == 'a' or self.data[row,col].decode() == 'b' :
						return None
					else:
						curr.append([row,col])
				#Goes left
				elif r2 == 6:
					col-=1
					if(not(self.in_bounds([row,col]))):
						return curr
					if self.data[row,col].decode() == 'a' or self.data[row,col].decode() == 'b' :
						return None
					else:
						curr.append([row,col])
				#Goes right
				elif r2 == 7:
					col+=1
					if(not(self.in_bounds([row,col]))):
						return curr
					if self.data[row,col].decode() == 'a' or self.data[row,col].decode() == 'b' :
						return None
					else:
						curr.append([row,col])

		return curr
		
	def plotEast(self, row, col):
		curr = []
		curr.append([row, col])
		#First 20 extend perpendicular to border
		for _ in range(20):
			col-=1
			if self.data[row,col].decode() == 'a' or self.data[row,col].decode() == 'b' :
				return None
			else:
				curr.append([row,col])
		#Next 20 60% chance to go straight, 20% chance to diverge until over 100 or wall
		while len(curr) < 100:
			r2 = randint(0,7)
			for _ in range(20):
				#Goes Straight
				if 0<=r2<=5:
					col-=1
					if(not(self.in_bounds([row,col]))):
						return curr
					if self.data[row,col].decode() == 'a' or self.data[row,col].decode() == 'b' :
						return None
					else:
						curr.append([row,col])
				#Goes left
				elif r2 == 6:
					row+=1
					if(not(self.in_bounds([row,col]))):
						return curr
					if self.data[row,col].decode() == 'a' or self.data[row,col].decode() == 'b' :
						return None
					else:
						curr.append([row,col])
				#Goes right
				elif r2 == 7:
					row-=1
					if(not(self.in_bounds([row,col]))):
						return curr
					if self.data[row,col].decode() == 'a' or self.data[row,col].decode() == 'b' :
						return None
					else:
						curr.append([row,col])
		return curr

	def plotWest(self, row, col):
		curr = []
		curr.append([row, col])
		#First 20 extend perpendicular to border
		for _ in range(20):
			col+=1
			if self.data[row,col].decode() == 'a' or self.data[row,col].decode() == 'b' :
				return None
			else:
				curr.append([row,col])
		#Next 20 60% chance to go straight, 20% chance to diverge until over 100 or wall
		while len(curr) < 100:
			r2 = randint(0,7)
			for _ in range(20):
				#Goes Straight
				if 0<=r2<=5:
					col+=1
					if(not(self.in_bounds([row,col]))):
						return curr
					if self.data[row,col].decode() == 'a' or self.data[row,col].decode() == 'b' :
						return None
					else:
						curr.append([row,col])
				#Goes left
				elif r2 == 6:
					row-=1
					if(not(self.in_bounds([row,col]))):
						return curr
					if self.data[row,col].decode() == 'a' or self.data[row,col].decode() == 'b' :
						return None
					else:
						curr.append([row,col])
				#Goes right
				elif r2 == 7:
					row+=1
					if(not(self.in_bounds([row,col]))):
						return curr
					if self.data[row,col].decode() == 'a' or self.data[row,col].decode() == 'b' :
						return None
					else:
						curr.append([row,col])

		return curr

def randomHighwayStart():
	r1 = randint(0, 3)
	#North
	if r1 == 0:
		cols = randint(0,159)
		s = [0, cols, r1]
	#South
	elif r1 == 1:
		cols = randint(0,159)
		s = [119, cols, r1]
	#East
	elif r1 == 2:
		rows = randint(0,119)
		s = [rows, 159, r1]
	#West
	elif r1 == 3:
		rows = randint(0,119)
		s = [rows, 0, r1] 
	else:
		exit('ERROR: r1 is equal to ' + r1 + ' terminating from highway creator')
	return s
def randomize(w):
	#Defines start and Goal
	global start
	start = [None, None]
	global goal
	goal = [None, None]

	r1 = randint(0,3)
	#North
	if r1 == 0:
		rows = randint(0,19)
		cols = randint(0,159)
		rowg = randint(99,119)
		colg = randint(0,159)
		start = [rows, cols]
		goal = [rowg, colg]
	#South
	elif r1 == 1:
		rows = randint(99,119)
		cols = randint(0,159)
		rowg = randint(0,19)
		colg = randint(0,159)
		start = [rows, cols]
		goal = [rowg, colg]
	#East
	elif r1 == 2:
		rows = randint(0,119)
		cols = randint(139,159)
		rowg = randint(0,119)
		colg = randint(0,19)
		start = [rows, cols]
		goal = [rowg, colg]
	#West
	elif r1 == 3:
		rows = randint(0,119)
		cols = randint(0,19)
		rowg = randint(0,119)
		colg = randint(139,159)
		start = [rows, cols]
		goal = [rowg, colg]
	if w.data[start[0], start[1]].decode() == '0' or w.data[goal[0], goal[1]].decode() == '0' or w.data[start[0], start[1]].decode() == 'a' or w.data[goal[0], goal[1]].decode() == 'a' or w.data[start[0], start[1]].decode() == 'b' or w.data[goal[0], goal[1]].decode() == 'b':
		print("triggered")
		w.rotateSnG()
	w.setSnG()

	global hard_travers
	hard_travers = []
	for _ in range(8):
		hard_travers.append([randint(0,119), randint(0,159)])

def load(w):
	if(input("Would you like to load a file? (y/n): ") != "y"):
		randomize(w)
		return
	with open(input("Please enter the path to input file: "), 'r') as f:
		input_list = f.read().strip().split("\n")
		#First line will provide the coordinates of start
		global start
		start = [None, None]
		token = input_list[0].split(",")
		start[0] = int(token[0])
		start[1] = int(token[1])
		#Second line will provide the coordinates of goal
		global goal
		goal = [None, None]
		token = input_list[1].split(",")
		goal[0] = int(token[0])
		goal[1] = int(token[1])
		#Next EIGHT lines will provide the coordinates of the centers of the hard to traverse regions
		global hard_travers
		hard_travers = [input_list[2].split(","), input_list[3].split(","), input_list[4].split(","), input_list[5].split(","), input_list[6].split(","), input_list[7].split(","), input_list[8].split(","), input_list[9].split(",")]
		for pair in hard_travers:
			pair[0] = int(pair[0])
			pair[1] = int(pair[1])

def unload():
	with open(input("Please enter the path to output file: "), 'w') as f:
		f.write("Start: ")
		f.write(str(start[0]) + "," + str(start[1]) + "\n")
		f.write("Goal: ")
		f.write(str(goal[0]) + "," + str(goal[1]) + "\n")

		f.write("Hard Traversal: ")
		for l in hard_travers:
			f.write(str(l[0]) + "," + str(l[1]) + "\n")

		f.write("Highway List: ")
		for pair in highwaylist:
			f.write(str(pair[0])+","+str(pair[1])+ "\n")

# search

def createPath(parent):
	path = set()
	path.add(parent.position)
	ptr = parent.parent
	while(ptr is not None):
		path.add(ptr.position)
		ptr = ptr.parent
	return path

def uniformCostSearch(world, heuristic):
	visited = set()
	pq = queue.PriorityQueue()
	start_node = Node(tuple((world.start[0], world.start[1])), None)
	pq.put((start_node.f, start_node))

	while not pq.empty():
		cur = pq.get()
		curr_node = cur[1]
		if curr_node not in visited:
			visited.add(curr_node)

			if curr_node.position == tuple(world.goal):
				return createPath(curr_node.parent), closedToPos(visited)
			for nextCell in world.connected_cells(curr_node.position):
				nextNode = Node(nextCell, curr_node)
				if nextNode not in visited:
					cost = getCost(world, curr_node, nextNode)
					nextNode.g = curr_node.g + cost
					nextNode.h = getHeuristic(world, nextNode, heuristic)
					nextNode.f = nextNode.g + nextNode.h
					pq.put((nextNode.f, nextNode))
	return None

def aStarSearch(world, heuristic, weight):
	# when weight == 1: normal A*
	# when weight > 1: weighted A*
	closedList = set() # collection of expanded nodes
	openQueue = queue.PriorityQueue() # collection of all generated nodes
	openList = set()

	start_node = Node(tuple((world.start[0], world.start[1])), None)
	start_node.f = 0
	openQueue.put((start_node.f, start_node))
	openList.add(start_node)

	while not openQueue.empty():
		# get next in open list and set as current node
		cur = openQueue.get()
		try:
			openList.remove(cur[1])
		except KeyError:
			print("yep")
		#Node is the second item in the tuple
		curr_node = cur[1]
        #Check if goal 
		if curr_node.position == tuple(world.goal):
			return createPath(curr_node.parent), closedToPos(closedList)
		closedList.add(curr_node)
		#Generates the current node's 8 (or 4 if highway) possible neighbors
		for nextCell in world.connected_cells(curr_node.position):
			next_node = Node(nextCell, curr_node)
			#If node is in the closed list move on
			if next_node in closedList:
				continue
			cost = getCost(world, curr_node, next_node)
			next_node.g = curr_node.g + cost
			next_node.h = getHeuristic(world, next_node, heuristic)
			next_node.f = next_node.g + (float(weight) * next_node.h)
			#Check if new node is in the open list, and if it has a lower f
			if next_node in openList:
				for node in openList:
					if(node.position == next_node.position) and (next_node.f < node.f):
						node.g = next_node.g
						node.h = next_node.h
						node.f = next_node.f
						node.parent = next_node.parent
						node.position = next_node.position
						break
			else:
				openList.add(next_node)
				openQueue.put((int(next_node.f), next_node))

	return None, closedToPos(closedList) # path not found

def closedToPos(closedList):
	posList = []
	for node in closedList:
		posList.append(node.position)
	return posList

def getHeuristic(w, node, heuristic):
	x1, y1 = node.position[0], node.position[1]
	x2, y2 = w.goal[0], w.goal[1]

	if heuristic.lower() == "manhattan":
		return abs(x1-x2) + abs(y1-y2)
	elif heuristic.lower() == "euclidean":
		return math.sqrt((x1-x2)**2 + (y1-y2)**2)
	elif heuristic.lower() == "euclidean_squared":
		return (x1-x2)**2 + (y1-y2)**2
	elif heuristic.lower() == "chebyshev":
		return abs(x1-x2) + abs(y1-y2) - min(abs(x1-x2),abs(y1-y2))
	elif heuristic.lower() == "octile":
		return abs(x1-x2) + abs(y1-y2) - (math.sqrt(2)-2) * min(abs(x1-x2),abs(y1-y2))
	elif heuristic.lower() == "mini_manhattan":
		return (abs(x1-x2) + abs(y1-y2))/2

def getCost(world, current, nextCell):
	currType = world.data[current.position[0], current.position[1]].decode()
	if(currType == 'S'):
		currType = '1'
	nextType = world.data[nextCell.position[0], nextCell.position[1]].decode()
	if(nextType == 'S' or nextType == 'G'):
		nextType = '1'
	currR = current.position[0]
	currC = current.position[1]
	nextR = nextCell.position[0]
	nextC = nextCell.position[1]
	#Boolean value to see if row and col changed
	changeR = bool((abs(nextR-currR)) > 0)
	changeC = bool((abs(nextC-currC)) > 0)
	#Sets boolean value for diagonal and horizontalOrVertical (horv)
	diagonal = changeR and changeC

	#Current cell is an unblocked
	if currType == '1':
		#Next is unblocked
		if nextType == '1':
			if not diagonal:
				return 1
			else:
				return math.sqrt(2)
		#Next is hard to traverse
		elif nextType == '2':
			if not diagonal:
				return 1.5
			else:
				return (math.sqrt(2) + math.sqrt(8))/2
		#Next is unblocked highway
		elif nextType == 'a':
			if not diagonal:
				return 0.25
			else:
				return (math.sqrt(2))/4
		#Next is hard to traverse highway
		elif nextType == 'b':
			if not diagonal:
				return float(3/8)
			else:
				return float((math.sqrt(2) + math.sqrt(8))/8)
	#Current cell is hard to traverse
	if currType == '2':
		#Next is unblocked
		if nextType == '1':
			if not diagonal:
				return 1.5
			else:
				return (math.sqrt(2) + math.sqrt(8))/2
		#Next is hard to traverse
		elif nextType == '2':
			if not diagonal:
				return 2
			else:
				return math.sqrt(8)
		#Next is unblocked highway
		elif nextType == 'a':
			if not diagonal:
				return float(3/8)
			else:
				return float((math.sqrt(2) + math.sqrt(8))/8)
		#Next is hard to traverse highway
		elif nextType == 'b':
			if not diagonal:
				return float(1/2)
			else:
				return float(math.sqrt(8)/4)
	#Current cell is an unblocked highway
	if currType == 'a':
		#Next is unblocked
		if nextType == '1':
			if not diagonal:
				return 1
			else:
				return math.sqrt(2)
		#Next is hard to traverse
		elif nextType == '2':
			if not diagonal:
				return 1.5
			else:
				return float((math.sqrt(2) + math.sqrt(8))/2)
		#Next is unblocked highway
		elif nextType == 'a':
			if not diagonal:
				return 0.25
			else:
				return (math.sqrt(2))/4
		#Next is hard to traverse highway
		elif nextType == 'b':
			if not diagonal:
				return float(3/8)
			else:
				return float((math.sqrt(2) + math.sqrt(8))/8)
	#Current cell is a hard to traverse highway
	if currType == 'b':
		#Next is unblocked
		if nextType == '1':
			if not diagonal:
				return 1.5
			else:
				return (math.sqrt(2) + math.sqrt(8))/2
		#Next is hard to traverse
		elif nextType == '2':
			if not diagonal:
				return 2
			else:
				return math.sqrt(8)
		#Next is unblocked highway
		elif nextType == 'a':
			if not diagonal:
				return float(3/8)
			else:
				return (math.sqrt(2))/4
		#Next is hard to traverse highway
		elif nextType == 'b':
			if not diagonal:
				return float(1/2)
			else:
				return float(math.sqrt(8)/4)
	print(currType, nextType)
	return None

# gui

FRAME_SIZE = 960
WEIGHT = 1

def draw_handler(canvas):
	drawMap(canvas)

def generateMap():
	global currentWorld
	currentWorld = world()
	wipePath()

def getMap():
	return world()

def input_handler():
	pass

def drawMap(canvas):
	w = 1280 / 160
	t = 960 / 120
	global path, visited
	for col in range(120):
		for row in range(160):
			pts = [(row * t, col * w), ((row + 1) * t, col * w),
						  ((row + 1) * t, (col + 1) * w), ((row * t), (col + 1) * w)]
			# Draw first and last cell
			if [col, row] == currentWorld.start:
				canvas.draw_polygon(pts, 1, "Black", "#00FF00")
			elif [col, row] == currentWorld.goal:
				canvas.draw_polygon(pts, 1, "Black", "#ff0000")
			elif currentWorld.data[col, row].decode() == '0':
				canvas.draw_polygon(pts, 1, "Black", "#292929")
			elif (col, row) in path:
				canvas.draw_polygon(pts, 1, "Black", "#4CAF50")
			elif (col, row) in visited:
				canvas.draw_polygon(pts, 1, "Black", "#C8E6C9")
			elif currentWorld.data[col, row].decode() == 'a':
				canvas.draw_polygon(pts, 1, "Black", "#add8e6")
			elif currentWorld.data[col, row].decode() == 'b':
				canvas.draw_polygon(pts, 1, "Black", "Blue")
			elif currentWorld.data[col, row].decode() == '1':
				canvas.draw_polygon(pts, 1, "Black", "White")
			elif currentWorld.data[col, row].decode() == '2':
				canvas.draw_polygon(pts, 1, "Black", "#9B9898")
			else:
				canvas.draw_polygon(pts, 1, "Black", "#464646")
def wipePath():
	global path, visited
	path = []
	visited = []

def paramCheck():
	if heur.get_text()[19:] not in ["Euclidean", "Manhattan", "E^2", "Chebyshev", "Octile", "M.M."]:
		heur.set_text("Current Heuristic: Euclidean")

def aStarSolve():
	global path, visited
	if inputWeight.get_text() != "1":
		inputWeight.set_text("1")
	paramCheck()
	algo.set_text("Current Algorithm: A*")
	if heur.get_text()[19:] == "Euclidean":
		path, visited = aStarSearch(currentWorld, "euclidean", 1)
	elif heur.get_text()[19:] == "Manhattan":
		path, visited = aStarSearch(currentWorld, "manhattan", 1)
	elif heur.get_text()[19:] == "E^2":
		path, visited = aStarSearch(currentWorld, "euclidean_squared", 1)
	elif heur.get_text()[19:] == "Chebyshev":
		path, visited = aStarSearch(currentWorld, "chebyshev", 1)
	elif heur.get_text()[19:] == "Octile":
		path, visited = aStarSearch(currentWorld, "octile", 1)
	elif heur.get_text()[19:] == "M.M.":
		path, visited = aStarSearch(currentWorld, "mini_manhattan", 1)
	else:
		path, visited = aStarSearch(currentWorld, "euclidean", 1)
	if path:
		status.set_text("Current Status: Path Found")
		visitedCells.set_text("# of Visited Cells: " + str(len(visited)))
		pathLen.set_text("Length of Path: " + str(len(path)))
	else:
		status.set_text("Current Status: No Path")
	
def ucsSolve():
	global path, visited
	algo.set_text("Current Algorithm: UCS")
	paramCheck()
	if heur.get_text()[19:] == "Euclidean":
		path, visited = uniformCostSearch(currentWorld, "euclidean")
	elif heur.get_text()[19:] == "Manhattan":
		path, visited = uniformCostSearch(currentWorld, "manhattan")
	elif heur.get_text()[19:] == "E^2":
		path, visited = uniformCostSearch(currentWorld, "euclidean_squared")
	elif heur.get_text()[19:] == "Chebyshev":
		path, visited = uniformCostSearch(currentWorld, "chebyshev")
	elif heur.get_text()[19:] == "Octile":
		path, visited = uniformCostSearch(currentWorld, "octile")
	elif heur.get_text()[19:] == "M.M.":
		path, visited = uniformCostSearch(currentWorld, "mini_manhattan")
	else:
		path, visited = uniformCostSearch(currentWorld, "euclidean")
	if path:
		status.set_text("Current Status: Path Found")
		visitedCells.set_text("# of Visited Cells: " + str(len(visited)))
		pathLen.set_text("Length of Path: " + str(len(path)))
	else:
		status.set_text("Current Status: No Path")

def weightedAStarSolve():
	global path, visited
	algo.set_text("Current Algorithm: Weighted A*")
	paramCheck()
	weight = inputWeight.get_text()
	if heur.get_text()[19:] == "Euclidean":
		path, visited = aStarSearch(currentWorld, "euclidean", weight)
	elif heur.get_text()[19:] == "Manhattan":
		path, visited = aStarSearch(currentWorld, "manhattan", weight)
	elif heur.get_text()[19:] == "E^2":
		path, visited = aStarSearch(currentWorld, "euclidean_squared", weight)
	elif heur.get_text()[19:] == "Chebyshev":
		path, visited = aStarSearch(currentWorld, "Chebyshev", weight)
	elif heur.get_text()[19:] == "Octile":
		path, visited = aStarSearch(currentWorld, "octile", weight)
	elif heur.get_text()[19:] == "M.M.":
		path, visited = aStarSearch(currentWorld, "mini_manhattan", weight)
	else:
		path, visited = aStarSearch(currentWorld, "euclidean", weight)
	if path:
		status.set_text("Current Status: Path Found")
		visitedCells.set_text("# of Visited Cells: " + str(len(visited)))
		pathLen.set_text("Length of Path: " + str(len(path)))
	else:
		status.set_text("Current Status: No Path")

def generateBenchmark():
	global currentWorld
	worlds = []
	# pathAvg = dict()
	# visitedAvg = dict()
	for i in range(49):
		worlds.append(getMap())
	total = dict()
	for algo in ["UCS", "A*", "A*W1.5", "A*W2"]:
		timeAvg = dict()
		for h in ["euclidean", "manhattan", "chebyshev", "octile", "mini_manhattan"]:
			# totalPathLen = 0
			# totalVisited = 0
			avgTime = 0
			for world in worlds:
				s = time.time()
				if algo == "UCS":
					path, visited = uniformCostSearch(world, h)
				elif algo == "A*":
					path, visited = aStarSearch(world, h, 1)
				elif algo == "A*W1.5":
					path, visited = aStarSearch(world, h, 1.5)
				elif algo == "A*W2":
					path, visited = aStarSearch(world, h, 2)
				e = time.time()
				avgTime += (e-s)*1000
				# totalPathLen+=len(path)
				# totalVisited+=len(visited)
			# pathAvg[h] = totalPathLen/50
			# visitedAvg[h] = totalVisited/50
			timeAvg[h] = avgTime/50
		total[algo] = timeAvg
	print(total)


	# print(pathAvg)
	# print(visitedAvg)
	print(timeAvg)


def sequentialAStarSolve():
	aStarSolve()
	algo.set_text("Current Algorithm: Seq. A*")

#couldn't figure out how to pass param to button_handler
def resetText():
	algo.set_text("Current Algorithm: N/A")
	status.set_text("Current Status: N/A")
	visitedCells.set_text("# of Visited Cells: N/A")
	pathLen.set_text("Length of Path: N/A")
def setheuristicE():
	heur.set_text("Curent Heuristic: Euclidean")
	resetText()
def setheuristicM():
	heur.set_text("Current Heuristic: Manhattan")
	resetText()
def setheuristicES():
	heur.set_text("Current Heuristic: E^2")
	resetText()
def setheuristicC():
	heur.set_text("Current Heuristic: Chebyshev")
	resetText()
def setheuristicO():
	heur.set_text("Current Heuristic: Octile")
	resetText()
def setheuristicMM():
	heur.set_text("Current Heuristic: M.M.")
	resetText()


def main():
	global currentWorld
	currentWorld = world()
	global path, visited
	path = []
	visited = []
	# generateBenchmark()
	return
	frame = simplegui.create_frame("Heuristic Search", 1280, 960)
	frame.add_button("Generate Map", generateMap, 100)
	frame.add_button("Update Start/Goal", currentWorld.rotateSNGHandler,100)
	frame.set_draw_handler(draw_handler)
	global inputWeight
	inputWeight = frame.add_input("Weight", input_handler, 50)
	inputWeight.set_text(str(WEIGHT))

	frame.add_label("")
	frame.add_label("Heuristic:")
	frame.add_button("Euclidean", setheuristicE, 100)
	frame.add_button("Manhattan", setheuristicM, 100)
	frame.add_button("Euclidean Squared", setheuristicES, 100)
	frame.add_button("Chebyshev", setheuristicC, 100)
	frame.add_button("Octile", setheuristicO, 100)
	frame.add_button("Mini Manhattan", setheuristicMM, 100)

	frame.add_label("")
	frame.add_label("Search Algorithm:")
	frame.add_button("UCS", ucsSolve, 100)
	frame.add_button("A*", aStarSolve, 100)
	frame.add_button("Weighted A*", weightedAStarSolve, 100)
	frame.add_button("Sequential A*", sequentialAStarSolve, 100)

	frame.add_label("")
	global algo, heur, status, visitedCells, pathLen
	algo = frame.add_label("Current Algorithm: N/A")
	heur = frame.add_label("Current Heuristic: N/A")
	status = frame.add_label("Current Status: N/A")
	visitedCells = frame.add_label("# of Visited Cells: N/A")
	pathLen = frame.add_label("Length of Path: N/A")

	frame.add_label("")
	frame.add_label("Key:")
	frame.add_label("Green = Start")
	frame.add_label("Red = Goal")
	frame.add_label("White = Unblocked")
	frame.add_label("Black = Blocked")
	frame.add_label("Gray = Hard to Traverse")
	frame.add_label("Light Blue = Unblocked Highway")
	frame.add_label("Blue = Hard Traverse Highway")
	frame.add_label("Light Green = Visited")
	frame.add_label("Green = Path")

	frame.add_label("")
	frame.add_button("Save Map", currentWorld.saveCurrentMap, 100)
	frame.add_button("Load Map", currentWorld.callLoad, 100) 
	frame.add_button("Wipe Path", wipePath, 100)

	frame.start()

if __name__ == "__main__":
	main()
