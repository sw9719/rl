import pygame
import Game
import os
import dqn
import random as r
import time
import math as m
import torch
import numpy as np

os.environ['SDL_AUDIODRIVER'] = 'dsp'

qnetwork = dqn.NeuralNetwork()
target = dqn.NeuralNetwork(True)
gamma = 0.9

e = 1
ep_end = 0.001

steps = 1000000
decay_factor = (ep_end/e)**(1/steps)

batch_size = 64


C = 2000

st = None
st1 = None

game = Game.game()

running = True

def gatherq(out,r):
    q = torch.zeros((batch_size))
    for i in range(batch_size):
        q[i] = out[i][r[i]]
    return q        


def learn():
    global e
    batch = game.replay_memory.sample(batch_size)
    st = torch.zeros((batch_size,2,6,6))
    st1 = torch.zeros((batch_size,2,6,6))
    a = torch.zeros(batch_size)
    r = torch.zeros(batch_size,dtype=torch.int8)
    for i in range(batch_size):
        st[i] = torch.tensor(batch[i][0])
        a[i] = torch.tensor(batch[i][1])
        r[i] = torch.tensor(batch[i][2])
        st1[i] = torch.tensor(batch[i][3])
    out = qnetwork.forward(st)
    q = gatherq(out,r)
    q1max = target.forward(st1).max(dim=1).values
    tq = r + gamma*q1max
    loss = qnetwork.criterion(q,tq)
    qnetwork.zero_grad()
    loss.backward()
    for param in qnetwork.parameters():
            param.grad.data.clamp_(-1, 1)
    qnetwork.optim.step()
    print("Loss: ",loss.item(),"e: ",e)
    if(game.matches % C == 0):
        target.load_state_dict(qnetwork.state_dict())
    if(game.matches % 1000 == 0):
        torch.save(target.state_dict(), "weights.pt")

def get_move():
    global e
    grd = game.grid
    st = torch.zeros((2,6,6))
    st[0] = torch.tensor(grd['atoms'])
    st[1] = torch.tensor(grd['player'])
    move = -1
    ind = torch.where(st[1].flatten() != 0)
    #n = game.matches
    #e = abs(m.cos(n**(0.8/batch_size)))/n**(1/50)
    e = e*decay_factor
    choice = [True,False]
    weight = [1-e,e]
    takemax = r.choices(choice,weights=weight,k=1)
    if takemax is True:
        out = qnetwork.forward(st)
        valid_qs = torch.gather(out,0,ind[0])
        maxq = valid_qs.max()
        move = torch.where(out == maxq)[0][0]
    else:
        move =  r.choice(ind[0].tolist())
    return int(move/6), int(move % 6)


while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:

            running = False
        
    x,y = r.choice(game.get_valid_moves())
    game.show_move(x,y)
    pygame.display.flip()

    if(game.has_ended()):
        print("winner is player:", game.winner())
        game.reset()
        if game.matches > 50:
            learn()
        continue
    

    st = game.copy_state()

    #x,y = r.choice(game.get_valid_moves())
    x,y = get_move()

    game.show_move(x,y)
    st1 = game.copy_state()
    rw = game.get_reward(st,st1)
    a = game.get_action(x,y)
    game.replay_memory.push(st,a,rw,st1)
    pygame.display.flip()
    
    if(game.has_ended()):
        print("winner is player:", game.winner())
        game.reset()
        if game.matches > 50:
            learn()
        #running = False
    
        



# Done! Time to quit.

pygame.quit()
