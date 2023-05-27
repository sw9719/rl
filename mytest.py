from dqn import NeuralNetwork
import torch.nn as nn
import torch

inp = torch.zeros((2,6,6))
inp[0] = torch.randint(0,4,(6,6))
inp[1] = torch.randint(0,2,(6,6))
model = NeuralNetwork()

criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
the_loss = 0

optimizer.zero_grad()
x = model.forward(inp)
output = torch.randint(0,1,(36,),dtype=torch.float)
loss = criterion(output, x)
loss.backward()
optimizer.step()
the_loss = loss.item()