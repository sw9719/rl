import pygame
import Game
import os
import time
import random as r


os.environ['SDL_AUDIODRIVER'] = 'dsp'

game = Game.game()
moves = 0

running = True

while running:


    # Did the user click the window close button?

    for event in pygame.event.get():

        '''if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX,mouseY = pygame.mouse.get_pos()
            if (game.pos_in_grid(mouseX)) and (game.pos_in_grid(mouseY)):
                # get the cell index inside the grid
                x = int((mouseX - 50) / 70) # this is actually column number(for visualizing)
                y = int((mouseY - 50) / 70) # and this is actually row number
                if(moves < 2):
                    moves += 1
                game.show_move(x,y)
                if(game.has_ended() and moves >= 2):
                    print("winner is player",game.winner())
                    running = False
            else:
                print("not in")'''
        if event.type == pygame.QUIT:

            running = False
        
        
    if(moves < 2):
        moves += 1
    x,y = r.choice(game.get_valid_moves())
    game.show_move(y,x)
    pygame.display.flip()
    if(game.has_ended() and moves >= 2):
        #print("winner is player",game.winner())
        game.reset()
        moves = 0
        #running = False
        



# Done! Time to quit.

pygame.quit()
