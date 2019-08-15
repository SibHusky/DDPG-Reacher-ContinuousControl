# DDPG-Reacher-ContinuousControl
Agent for solving the Unity "Reacher" Environment

## Introduction
This is all about a Reinforcement Learning problem. A double-jointed must move its hand to the goal location and keep it there. For each step the agent's hand is in the goal location a reward of +0.1 is earned.
To solve the environment the agent must get an average score of +30 over 100 consecutive episodes.

## Setting up the environment 
This project requires a python version 3.6 or higher.

It is recommanded to create a new python environment. Therefore you may follow the steps described here https://github.com/udacity/deep-reinforcement-learning#dependencies.

After creating the python environment the following packages must be installed:
 - torch 0.4.0
 - numpy 1.14.5
 - matplotlib 3.1.0
 - unityagents 0.3.0

#### How to install unityagents
An installation manual for Windows (contains also links for Linux - installation)  
https://github.com/reinforcement-learning-kr/pg_travel/wiki/Installing-Unity-ml-agents-on-Windows

## The Environment
The environment is an adpated version of https://www.youtube.com/watch?v=bhsVB0QKvoQ and is a project of the Udacity Deep Reinforcement Learning nanodegree. The Reacher_Windows_x86_64.zip file offers this environment.
More informations: https://github.com/Unity-Technologies/ml-agents/blob/master/docs/Learning-Environment-Examples.md

## Getting started
Follow the instruction in the jupyter notebook Continuous_Control.ipynb.
