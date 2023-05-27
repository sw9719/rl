import torch
from torch import nn

class NeuralNetwork(nn.Module):
    def __init__(self,target = False):
       super(NeuralNetwork, self).__init__()
       self.fc1 = nn.Linear(72,48)
       torch.nn.init.kaiming_uniform_(self.fc1.weight,
                               a=0, mode="fan_in",
                               nonlinearity="relu")
       self.fc2 = nn.Linear(48,36)
       torch.nn.init.kaiming_uniform_(self.fc2.weight,
                               a=0, mode="fan_in",
                               nonlinearity="relu")
       if not target:
          self.optim = torch.optim.Adam(self.parameters(), lr=0.001)
          self.criterion = nn.HuberLoss()

    def forward(self, x):
       x = self.pre_process(x)
       x = self.fc1(x)
       x = torch.relu(x)
       x = self.fc2(x)
       x = torch.relu(x)
       return x
    
    def pre_process(self,x):
        x[:,0] = x[:,0]/3
        x[:,1] = (x[:,1]+1)/3
        return x.reshape(-1,72)