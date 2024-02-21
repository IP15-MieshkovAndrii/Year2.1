import func_timeout
from maze import *
from queue import PriorityQueue
import math
import os
import psutil


class AStar:
    def __init__(self):
        self.iterat = 0
        self.state = 0
        self.mem_st = 0

    def grid(self, rows, cols):
        grid=[]
        maze_map={}
        y=0
        for n in range(cols):
            x = 1
            y = 1+y
            for m in range(rows):
                grid.append((x,y))
                maze_map[x,y]={'right':0,'left':0,'top':0,'bottom':0}
                x = x + 1 
        return grid

    def h(self, cell1, cell2):
        x1,y1=cell1
        x2,y2=cell2

        return math.sqrt((x1-x2)**2 + (y1-y2)**2)

    def search(self,m, x, y, start, end):
        return func_timeout.func_timeout(30*60, self._search, args=[m, x, y, start, end])    

    def _search(self, m, x, y, start, end):
        self.iterat = 0
        self.state = 0
        self.mem_st = 0

        m_copy = m
        dir_map = self.new_map(m)
        priority = ["bottom", "right", "top", "left"]

        g_score = {cell:float('inf') for cell in self.grid(x, y)}
        g_score[start]=0
        f_score={cell:float('inf') for cell in self.grid(x, y)}
        f_score[start] = self.h(start, end)


        border=PriorityQueue()
        border.put((self.h(start, end), self.h(start, end), start))
        aPath = {}
        states = []
        pathF = False
        while not border.empty():
            if psutil.Process(os.getpid()).memory_info().rss > 1024**3:
                raise MemoryError("1 Gb memory exceeded")
            self.iterat += 1

            if border.qsize() > self.mem_st:
                self.mem_st = border.qsize()

            curr = border.get()[2]

            if curr not in states:
                states.append(curr)

            if curr == end:
                pathF = True
                break

            for d in priority:
                if dir_map[curr][d]==True:
                    if d=='right':
                        nextcell=(curr[0],curr[1]+1)
                    if d=='left':
                        nextcell=(curr[0],curr[1]-1)
                    if d=='top':
                        nextcell=(curr[0]-1,curr[1])
                    if d=='bottom':
                        nextcell=(curr[0]+1,curr[1])
                    temp_g_score=g_score[curr]+1
                    temp_f_score=temp_g_score+self.h(curr,end)

                    if temp_f_score < f_score[nextcell]:
                        g_score[nextcell]= temp_g_score
                        f_score[nextcell]= temp_f_score
                        border.put((temp_f_score,self.h(nextcell,end),nextcell))
                        aPath[nextcell]=curr
                        
                    # if self.iterat > 1 and m_copy[curr[0]][curr[1]] != 'S':
                    #         m_copy[curr[0]][curr[1]] = 'P'
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
            printMaze(m_copy, x, y)
            for i in range(x):
                for j in range(y):
                    if (m[i][j]!="w"):
                        self.state += 1

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
