import gym
import numpy as np
#from gym import spaces
#from gym.utils import seeding


class DiceGame(gym.Env):

    def __init__(self):
        self.state = np.zeros((7,3))
        self.top = [1000,6,6,6,6,6,6] #Arb top for Col 0, High so it doesn't Accidentally Trigger Col Done Count
        self.dice = (np.random.randint(1, 7),np.random.randint(1, 7),np.random.randint(1, 7))
        self.state[0] = self.dice
        self.blackDots = 2
        self.turn = 0 #Total Turns, or how many times opponent had a chance to counter attack
        self.round = 0 #Rounds within a current turn, used to track reward
        self.reward = 0
        self.bust = False
        self.done = False
        
    def step(self, action):
        if self.done:
            return self.state, self.dice, self.blackDots, self.turn, 0, self.done
        else:
            #assert self.action_space.contains(action)
            assert action in [0,1,2,3,4,5]
            # 0 is dice 1 and stay
            # 1 is dice 1 and go
            # 2 is dice 2 and stay
            # 3 is dice 2 and go
            # 4 is dice 3 and stay
            # 5 is dice 3 and go
            dicePick = self.dice[action//2] #Numerical Value of Dice Picked
            stay = (action%2 == 0) #Stay or push value

            #Code for checking if move is legal because top has been reached previously
            #in either Black or Colors
            if any (X >= self.top[dicePick] for X in env.state[dicePick]):
                self.bust=True

            #Code for checking if move is illegal due to out of black dots and attempting to place another
            if env.state[dicePick][2]==0 and self.blackDots<=0:
                self.bust=True

            #Bust, Reset all Black Dots to 0 and increase Turn. Reset and set what is needed for next round
            if self.bust:
                for i in range(len(env.state)):
                    env.state[i,2]=0
                self.turn+=1
                self.blackDots=2
                self.bust=False
                self.reward=(-1)*self.round
                self.round=0
                self.dice = (np.random.randint(1, 7),np.random.randint(1, 7),np.random.randint(1, 7))
                self.state[0] = self.dice

            #Increase picked value. Decrease BlackDot count if needed
            else:
                #If new blackdot Placement, initialize blackdot
                if self.state[dicePick][2]==0:
                    self.state[dicePick][2]=self.state[dicePick][0]
                    self.blackDots-=1            
                self.state[dicePick][2]+=1
                self.round+=1
                self.reward=0
                self.dice = (np.random.randint(1, 7),np.random.randint(1, 7),np.random.randint(1, 7))
                self.state[0] = self.dice

                #If stay also chosen, increase turn count, lock in and reset blackDots, reset BD count
                if stay:
                    for i in range(1,7):
                        if env.state[i][2]>0:
                            env.state[i][0]=env.state[i][2] 
                            env.state[i][2]=0
                    self.turn+=1
                    self.blackDots=2
                    self.bust=False
                    self.reward=(self.round-1)
                    self.round=0
                    
                    countDone=0
                    for i in range(1,7):
                        if env.state[i][0]>=self.top[i]:
                            countDone+=1
                    if (countDone>=3):
                        self.done = True
                        self.reward = 1000#/self.turn #Arb Reward for completing Game
                

            return self.state, self.dice, self.blackDots, self.turn, self.reward, self.done
        
    def softreset(self):
        self.turn+=1
        self.blackDots=2
        self.bust=False
        self.round=0

    def reset(self):
        self.state = np.zeros((7,3))
        self.top = [1000,6,6,6,6,6,6]
        self.dice = (np.random.randint(1, 7),np.random.randint(1, 7),np.random.randint(1, 7))
        self.state[0] = self.dice
        self.blackDots = 2
        self.turn = 0
        self.round = 0
        self.reward = 0
        self.bust = False
        self.done = False
        return self.state, self.dice, self.blackDots, self.turn, self.reward, self.done