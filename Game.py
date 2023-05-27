import os
import numpy as np
from graphics import board
from queue import Queue
import random as r

class Memory:
    def __init__(self,size) -> None:
        self.memory = []
        self.size = size

    def push(self,st,a,r,st1):
        if(len(self.memory) >= self.size):
            self.memory.pop(0)
        self.memory.insert(self.size,[st,a,r,st1])

    def sample(self,n):
        return r.sample(self.memory,n)

class game:

    matches = 0
    replay_memory = Memory(500)
    def __init__(self,screen = None) -> None:
        self.board = board(screen)
        self.grid = self.init_grid()
        self.player = 0
        game.matches += 1
        self.move_queue = Queue()
        self.board.set_counter(game.matches)
        self.moves = 0
    
    def reset(self):
        self.__init__(self.board.screen)

    def getRect(self,x,y):
        # return top left coordinates from cell location in grid
        return [50+70*x,50+70*y]

    def init_grid(self):
        # grid is a dictionary that contains playing grid metadata with following values
        # player: which player is currently occupying the block. -1 for none
        # atoms: the actual number of atoms in that box:
        grid = {}
        grid['player'] = np.full([6,6],-1,dtype=int)
        grid['atoms'] = np.zeros([6,6],dtype=int)
        return grid

    def get_neighbours(self,x,y):
        corner = [(0,0),(5,0),(0,5),(5,5)]
        if (x,y) in corner:
            return 2
        edge = []
        for j in range(6):
            for i in range(6):
                if i != j and (i in [0,5] or j in [0,5]):
                    edge.append((i,j))
        if (x,y) in edge:
            return 3
        else:
            return 4
        
    def get_neighbour_indices(self,x,y):
        lst = []
        tmp = [(x+1,y),(x,y+1),(x-1,y),(x,y-1)]
        for X,Y in tmp:
            if X >= 0 and X <= 5 and Y >= 0 and Y <= 5:
                lst.append((X,Y))
        return lst

    def fission(self):
        while not self.move_queue.empty() and not self.has_ended():
            self.do_fission()

    
   
    def do_fission(self):
        # Very important :1
        # First it checks if the number of atoms is about to exceed the neighbours or not
        # if it does, the atoms spread to adjacent atoms, leaving the current cell empty
        # however, we now need to check in the adjacent atoms for the same condition
        # as long as the atoms are equal to number of atoms, they keep spreading, creating a chain reaction
        # The fission queue will keep on growing
        # After some time, the grid will either stabilize or a player will occupy all cells, denoting the game end
        x,y = self.move_queue.get()
        adj = self.get_neighbours(x,y)
        self.grid['atoms'][x][y] += 1
        if (self.grid['atoms'][x][y] < adj):
            self.grid['player'][x][y] = self.player
            return None
        self.grid['atoms'][x][y] = 0
        self.grid['player'][x][y] = -1
        ind = self.get_neighbour_indices(x,y)
        for i in ind:
            self.move_queue.put(i)

    def change_player(self):
        if (self.player == 0):
            self.player = 1
        else:
            self.player = 0


    def show_move(self,x,y):
        # grid['player'] is a 2d numpy array mapping which player is using the cell in grid
        # First check if player is doing a valid move and update grid accordingly
        # finally, flip the current player to denote change of turn
        if (self.grid['player'][x][y] != self.player) and (self.grid['atoms'][x][y] != 0):
            print("Error: Invalid move by",self.player)
            #print(x,y)
            #print(self.grid)
            os._exit(0)
            return -1
        #print(x,y)
        self.move_queue.put((x,y))
        self.fission()
        self.moves += 1

        self.board.show_move(self.grid)

        self.change_player()
    
    def pos_in_grid(self,n):
        return self.board.pos_in_grid(n)
    
    def has_ended(self):
        if self.moves < 2:
            return False
        p = self.grid['player']
        if (np.any(p == 1) and np.any(p == 0)):
            return False
        return True
    
    def winner(self):
        p = self.grid['player']
        #print(p)
        if ( np.any(p == 0)):
            return 0
        else:
            return 1
    
    def get_valid_moves(self):
        valid = []
        for i in range(6):
            for j in range(6):
                if self.grid['player'][i][j] == self.player or self.grid['atoms'][i][j] == 0:
                    valid.append((i,j))
        return valid

    def get_reward(self,st,st1):
        rw = 0
        if np.count_nonzero(st1[1] == 0) < np.count_nonzero(st[1] == 0):
            rw += 0.1
        if self.has_ended() and self.winner() == 1:
            rw += 0.9
        elif self.has_ended():
            rw -= 0.9
        return rw

    def get_action(self,x,y):
        return 6*x+y
    
    def copy_state(self):
        s = np.zeros((2,6,6))
        s[0] = np.copy(self.grid['atoms'])
        s[1] = np.copy(self.grid['player'])
        return s


        
        