import pygame
import numpy as np
class colors:
    # a class declaring rgb values of colors
    white =  (255,255,255)
    green =  (0,255,0)
    blue  =  (0,0,255)
    black =  (0,0,0)
    yellow = (255,251,0)

class board():
    # game class holds sets up the game in pygame and initializes its state
    def __init__(self,screen) -> None:
        self.player_color = [colors.blue,colors.green]
        self.grid_coords = self.init_coords()
        if screen:
            self.screen = screen
            self.reset_board()
        else:
            self.draw_board()

    def reset_board(self):
        for i in range(6):
            for j in range(6):
                cell = self.grid_coords[i][j]
                pygame.draw.rect(self.screen,colors.black,(cell[0]+1,cell[1]+1,68,68))

    
    def init_coords(self):
        # set top left coordinates for each cell in a 2-d list
        coords = [[None for _ in range(6)] for _ in range(6)]
        for x in range(6):
            for y in range(6):
                coords[x][y] = (50+70*y,50+70*x)
        return coords
    
    def draw_board(self):
    # drawing board routine and is called only once in the entire program
        pygame.init()
        self.screen = pygame.display.set_mode([520, 520])
        self.screen.fill((0, 0, 0))
        pygame.draw.lines(self.screen,colors.white,True,[(50,50),(470,50),(470,470),(50,470)],1)
        for n in range(50,470,70):
            pygame.draw.line(self.screen,colors.white,(n,50),(n,470),1) #Horizontal
            pygame.draw.line(self.screen,colors.white,(50,n),(470,n),1) #Vertical
        pygame.display.update()
    
    def getCellCenter(self,x,y):    
    # simply check if coordinated lie outside the game box. If not,
    # then return the center of cell where text can be rendered
        if x < 0 or x > 5 or y < 0 or y > 5:
            print("invalid cell location")
            return 0,0
        return 70*(y+1)+8,70*(x+1)
        
    
    def drawtext(self,X,Y,grid):
    # replaces the cell with black rectangle and renders number of atoms as number inside it
    # with color coding
        cell = self.grid_coords[X][Y]
        pygame.draw.rect(self.screen,colors.black,(cell[0]+1,cell[1]+1,68,68))
        if grid['atoms'][X][Y] == 0:
            return
        myfont = pygame.font.SysFont("monospace",25)
        val = grid['atoms'][X][Y]
        color = self.player_color[grid['player'][X][Y]]
        label = myfont.render(str(val), 1, color)
        self.screen.blit(label,self.getCellCenter(X,Y))
    
    def show_move(self,grid):
        #grid['player'][x][y] contains player number at cell x,y
        # so we take the color based on player color
        for i in range(6):
            for j in range(6):          
                self.drawtext(i,j,grid)
    
    def pos_in_grid(self,pos):
        if (pos > 50 and pos < 470):
            return True
        else:
            return False
    
    def set_counter(self,c):
        myfont = pygame.font.SysFont("monospace",25)
        color = colors.yellow
        label = myfont.render(str(c), 1, color)
        pygame.draw.rect(self.screen,colors.black,(10,10,500,30))
        self.screen.blit(label,(10,10,500,30))


