import numpy as np
import random
import copy
from collections import namedtuple, deque

from actor_critic_DNN import Actor, Critic

import torch
import torch.nn.functional as F
import torch.optim as optim



device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

class OUNoise:
    """Ornstein-Uhlenbeck process."""

    def __init__(self, size, seed, mu=0., theta=0.15, sigma=0.05):
        """
        Initialize parameters and noise process.
        """
        self.mu = mu * np.ones(size)
        self.theta = theta
        self.sigma = sigma
        random.seed(seed)
        self.reset()

    def reset(self):
        """Reset the internal state (= noise) to mean (mu)."""
        self.state = copy.copy(self.mu)

    def sample(self):
        """Update internal state and return it as a noise sample."""
        x = self.state
        dx = self.theta * (self.mu - x) + self.sigma * np.array([random.random() for i in range(len(x))])
        self.state = x + dx
        return self.state
		
class ReplayBuffer:
    """
    Fixed-size Buffer for the experience tuples
    """

    def __init__(self, buffer_size, batch_size, seed):
        """Initialize a ReplayBuffer object.
        Params
        ======
            buffer_size (int): maximum size of buffer
            batch_size (int): size of each training batch
            random_seed (int): random seed
        """
		
        self.rb = deque(maxlen=buffer_size)  # internal memory (deque)
        self.batch_size = batch_size
        self.experience = namedtuple("Experience", field_names=["state", "action", "reward", "next_state", "done"])
        random.seed(seed)
    
    def add(self,state,action,reward,next_state,done):
        """Add a new experience tuple to the ring buffer"""
        single_expi = self.experience(state,action,reward,next_state,done)
        self.rb.append(single_expi)
    
    def sample(self):
        """Randomly sample a batch of experiences from memory."""
        experiences = random.sample(self.rb, k=self.batch_size)

        states = torch.from_numpy(np.vstack([e.state for e in experiences if e is not None])).float().to(device)
        actions = torch.from_numpy(np.vstack([e.action for e in experiences if e is not None])).float().to(device)
        rewards = torch.from_numpy(np.vstack([e.reward for e in experiences if e is not None])).float().to(device)
        next_states = torch.from_numpy(np.vstack([e.next_state for e in experiences if e is not None])).float().to(device)
        dones = torch.from_numpy(np.vstack([e.done for e in experiences if e is not None]).astype(np.uint8)).float().to(device)
        #torch_done = torch.from_numpy(np.vstack([1 if e.done == True else 0 for e in experience if e is not None])).float().to(device)

        return (states, actions, rewards, next_states, dones)

    def __len__(self):
        """Return the current size of internal memory."""
        return len(self.rb)


