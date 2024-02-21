from LDFS import LDFS
from ASTAR import AStar
from maze import *
from colorama import Fore



class Test:
    def __init__(self):
        self.ldfs = LDFS()
        self.astar = AStar()

    def create_mazes(self, x, y):
        m = Maze(x, y)

    def test_ldfs(self, n=20):
        iterat = 0
        state = 0
        mem_st = 0
        stop = 0
        x = 10
        y = 10
        for _ in range(n):
            m, start, end = Maze(x, y)
            self.ldfs.search(m, x, y, start, end)
            print(Fore.WHITE + f"Maze {x}x{y}\n"
                    f"Iterations: {self.ldfs.iterat}, n of states: {self.ldfs.state}, max stack len: {self.ldfs.mem_st}, "
                  f"n of stops: {self.ldfs.stop}\n")
            iterat += self.ldfs.iterat
            state += self.ldfs.state
            mem_st += self.ldfs.mem_st
            stop += self.ldfs.stop


        print(f"Average iterations: {iterat/n}\n"
              f"Average n of states: {state/n}\n"
              f"Average max stack: {mem_st/n}\n"
              f"Average n of stops: {stop/n}\n")
           


    def test_astar(self, n=20):
        iterat = 0
        state = 0
        mem_st = 0
        x = 10
        y = 10
        for _ in range(n):
            m, start, end = Maze(x, y)
            self.astar.search(m, x, y, start, end)
            print(Fore.WHITE + f"Maze {x}x{y}\n"
                    f"Iterations: {self.astar.iterat}, n of states: {self.astar.state}, max stack len: {self.astar.mem_st} ")
            iterat += self.astar.iterat
            state += self.astar.state
            mem_st += self.astar.mem_st


        print(f"Average iterations: {iterat/n}\n"
              f"Average n of states: {state/n}\n"
              f"Average max stack: {mem_st/n}\n")

    