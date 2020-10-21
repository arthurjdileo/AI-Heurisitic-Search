from random import randint
import numpy as np
import queue
import math
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

class world:
    def __init__(self):
        self.data = np.chararray(shape=(120, 160))
        self.data[:] = '1'
        load()
        self.start = start
        self.goal = goal
        self.hard_travers = hard_travers
        self.generateTexture()
        self.createHighways()
        self.highwaylist = highwaylist
        self.createBlocked()
        self.setSnG()

    def setSnG(self):
        #assigns the start index
        self.data[start[0],start[1]] = 'S'
        #assigns the goal index
        self.data[goal[0],goal[1]] = 'G'

    def printworld(self):
        with open(input("Please enter the path to output file: "), 'w') as f:
            for row in self.data:
                f.write(str(row, 'utf-8'))
                f.write('\n')
    def createBlocked(self):
        #assign 20% of total board to blocked
        for cell in range(3840):
            row = randint(0,119)
            col = randint(0,159)
            if(self.data[row,col].decode() == 'a' or self.data[row,col].decode() == 'b'):
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
        x = cell[0]
        y = cell[1]
        connected_cells = set()
        all_possible = [(x, y+1), (x, y-1), (x+1, y+1), (x+1, y), (x+1, y-1), (x-1, y), (x-1, y+1), (x-1, y-1)]
        for (row, col) in all_possible:
            if self.in_bounds((row,col)):
                if self.data[row,col] != '0':
                    connected_cells.add((row,col))
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
def randomize():
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



    global hard_travers
    hard_travers = []
    for _ in range(8):
        hard_travers.append([randint(0,119), randint(0,159)])

def load():
    if(input("Would you like to load a file? (y/n): ") != "y"):
        randomize()
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
def aStarSearch(world, heurisitic, weight):
	# when weight == 1: normal A*
	# when weight > 1: weighted A*
	closedList = set() # collection of expanded nodes
	openList = queue.PriorityQueue() # collection of all generated nodes
	costPerCell = {start: 0} # collection of cost from start to specific node
	parent = {}

	closedList.add(start)
	openList.put((0, start))

	while not openList.empty():
		# get next in open list and set as current node
		cur = openList.get()

		if cur == goal:
			p = createPath(parent)
			# return visited nodes and path
			return (closedList, p)
		
		for node in world.connected_cells(cur):
			cost = costPerCell[cur] + getCost(world, parent, node)
			if node not in closedList:
				costPerCell[node] = cost
				parent[node] = cur
				closedList.add(node)
				openList.put((cost + (weight * getHeurisitic(node, heurisitic)), node))
	return (closedList, None) # path not found

def createPath(parent):
	path = []
	cur = parent[goal]
	while cur != (0, 0):
		path = path + tuple(cur)
		cur = parent[cur]
	return path[::-1]

def getHeurisitic(node, heurisitic):
	x1, y1 = node.x, node.y
	x2, y2 = gridbuilder.goal[0], gridbuilder.goal[1]
	if heurisitic == "manhattan":
		return abs(x1-x2) + abs(y1-y2)
	elif heurisitic == "euclidean":
		return math.sqrt((x1-x2)**2 + (y1-y2)**2)
	elif heurisitic == "euclidean_squared":
        	return (x1-x2)**2 + (y1-y2)**2
	elif heurisitic == "chebyshev":
		return abs(x1-x2) + abs(y1-y2) - min(abs(x1-x2),abs(y1-y2))
	elif heurisitic == "octile":
		return abs(x1-x2) + abs(y1-y2) - (math.sqrt(2)-2) * min(abs(x1-x2),abs(y1-y2))
	elif heurisitic == "mini_manhattan":
		return (abs(x1-x2) + abs(y1-y2))/4
	elif heurisitic == "mini_euclidean":
		return math.sqrt((x1-x2)**2 + (y1-y2)**2)/4

def getCost(world, parent, node):
	cellType = world.data[node[0], node[1]]
	parentType = world.data[parent[0], parent[1]]
	return 1
	if cellType == '1':
		if parentType == '1':
			if node.direction == "horiz" or node.direction == "vert":
				return 1
			else:
				return math.sqrt(2)
		elif parentType == '2':
			if node.direction == "horiz" or node.direction == "vert":
				return 1.5
			else:
				return ((math.sqrt(2)+math.sqrt(8))/2)
	elif cellType == 2:
		if parentType == 2:
			if node.direction == "horiz" or node.direction == "vert":
				return 2
			else:
				return math.sqrt(8)
		elif parentType == 1:
			if node.direction == "horiz" or node.direction == "vert":
				return 1.5
			else:
				return ((math.sqrt(2)+math.sqrt(8))/2)
	elif cellType == 'a': 
		if parentType == 'a':
			return 0.25
		elif parentType == 'b':
				return 0.375
	elif cellType == 'b':
		if parentType == 'b':
				return 0.5
		elif parentType == 'a':
				return 0.375


# gui
# FRAME_SIZE = 1000
# WEIGHT = 1

# currentParams = ["", ""]

# def draw_handler(canvas):
#     pass

# def generateMap():
#     pass

# def input_handler():
#     pass

# def solve_with_a_star_euclidean():
#     pass

# def solve_with_a_star_manhattan():
#     pass

# def setHeurisitic(h):
#     # global heur
#     # heur.set_text("Current Heurisitic: " + h)
#     pass

# frame = simplegui.create_frame("Heuristic Search", FRAME_SIZE, FRAME_SIZE)
# frame.add_button("Generate Map", generateMap, 100)
# frame.set_draw_handler(draw_handler)
# inputWeight = frame.add_input("Weight", input_handler, 50)
# inputWeight.set_text(str(WEIGHT))

# frame.add_label("")
# frame.add_label("Heuristic:")
# frame.add_button("Euclidean", setHeurisitic("Euclidean"), 100)
# frame.add_button("Manhattan", setHeurisitic("Manhattan"), 100)

# frame.add_label("")
# frame.add_label("Search Algorithm:")
# frame.add_button("A*", solve_with_a_star_euclidean, 100)
# frame.add_button("Weighted A*", solve_with_a_star_manhattan, 100)
# frame.add_button("Sequential", solve_with_a_star_manhattan, 100)

# global algo
# global status
# global visitedCells
# global pathLen
# frame.add_label("")
# algo = frame.add_label("Current Algorithm: N/A")
# global heur
# heur = frame.add_label("Current Heuristic: N/A")
# status = frame.add_label("Current Status: N/A")
# visitedCells = frame.add_label("# of Visited Cells: N/A")
# pathLen = frame.add_label("Length of Path: N/A")

# frame.start()

def main():
    w = world()
    w.generateTexture()
    w.createHighways()
    w.createBlocked()
    w.printworld()
    print(aStarSearch(world, "manhattan", 1))

if __name__ == "__main__":
	main()
