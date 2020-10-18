import queue
import math

def aStarSearch(arr, heurisitic, weight):
	# when weight == 1: normal A*
	# when weight > 1: weighted A*
	closedList = set() # collection of expanded nodes
	openList = queue.PriorityQueue() # collection of all generated nodes
	costPerCell = {arr.startPosition: 0} # collection of cost from start to specific node
	parent = {}

	closedList.add(arr.startPosition)
	openList.put((0, arr.startPosition))

	while not openList.empty():
		# get next in open list and set as current node
		cur = openList.get()

		if cur == END_POSITION:
			p = buildPath(parent)
			# return visited nodes and path
			return (closedList, p)
		
		for node in connectedNodes(cur):
			cost = costPerCell[cur] + getCost(parent, node)
			if node not in closedList:
				costPerCell[node] = cost
				parent[node] = cur
				closedList.add(node)
				openList.put((cost + weight * getHeurisitic(node, heurisitic), node))
	return (closedList, None) # path not found

def buildPath(pathDict):
	path = []
	cur = pathDict[END_POSITION]
	while cur != (0, 0):
		path = path + tuple(current)
		cur = pathDict[cur]
	return path[::-1]

def getHeurisitic(node, heurisitic):
	x1, y1 = node.x, node.y
	x2, y2 = END_POSITION
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

def getCost(parent, node):
	if node.type == 1:
		if parent.type == 1:
			if node.direction == "horiz" || node.direction == "vert":
				return 1
			else:
				return math.sqrt(2)
		elif parent.type == 2:
			if node.direction == "horiz" || node.direction == "vert":
				return 1.5
			else:
				return ((math.sqrt(2)+math.sqrt(8))/2)
	elif node.type == 2:
		if parent.type == 2:
			if node.direction == "horiz" || node.direction == "vert":
				return 2
			else:
				return math.sqrt(8)
		elif parent.type == 1:
			if node.direction == "horiz" || node.direction == "vert":
				return 1.5
			else:
				return ((math.sqrt(2)+math.sqrt(8))/2)
	elif node.type == 'a': 
		if parent.type == 'a':
            		return 0.25
        	elif parent.type == 'b':
            		return 0.375
    	elif node.type == 'b':
        	if parent.type == 'b':
            		return 0.5
        	elif parent.type == 'a':
            		return 0.375