class Agent():
    """
    The Agent interacts with the environment and learns from the interactions and the environment
    """
    def __init__(self, state_size, action_size, buffer_size, batch_size, gamma, tau, lr_actor, lr_critic, \
        weight_decay, epsilon_decay, update_every, update_times, random_seed = 23, epsilon = 1.0):
        """
        Parameters
        ==========
            state_size (in): dimension of each state
            action_size (int): dimension of each action
            random_seed (int): random seed
            epsilon (int): start value of epsilon, default 1.0
            buffer_size (int): size of the memorybuffer
            batch_size (int): size of the batch
            gamma (float): discounted value, must be between 0 and 1
            tau (float): blend parameter for the soft update, has to be between 0 and 1
            lr_actor (float): learning rate for the actor dnn
            lr_critic (float): learning rate for the critic dnn
            weight_decay (float): L2 penalty
            epsilon_decay (float): factor to reduce epsilon frequently
            update_every (int): update frequence
            update_times (int): how many times the weights should be updated at one update step

        """
        self.state_size = state_size
        self.action_size = action_size
        self.seed = random.seed(random_seed)
        self.random_seed = random_seed
        self.epsilon = epsilon
        self.buffer_size = buffer_size
        self.batch_size = batch_size
        self.gamma = gamma
        self.tau = tau
        self.lr_actor = lr_actor
        self.lr_critic = lr_critic
        self.weight_decay = weight_decay
        self.epsilon_decay = epsilon_decay
        self.update_every = update_every
        self.update_times = update_times

        self.update_every_x = 0

        # The Actor
        ###########
        self.actor_local  = Actor(self.state_size, self.action_size, self.random_seed).to(device)
        self.actor_target = Actor(self.state_size, self.action_size, self.random_seed).to(device)
        self.actor_optimizer = optim.Adam(self.actor_local.parameters(), lr = self.lr_actor)

        # The Critic
        ############
        self.critic_local = Critic(self.state_size, self.action_size, self.random_seed).to(device)
        self.critic_target = Critic(self.state_size, self.action_size, self.random_seed).to(device)
        self.critic_optimizer = optim.Adam(self.critic_local.parameters(), lr = self.lr_critic, weight_decay = self.weight_decay)

        # for target_param, param in zip(self.actor_target.parameters(), self.actor_local.parameters()):
        #     target_param.data.copy_(param.data)
        # for target_param, param in zip(self.critic_target.parameters(), self.critic_local.parameters()):
        #     target_param.data.copy_(param.data)
            
        # The Replay Buffer
        ###################
        self.RepMem = ReplayBuffer(self.buffer_size, self.batch_size, self.random_seed)

        # The "Ornstein-Uhlenbeck-Noise"
        ################################
        self.noise = OUNoise(self.action_size, self.random_seed)

    def step(self, state, action, reward, next_state, done):
        """
        add info to the ringbuffer, if enough entries are available --> learn
        """
        self.RepMem.add(state, action, reward, next_state, done)
        #print("Length buffer: " + str(len(self.RepMem)))
        self.update_every_x = (self.update_every_x+1) % self.update_every
        if self.update_every_x == 0:
            # start learning when buffer is half-full
            if len(self.RepMem) > int(self.buffer_size/2):
                for _ in range(int(self.update_times)):
                    sample_batch = self.RepMem.sample()
                    #print (sample_batch)
                    #print("----------")
                    self.learn(sample_batch)
                    #print ("Learned")
                    #print ("++++++++++")
        


    def act(self, state, add_noise = True):
        """
        choose an action due to the given state and policy
        Parameters:
        ===========
        state: the current state
        add_noise (bool): True: adds a noise for exploration
        
        return: the estimate action
        """
        ### adapt state and send it to device
        state = torch.from_numpy(state).float().to(device)
        self.actor_local.eval()
        with torch.no_grad():
            action = self.actor_local(state).cpu().data.numpy()
        self.actor_local.train()
        if add_noise:
            noise_ = self.noise.sample()
            #print (action)
            action += self.epsilon * noise_
            #print (action)
            #print ("------------------------------------------")
        ### be shure that with the noise the action is still between -1 and 1  
        return np.clip(action, -1.0, 1.0)

    def get_epsilon(self):
        """
        getter function: used to monitor epsilon
        """
        return self.epsilon

    def learn(self, experiences):
        """
        update the DNNs
        Parameters:
        ==========
        experiences: batch sample 
        """
        states, actions, rewards, next_states, dones = experiences

        # ---------------------------- update critic ---------------------------- #
        # Get predicted next-state actions and Q values from target models
        actions_next = self.actor_target(next_states)
        Q_targets_next = self.critic_target(next_states, actions_next)
        # Compute Q targets for current states (y_i)
        Q_targets = rewards + (self.gamma * Q_targets_next * (1 - dones))
        # Compute critic loss
        Q_expected = self.critic_local(states, actions)
        critic_loss = F.mse_loss(Q_expected, Q_targets)
        # Minimize the loss
        self.critic_optimizer.zero_grad()
        critic_loss.backward()
        self.critic_optimizer.step()

        # ---------------------------- update actor ---------------------------- #
        # Compute actor loss
        actions_pred = self.actor_local(states)
        actor_loss = -self.critic_local(states, actions_pred).mean()
        # Minimize the loss
        self.actor_optimizer.zero_grad()
        actor_loss.backward()
        self.actor_optimizer.step()

        # ----------------------- update target networks ----------------------- #
        self.soft_update(self.critic_local, self.critic_target, self.tau)
        self.soft_update(self.actor_local, self.actor_target, self.tau)  

        self.epsilon = max(0.001, self.epsilon * self.epsilon_decay)
        self.noise.reset()



    def soft_update(self, local_model, target_model, tau):
        """
        θ_target = τ*θ_local + (1 - τ)*θ_target
        Parameters
        ==========
        local_model (Actor or Critic object): from that model the parameters are used
        target_model (Actor or Critic object): to that model the parameters are updated 
        tau (float): blend parameter, has to be between 0 and 1
        """
        for target_param, local_param in zip(target_model.parameters(), local_model.parameters()):
            target_param.data.copy_(tau*local_param.data + (1.0-tau)*target_param.data)

    def reset(self):
        self.noise.reset()







if __name__ == "__main__":
    test = Agent(3,4,5)
    test.reset()