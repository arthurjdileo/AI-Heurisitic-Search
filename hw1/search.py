import queue
import math
import gridbuilder

start = (gridbuilder.start[0], gridbuilder.start[1])
goal = (gridbuilder.goal[0], gridbuilder.goal[1])

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