# Report

## The learning algorithm

The basics of this algorithm is described in https://arxiv.org/pdf/1509.02971.pdf

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

Episode 100  	Average100  Score: 0.11	Score: 0.00  
Episode 200  	Average100 Score: 0.10	Score: 0.00  
Episode 300  	Average100 Score: 0.14	Score: 0.00  
Episode 400  	Average100 Score: 0.16	Score: 1.17  
Episode 500  	Average100 Score: 0.18	Score: 0.00  
Episode 600  	Average100 Score: 0.90	Score: 1.37  
Episode 700  	Average100 Score: 1.88	Score: 2.83  
Episode 800  	Average100 Score: 3.85	Score: 4.21  
Episode 900	  Average100 Score: 6.12	Score: 5.68  
Episode 1000	Average100 Score: 6.82	Score: 1.52  
Episode 1100	Average100 Score: 7.26	Score: 7.25  
Episode 1200	Average100 Score: 7.46	Score: 12.42  
Episode 1300	Average100 Score: 8.19	Score: 8.09  
Episode 1400	Average100 Score: 8.34	Score: 13.12  
Episode 1500	Average100 Score: 8.17	Score: 8.54  
Episode 1600	Average100 Score: 8.34	Score: 5.68  
Episode 1700	Average100 Score: 10.50	Score: 12.22  
Episode 1800	Average100 Score: 12.23	Score: 19.88  
Episode 1900	Average100 Score: 12.65	Score: 14.54  
Episode 2000	Average100 Score: 13.94	Score: 7.89  
Episode 2100	Average100 Score: 14.23	Score: 11.00  
Episode 2200	Average100 Score: 14.52	Score: 13.65  
Episode 2300	Average100 Score: 15.29	Score: 13.55  
Episode 2400	Average100 Score: 17.08	Score: 17.28  
Episode 2500	Average100 Score: 18.20	Score: 10.92  
Episode 2600	Average100 Score: 17.90	Score: 17.91  
Episode 2700	Average100 Score: 20.05	Score: 22.55  
Episode 2800	Average100 Score: 19.95	Score: 15.07  
Episode 2900	Average100 Score: 22.48	Score: 22.10  
Episode 3000	Average100 Score: 22.43	Score: 33.57  
Episode 3100	Average100 Score: 24.27	Score: 23.81  
Episode 3200	Average100 Score: 26.16	Score: 24.98  
Episode 3300	Average100 Score: 26.95	Score: 39.64  
Episode 3400	Average100 Score: 26.13	Score: 33.75  
Episode 3500	Average100 Score: 25.51	Score: 26.91  
Episode 3600	Average100 Score: 29.13	Score: 30.12  
Episode 3626	Average100 Score: 30.00	Score: 26.37  
Environment solved! 	Average100 Score: 30.00	Episodes: 3626

 

<img src="https://github.com/SibHusky/DDPG-Reacher-ContinuousControl/blob/master/result_plot.png" width="480" height="270" />

## Untrained vs trained agent

| <img src="https://github.com/SibHusky/DDPG-Reacher-ContinuousControl/blob/master/gifs/Reacher_untrained.gif" width="480" height="270" /> | <img src="https://github.com/SibHusky/DDPG-Reacher-ContinuousControl/blob/master/gifs/Reacher_trained.gif" width="480" height="270" />  |
|---|---|

## Ideas for the future work
- intensive hyperparameter tuning
  (especially the epsilon_decay parameter --> dealing with the Ornstein-Uhlenbeck noise)
- try D4PG
- switch to the environment with 20 reacher and check out A3C/A2C
  
