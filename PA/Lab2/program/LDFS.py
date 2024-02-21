import func_timeout
from maze import *


class LDFS:
    def __init__(self):
        self.iterat = 0
        self.state = 0
        self.mem_st = 0
        self.stop = 0

    def search(self,m, x, y, start, end):
        return func_timeout.func_timeout(30*60, self._search, args=[m, x, y, start, end])

    def _search(self, m, x, y, start, end):
        self.iterat = 0
        self.mem_st = 0
        self.stop = 0
        self.state = 0
        limit =  x*y//3
        m_copy = m
        dir_map = self.new_map(m)
        priority = ["bottom", "right", "top", "left"]
        aPath = {}
        cells = [start]
        movement = [start]
        pathF = False
        
        while len(movement) > 0:

            self.iterat+=1
            curr = movement.pop()

            if curr == end:
                pathF = True
                break

            if len(movement) > self.mem_st:
                self.mem_st = len(movement)

            if len(aPath) - 1 == limit:
                self.stop+=1
                break
            n = 0
            for direction in priority:
                if not dir_map[curr][direction]:
                    n+=1
                if dir_map[curr][direction]:
                    if direction == "left":
                        nextStep = (curr[0], curr[1] - 1)
                    elif direction == "top":
                        nextStep = (curr[0] - 1, curr[1])
                    elif direction == "right":
                        nextStep = (curr[0], curr[1] + 1)
                    else:
                        nextStep = (curr[0] + 1, curr[1])

                    if n == 3:
                        self.stop+=1
                    if nextStep in cells:
                        continue
                    cells.append(nextStep)
                    movement.append(nextStep)
                    aPath[nextStep]=curr        
        if (pathF == True):
            fwdPath={}
            cell=end
            while cell!=start:
                fwdPath[aPath[cell]]=cell
                cell=aPath[cell]
            printPath(fwdPath)

            for i in fwdPath:
                if m_copy[i[0]][i[1]] != 'S' and m_copy[i[0]][i[1]] != 'E':
                    m_copy[i[0]][i[1]] = 'P'

            for i in range(x):
                for j in range(y):
                    if (m[i][j]!="w"):
                        self.state += 1

            
            self.mem_st += len(movement)
            printMaze(m_copy, x, y)
        else:
            print("NO")


    def new_map(self, m):
        dir_map = {}

        for i in range(len(m)):
            for j in range(len(m[i])):
                x = i
                y = j
                curr = (x, y)
                dir_map[curr] = {"left": self.is_dir(m, i, j-1),
                                 "top": self.is_dir(m, i-1, j),
                                 "right": self.is_dir(m, i, j+1),
                                 "bottom": self.is_dir(m, i+1, j)}


        return dir_map
 
    def is_dir(self, m, x, y):
        if x>=len(m) or x<0 or y>=len(m[x]) or y<0:
            return False
        return True if m[x][y] == "c" or m[x][y] == "E" else False
