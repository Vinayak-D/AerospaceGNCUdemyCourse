#Training NN test

import torch
import numpy as np
import torch.optim as optim
import matplotlib.pyplot as plt
import pandas as pd
import copy

#Random seed
torch.manual_seed(0)

#Get training data
rawData = pd.read_csv('data.csv')
nRows = rawData.shape[0]

nTrain = 150

X_train = np.zeros((nTrain, 2))
Y_train = np.zeros((nTrain, 1))

for i in range(0, nTrain-1):
    curr_row = rawData.loc[i]
    if i == 0:
        #One timestep prior
        prev_row = copy.deepcopy(curr_row)
        #Initialize control error to 0
        prev_row.iloc[0] = 0
    else:    
        prev_row = rawData.loc[i-1]
    #inputs (error[t] and error[t-1])
    X_train[i][0] = curr_row.iloc[0]
    X_train[i][1] = prev_row.iloc[0]
    #outputs (U: unsaturated control signal)
    Y_train[i][0] = curr_row.iloc[1]
    
#neural network: n inputs, m outputs
model = torch.nn.Sequential(
    #first layer w/ and ReLU activation
    torch.nn.Linear(2,5),
    torch.nn.ReLU(),
    #second layer same as first
    torch.nn.Linear(5,5), 
    torch.nn.ReLU(),
    #last layer, linear
    torch.nn.Linear(5,1)
    )

plt.subplot(3,1,1)
plt.plot(Y_train[:,0][0:-1])
plt.xlabel('Timestep (k)')
plt.ylabel(r'U: $\delta_{elev} (rad)$')
plt.title('Training Data')

print("Parameters: ", model)
    
all_inputs = torch.tensor(X_train, dtype=torch.float32)    
all_outputs = torch.tensor(Y_train, dtype=torch.float32)

loss_fn = torch.nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr = 0.01)

#experiment with this: default = 1000
n_runs = 3

losses = []
n_epochs = []

for epoch in range (n_runs):
    
    #forward pass
    y_pred = model(all_inputs)
    
    #calculate loss: f(predicted, truth)
    loss = loss_fn(y_pred, all_outputs)
    
    #backpropagation
    #first: zero the gradients
    optimizer.zero_grad()
    #next: backpropagate: calculate gradients
    loss.backward()
    
    #using those gradients, update weights
    optimizer.step()
    
    #record data
    n_epochs.append(epoch)
    losses.append(loss.item())   

plt.subplot(3,1,2)
plt.plot(n_epochs, losses)
plt.xlabel('Epoch')
plt.ylabel('Loss (MSE)')
plt.title('Training Runs')

#Inference
temp = np.array([0.00, 0.00])
test_input = torch.tensor(temp, dtype=torch.float32)

output = model(test_input)
print ("Inference: ", model(test_input))

#Testing

A = np.array([[-0.313, 56.7, 0.0], [-0.0139, -0.426, 0.0], [0.0, 56.7, 0.0]])
B = np.array([[0.232], [0.0203], [0.0]])
dT = 0.005

X = np.array([[0.0], [0.0], [0.0]])
U = np.array([0.0])

setpt = 0.75

prev_error = 0.0

output = []
setpoints = []
#default = 6000
nTimesteps = 12000

for i in range (nTimesteps):
    
    setpt = i*0.0005 + 0.5
    if (setpt > 1.25):
        setpt = 1.25
    
    setpoints.append(setpt)
               
    X = X + dT*(A @ X + B * U)
    Y = X[2]
    
    error = setpt - Y[0]
    
    net_in = np.array([error, prev_error])
    net_input = torch.tensor(net_in, dtype=torch.float32)
    
    U = model(net_input).item()
        
    output.append(Y[0])
    
    if U > 1.57:
        U = 1.57
    elif U < -1.57:
        U = -1.57    
        
    #print("e: ", error, ", U: ", U, "  ,Y: ", Y )
    
    prev_error = error
    
plt.subplot(3,1,3)
plt.plot(output)
plt.plot(setpoints)
plt.legend([r'$\theta$',r'$\theta_{des}$'])
plt.xlabel('Timestep (k)')
plt.ylabel(r'$\theta$ (rad)')
plt.title('Inference')

plt.tight_layout()









    




