# Report

## The learning algorithm

The basics of this algorithm is described in  

The start values for the hyperparameters were taken from a similar project. 
---
epsilon_start = 1.0  
epsilon_end = 0.001  
epsilon_decay = 0.9995  
  
replay buffer size = 1000000  
minibatch size = 64  
Gamma = 0.99  
Tau = 0.001  
 

The neural network
---


## Result and plots

 

<img src="" width="480" height="270" />

## Untrained vs trained agent

| <img src="https://github.com/SibHusky/DDPG-Reacher-ContinuousControl/blob/master/gifs/Reacher_untrained.gif" width="480" height="270" /> | <img src="https://github.com/SibHusky/DDPG-Reacher-ContinuousControl/blob/master/gifs/Reacher_trained.gif" width="480" height="270" />  |
|---|---|

## Ideas for the future work
- intensive hyperparameter tuning
