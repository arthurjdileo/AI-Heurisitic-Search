import queue
import math

def aStarSearch(arr, heurisitic):
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
            cost = costPerCell[cur] + getCost(node)
            if node not in closedList:
                costPerCell[node] = cost
                parent[node] = cur
                closedList.add(node)
                openList.put((cost + getHeurisitic(node, heurisitic)))
    return (closedList, None) # path not found