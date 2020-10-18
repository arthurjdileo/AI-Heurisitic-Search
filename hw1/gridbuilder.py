from random import randint
import numpy as np



def wipeHighways(world):
    for pair in highwaylist:
        if world.data[pair[0], pair[1]] == 'a':
            world.data[pair[0], pair[1]] = 1
        elif world.data[pair[0], pair[1]] == 'b':
            world.data[pair[0], pair[1]] = 2


class world:
    def __init__(self):
        self.data = np.chararray(shape=(120, 160))
        self.data[:] = '1'
    def printworld(self):
        with open(input("Please enter the path to output file: "), 'w') as f:
            for row in self.data:
                f.write(row)
                f.write('\n')
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
        #assigns the start index
        self.data[start[0],start[1]] = 'S'
        #assigns the goal index
        self.data[goal[0],goal[1]] = 'G'
    def createHighways(self):
        global highwaylist
        highwaylist = []
        count = 0
        for _ in range(4):
            # Randomly choose to begin at the North, West, South, or East border wall
            r1 = np.random.randint(0, 3)
            # The West Border
            if r1 == 0:
                # The column coordinate must be 0
                col = 0
                # The row coordinate will be a random point along the first column
                row = np.random.randint(0, 119)
                # assign either a or b depending on if cell is unblocked(1) or hardToTraverse(2)
                if self.data[row, col] == '1':
                    self.data[row, col] = 'a'
                elif self.data[row, col] == '2':
                    self.data[row, col] = 'b'
                # Move the highway away from the boundary for 20 cells
                pair = [row, col]
                highwaylist.append(pair)
                count+=1
                for _ in range(20):
                    col += 1
                    #If the next cell is already a highway, wipe highways and restart
                    if self.data[row, col] == 'a' or self.data[row, col] == 'b':
                        #function to wipe highways from map
                        #Calls itself to make new highways, repeats until no intersection
                        continue
                    #if the next cell is not a highway, continue
                    else:
                        pair = [row, col]
                        highwaylist.append(pair)
                        count+=1
                        if self.data[row, col] == '1':
                            self.data[row, col] = 'a'
                        elif self.data[row, col] == '2':
                            self.data[row,col] = 'b'
                #Move the highway with 60% chance of going straight and 20% chance of left/right
                while 0 <= row and row <= 119 and 0 <= col and col <= 159:
                    r2 = np.random.randint(0,9)
                    #60% chance to continue straight
                    if 0 <= r2 <= 5:
                        #continues straight for 20 cells
                        for _ in range(20):
                            col += 1
                            if(col < 0 or col > 159):
                                continue
                            #If the next cell is already a highway, wipe highways and restart
                            if self.data[row, col] == 'a' or self.data[row, col] == 'b':
                                #function to wipe highways from map
                                #Calls itself to make new highways, repeats until no intersection
                                continue
                            #if the next cell is not a highway, continue
                            else:
                                pair = [row, col]
                                highwaylist.append(pair)
                                count+=1
                                if self.data[row, col] == '1':
                                    self.data[row, col] = 'a'
                                elif self.data[row, col] == '2':
                                    self.data[row,col] = 'b'
                    #20% chance to move left/right
                    #10% chance to move left
                    elif r2 == 6:
                        #continues left for 20 cells
                        for _ in range(20):
                            row -= 1
                            if(row < 0 or row > 119):
                                continue
                            #If the next cell is already a highway, wipe highways and restart
                            if self.data[row, col] == 'a' or self.data[row, col] == 'b':
                                #function to wipe highways from map
                                #Calls itself to make new highways, repeats until no intersection
                                continue
                            #if the next cell is not a highway, continue
                            else:
                                pair = [row, col]
                                highwaylist.append(pair)
                                count+=1
                                if self.data[row, col] == '1':
                                    self.data[row, col] = 'a'
                                elif self.data[row, col] == '2':
                                    self.data[row,col] = 'b'

                    #10% chance to move right
                    elif r2 == 7:
                        #continues right for 20 cells
                        for _ in range(20):
                            row += 1
                            if(row < 0 or row > 119):
                                continue
                            #If the next cell is already a highway, wipe highways and restart
                            if self.data[row, col] == 'a' or self.data[row, col] == 'b':
                                #function to wipe highways from map
                                #Calls itself to make new highways, repeats until no intersection
                                continue
                            #if the next cell is not a highway, continue
                            else:
                                pair = [row, col]
                                highwaylist.append(pair)
                                count+=1
                                if self.data[row, col] == '1':
                                    self.data[row, col] = 'a'
                                elif self.data[row, col] == '2':
                                    self.data[row,col] = 'b'
                    #20% chance to stop
                    else:
                        pass

            elif r1 == 1:
                # The North Border
                # The row coordinate must be 0
                row = 0
                # The column coordinate will be a random point along the first row
                col = np.random.randint(0, 159)
                # assign either a or b depending on if cell is unblocked(1) or hardToTraverse(2)
                if self.data[row, col] == '1':
                    self.data[row, col] = 'a'
                elif self.data[row, col] == '2':
                    self.data[row, col] = 'b'
                # Move the highway away from the boundary for 20 cells
                pair = [row, col]
                highwaylist.append(pair)
                count+=1
                for _ in range(20):
                    row += 1
                    #If the next cell is already a highway, wipe highways and restart
                    if self.data[row, col] == 'a' or self.data[row, col] == 'b':
                        #function to wipe highways from map
                        #Calls itself to make new highways, repeats until no intersection
                        continue
                    #if the next cell is not a highway, continue
                    else:
                        pair = [row, col]
                        highwaylist.append(pair)
                        count+=1
                        if self.data[row, col] == '1':
                            self.data[row, col] = 'a'
                        elif self.data[row, col] == '2':
                            self.data[row,col] = 'b'
                #Move the highway with 60% chance of going straight and 20% chance of left/right
                while 0 <= row and row <= 119 and 0 <= col and col <= 159:
                    r2 = np.random.randint(0,9)
                    #60% chance to continue straight
                    if 0 <= r2 <= 5:
                        #continues straight for 20 cells
                        for _ in range(20):
                            #straight is down the map
                            row += 1
                            if(row < 0 or row > 119):
                                continue
                            #If the next cell is already a highway, wipe highways and restart
                            if self.data[row, col] == 'a' or self.data[row, col] == 'b':
                                #function to wipe highways from map
                                #Calls itself to make new highways, repeats until no intersection
                                continue
                            #if the next cell is not a highway, continue
                            else:
                                pair = [row, col]
                                highwaylist.append(pair)
                                count+=1
                                if self.data[row, col] == '1':
                                    self.data[row, col] = 'a'
                                elif self.data[row, col] == '2':
                                    self.data[row,col] = 'b'
                    #20% chance to move left/right
                    #10% chance to move left
                    elif r2 == 6:
                        #continues left for 20 cells
                        for _ in range(20):
                            col += 1
                            if(col < 0 or col > 159):
                                continue
                            #If the next cell is already a highway, wipe highways and restart
                            if self.data[row, col] == 'a' or self.data[row, col] == 'b':
                                #function to wipe highways from map
                                #Calls itself to make new highways, repeats until no intersection
                                continue
                            #if the next cell is not a highway, continue
                            else:
                                pair = [row, col]
                                highwaylist.append(pair)
                                count+=1
                                if self.data[row, col] == '1':
                                    self.data[row, col] = 'a'
                                elif self.data[row, col] == '2':
                                    self.data[row,col] = 'b'

                    #10% chance to move right
                    elif r2 == 7:
                        #continues right for 20 cells
                        for _ in range(20):
                            col -= 1
                            if(col < 0 or col > 159):


                                continue
                            #If the next cell is already a highway, wipe highways and restart
                            if self.data[row, col] == 'a' or self.data[row, col] == 'b':
                                #function to wipe highways from map

                                #Calls itself to make new highways, repeats until no intersection

                                continue
                            #if the next cell is not a highway, continue
                            else:
                                pair = [row, col]
                                highwaylist.append(pair)
                                count+=1
                                if self.data[row, col] == '1':
                                    self.data[row, col] = 'a'
                                elif self.data[row, col] == '2':
                                    self.data[row,col] = 'b'

                    #20% chance to stop
                    else:
                        pass

            elif r1 == 2:
                # The East Border
                # The column coordinate is the last column

                col = len(self.data[0]) - 1

                # The row coordinate will be a random point along the last column

                row = np.random.randint(0, 119)

                # assign either a or b depending on if cell is unblocked(1) or hardToTraverse(2)

                if self.data[row, col] == '1':
                    self.data[row, col] = 'a'
                elif self.data[row, col] == '2':
                    self.data[row, col] = 'b'

                # Move the highway away from the boundary for 20 cells
                pair = [row, col]
                highwaylist.append(pair)
                count+=1
                for _ in range(20):
                    col -= 1
                    #If the next cell is already a highway, wipe highways and restart
                    if self.data[row, col] == 'a' or self.data[row, col] == 'b':
                        #function to wipe highways from map

                        #Calls itself to make new highways, repeats until no intersection

                        continue
                    #if the next cell is not a highway, continue
                    else:
                        pair = [row, col]
                        highwaylist.append(pair)
                        count+=1
                        if self.data[row, col] == '1':
                            self.data[row, col] = 'a'
                        elif self.data[row, col] == '2':
                            self.data[row,col] = 'b'

                #Move the highway with 60% chance of going straight and 20% chance of left/right
                while 0 <= row and row <= 119 and 0 <= col and col <= 159:

                    r2 = np.random.randint(0,9)
                    #60% chance to continue straight
                    if 0 <= r2 <= 5:
                        #continues straight for 20 cells
                        for _ in range(20):
                            #straight is down the map
                            col -= 1
                            if(col < 0 or col > 159):


                                continue
                            #If the next cell is already a highway, wipe highways and restart
                            if self.data[row, col] == 'a' or self.data[row, col] == 'b':
                                #function to wipe highways from map

                                #Calls itself to make new highways, repeats until no intersection

                                continue
                            #if the next cell is not a highway, continue
                            else:
                                pair = [row, col]
                                highwaylist.append(pair)
                                count+=1
                                if self.data[row, col] == '1':
                                    self.data[row, col] = 'a'
                                elif self.data[row, col] == '2':
                                    self.data[row,col] = 'b'
                    #20% chance to move left/right
                    #10% chance to move left
                    elif r2 == 6:
                        #continues left for 20 cells
                        for _ in range(20):
                            row += 1
                            if(row < 0 or row > 119):


                                continue
                            #If the next cell is already a highway, wipe highways and restart
                            if self.data[row, col] == 'a' or self.data[row, col] == 'b':
                                #function to wipe highways from map

                                #Calls itself to make new highways, repeats until no intersection

                                continue
                            #if the next cell is not a highway, continue
                            else:
                                pair = [row, col]
                                highwaylist.append(pair)
                                count+=1
                                if self.data[row, col] == '1':
                                    self.data[row, col] = 'a'
                                elif self.data[row, col] == '2':
                                    self.data[row,col] = 'b'

                    #10% chance to move right
                    elif r2 == 7:
                        #continues right for 20 cells
                        for _ in range(20):
                            row -= 1
                            if(row < 0 or row > 159):


                                continue
                            #If the next cell is already a highway, wipe highways and restart
                            if self.data[row, col] == 'a' or self.data[row, col] == 'b':
                                #function to wipe highways from map

                                #Calls itself to make new highways, repeats until no intersection

                                continue
                            #if the next cell is not a highway, continue
                            else:
                                pair = [row, col]
                                highwaylist.append(pair)
                                count+=1
                                if self.data[row, col] == '1':
                                    self.data[row, col] = 'a'
                                elif self.data[row, col] == '2':
                                    self.data[row,col] = 'b'

                    #20% chance to stop
                    else:
                        pass

            elif r1 == 3:
                # The South Border

                # The row coordinate will be the last row

                row = len(self.data) - 1

                # The column coordinate will be a random point along the last row

                col = np.random.randint(0, 159)

                # assign either a or b depending on if cell is unblocked(1) or hardToTraverse(2)

                if self.data[row, col] == '1':
                    self.data[row, col] = 'a'
                elif self.data[row, col] == '2':
                    self.data[row, col] = 'b'

                # Move the highway away from the boundary for 20 cells
                pair = [row, col]
                highwaylist.append(pair)
                count+=1
                for _ in range(20):
                    row -= 1
                    #If the next cell is already a highway, wipe highways and restart
                    if self.data[row, col] == 'a' or self.data[row, col] == 'b':
                        #function to wipe highways from map

                        #Calls itself to make new highways, repeats until no intersection

                        continue
                    #if the next cell is not a highway, continue
                    else:
                        pair = [row, col]
                        highwaylist.append(pair)
                        count+=1
                        if self.data[row, col] == '1':
                            self.data[row, col] = 'a'
                        elif self.data[row, col] == '2':
                            self.data[row,col] = 'b'
                #Move the highway with 60% chance of going straight and 20% chance of left/right
                while 0 <= row and row <= 119 and 0 <= col and col <= 159:

                    r2 = np.random.randint(0,9)
                    #60% chance to continue straight
                    if 0 <= r2 <= 5:
                        #continues straight for 20 cells
                        for _ in range(20):
                            #straight is down the map
                            row -= 1
                            if(row < 0 or row > 119):


                                continue
                            #If the next cell is already a highway, wipe highways and restart
                            if self.data[row, col] == 'a' or self.data[row, col] == 'b':
                                #function to wipe highways from map

                                #Calls itself to make new highways, repeats until no intersection

                                continue
                            #if the next cell is not a highway, continue
                            else:
                                pair = [row, col]
                                highwaylist.append(pair)
                                count+=1
                                if self.data[row, col] == '1':
                                    self.data[row, col] = 'a'
                                elif self.data[row, col] == '2':
                                    self.data[row,col] = 'b'
                    #20% chance to move left/right
                    #10% chance to move left
                    elif r2 == 6:
                        #continues left for 20 cells
                        for _ in range(20):
                            col -= 1
                            if(col < 0 or col > 159):


                                continue
                            #If the next cell is already a highway, wipe highways and restart
                            if self.data[row, col] == 'a' or self.data[row, col] == 'b':
                                #function to wipe highways from map

                                #Calls itself to make new highways, repeats until no intersection

                                continue
                            #if the next cell is not a highway, continue
                            else:
                                pair = [row, col]
                                highwaylist.append(pair)
                                count+=1
                                if self.data[row, col] == '1':
                                    self.data[row, col] = 'a'
                                elif self.data[row, col] == '2':
                                    self.data[row,col] = 'b'

                    #10% chance to move right
                    elif r2 == 7:
                        #continues right for 20 cells
                        for _ in range(20):
                            col += 1
                            if(col < 0 or col > 159):


                                continue
                            #If the next cell is already a highway, wipe highways and restart
                            if self.data[row, col] == 'a' or self.data[row, col] == 'b':
                                #function to wipe highways from map

                                #Calls itself to make new highways, repeats until no intersection

                                continue
                            #if the next cell is not a highway, continue
                            else:
                                pair = [row, col]
                                highwaylist.append(pair)
                                count+=1
                                if self.data[row, col] == '1':
                                    self.data[row, col] = 'a'
                                elif self.data[row, col] == '2':
                                    self.data[row,col] = 'b'

                    #20% chance to stop
                    else:
                        pass

            else:
                exit('ERROR: r1 is equal to ' + r1 + ' terminating from highway creator')

            #Check length of highway
            if count < 100:
                continue

def load():
    if(raw_input("Would you like to load a file? (y/n): ") != "y"):
        randomize()
        return
    with open(input("Please enter the path to input file: "), 'r') as f:
        input_list = f.read().strip().split("\n")
        #First line will provide the coordinates of start
        global start
        start = input_list[0].split(",")
        start = map(int, start)
        #Second line will provide the coordinates of goal
        global goal
        goal = input_list[1].split(",")
        goal = map(int, goal)
        #Next EIGHT lines will provide the coordinates of the centers of the hard to traverse regions
        global hard_travers
        hard_travers = [input_list[2].split(","), input_list[3].split(","), input_list[4].split(","), input_list[5].split(","), input_list[6].split(","), input_list[7].split(","), input_list[8].split(","), input_list[9].split(",")]
        for pair in hard_travers:
            pair[0] = int(pair[0])
            pair[1] = int(pair[1])
        global highwaylist

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
            f.write(str(pair[0])+","+str(pair[1])+"\n")

def randomize():
    global start
    global goal
    global hard_travers

def main():
	load()
	w = world()
	w.generateTexture()
	w.createHighways()
	w.printworld()


if __name__ == "__main__":
	main()
