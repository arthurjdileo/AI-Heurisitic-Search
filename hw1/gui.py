try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui


# dark gray, white, red, green, light gray
colors = ['#292929','white', '#EB1717', "#83FF00",  '#9B9898']
FRAME_SIZE = 1000
WEIGHT = 1

currentParams = ["", ""]

def draw_handler(canvas):
    pass

def generateMap():
    pass

def input_handler():
    pass

def solve_with_a_star_euclidean():
    pass

def solve_with_a_star_manhattan():
    pass

def setHeurisitic(h):
    global heur
    heur.set_text("Current Heurisitic: " + h)

frame = simplegui.create_frame("Heuristic Search", FRAME_SIZE, FRAME_SIZE)
frame.add_button("Generate Map", generateMap, 100)
frame.set_draw_handler(draw_handler)
inputWeight = frame.add_input("Weight", input_handler, 50)
inputWeight.set_text(str(WEIGHT))

frame.add_label("")
frame.add_label("Heuristic:")
frame.add_button("Euclidean", setHeurisitic("Euclidean"), 100)
frame.add_button("Manhattan", setHeurisitic("Manhattan"), 100)

frame.add_label("")
frame.add_label("Search Algorithm:")
frame.add_button("A*", solve_with_a_star_euclidean, 100)
frame.add_button("Weighted A*", solve_with_a_star_manhattan, 100)
frame.add_button("Sequential", solve_with_a_star_manhattan, 100)

global algo
global status
global visitedCells
global pathLen
frame.add_label("")
algo = frame.add_label("Current Algorithm: N/A")
global heur
heur = frame.add_label("Current Heuristic: N/A")
status = frame.add_label("Current Status: N/A")
visitedCells = frame.add_label("# of Visited Cells: N/A")
pathLen = frame.add_label("Length of Path: N/A")

frame.start()
