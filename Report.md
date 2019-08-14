# Report

## The learning algorithm

The basics of this algorithm is described in  

The start values for the hyperparameters were taken from a similar project. 
---
EPSILON = 1.0  (strictly speaking no hyperparameter, hard coded)  
EPSILON_END = 0.001  (strictly speaking no hyperparameter, hard coded)  
EPSILON_DECAY = 0.99999    
  
buffer size = 1000000  
batch_size = 265  
Gamma = 0.99  
Tau = 0.001  

UPDATE_EVERY = 100 (Learning frequence, in that case: the learning process runs every 100 timesteps)  
UPDATE_TIMES = 10 (how often the weights are updated by the learning process)  
(The learning starts when the memory buffer is half-full)  
 

The neural networks
---
The state is represented as vector. So a vanilla DNN is used.
Both networks use an Adam optimizer with a learning rate of 0.001.

The actor:
- batch normalization layer
- full connected layer 1: 33  --> 128 + relu activation function
  (33 is the size of the state vector)
- batch normalization layer
- full connected layer 2: 128 --> 128 + relu activation function
- batch normalization layer
- full connected layer 3: 128 --> 4 + tanh activation function
  (4 is the size of the action vector)
  

The critic:
- batch normalization layer
- full connected layer 1: 33 --> 128 + relu activation function
- full connected layer 2: 128 + 4 --> 128 + relu activation function
  (in this layer the actions are added. that's why +4)
- full connected layer 3: 128 --> 1



## Result and plots

Episode 100  	Average100 Score: 0.11	Score: 0.00	
Episode 200  	Average100 Score: 0.10	Score: 0.00	
Episode 300	  Average100 Score: 0.14	Score: 0.00	
Episode 400	  Average100 Score: 0.16	Score: 1.17	
Episode 500  	Average100 Score: 0.18	Score: 0.12	
Episode 600	  Average100 Score: 0.56	Score: 0.59	
Episode 700	  Average100 Score: 1.06	Score: 2.09	
Episode 800  	Average100 Score: 1.67	Score: 1.75	
Episode 900	  Average100 Score: 3.44	Score: 2.80	
Episode 1000	Average100 Score: 4.69	Score: 4.36	
Episode 1100	Average100 Score: 5.70	Score: 6.06	
Episode 1200	Average100 Score: 6.31	Score: 7.88	
Episode 1300	Average100 Score: 6.58	Score: 5.63	
Episode 1400	Average100 Score: 8.61	Score: 11.64
Episode 1500	Average100 Score: 8.99	Score: 6.15	
Episode 1600	Average100 Score: 7.07	Score: 6.10	
Episode 1700	Average100 Score: 8.84	Score: 9.57	
Episode 1800	Average100 Score: 8.76	Score: 21.59
Episode 1900	Average100 Score: 12.16	Score: 20.66
Episode 2000	Average100 Score: 16.84	Score: 20.17
Episode 2100	Average100 Score: 16.45	Score: 11.29
Episode 2200	Average100 Score: 16.47	Score: 8.43	
Episode 2300	Average100 Score: 19.09	Score: 14.95
Episode 2400	Average100 Score: 22.91	Score: 31.40
Episode 2500	Average100 Score: 24.69	Score: 29.30
Episode 2600	Average100 Score: 25.22	Score: 30.80
Episode 2700	Average100 Score: 28.18	Score: 29.29
Episode 2800	Average100 Score: 27.01	Score: 16.76
Episode 2900	Average100 Score: 28.20	Score: 28.40
Episode 3000	Average100 Score: 28.92	Score: 29.29
Episode 3100	Average100 Score: 28.95	Score: 26.32
Episode 3146	Average100 Score: 30.01	Score: 36.03
Environment solved! 	Average100 Score: 30.01
 

<img src="https://github.com/SibHusky/DDPG-Reacher-ContinuousControl/blob/master/result_plot.png" width="480" height="270" />

## Untrained vs trained agent

| <img src="https://github.com/SibHusky/DDPG-Reacher-ContinuousControl/blob/master/gifs/Reacher_untrained.gif" width="480" height="270" /> | <img src="https://github.com/SibHusky/DDPG-Reacher-ContinuousControl/blob/master/gifs/Reacher_trained.gif" width="480" height="270" />  |
|---|---|

## Ideas for the future work
- intensive hyperparameter tuning
