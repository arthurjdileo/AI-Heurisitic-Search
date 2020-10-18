try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui


# dark gray, white, red, green, light gray
colors = ['#292929','white', '#EB1717', "#83FF00",  '#9B9898']
FRAME_WIDTH = 700
DEFAULT_SIZE = 100
DEFAULT_PROBABILITY = 0.2
global frame

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

def init():
    global frame
    frame = simplegui.create_frame("Heuristic Search", FRAME_WIDTH, FRAME_WIDTH)
    frame.add_button("Generate Map", generateMap, DEFAULT_SIZE)
    frame.set_draw_handler(draw_handler)
    inputSize = frame.add_input('Size', input_handler, 50)
    inputSize.set_text(str(DEFAULT_SIZE))
    inputProb = frame.add_input("Probability", input_handler, 50)
    inputProb.set_text(str(DEFAULT_PROBABILITY))

    frame.add_label("")
    frame.add_label("Heuristic")
    frame.add_button("Euclidean", solve_with_a_star_euclidean, 100)
    frame.add_button("Manhattan", solve_with_a_star_manhattan, 100)

    frame.add_label("")
    frame.add_label("Search Algorithm")
    frame.add_button("A*", solve_with_a_star_euclidean, 100)
    frame.add_button("Weighted A*", solve_with_a_star_manhattan, 100)
    frame.add_button("Sequential", solve_with_a_star_manhattan, 100)

    # Display status
    frame.add_label("")
    algorithm_used = frame.add_label("Current Algorithm: N/A")
    status_label = frame.add_label("Current Status: N/A")
    no_of_visited_cells_label = frame.add_label("# of Visited Cells: N/A")
    path_length_label = frame.add_label("Length of Path: N/A")

    frame.start()

init()
