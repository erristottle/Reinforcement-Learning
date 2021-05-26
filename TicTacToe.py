from __future__ import print_function, division
from builtins import range
# Note: you may need to update your version of future
# sudo pip install -U future


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random


NUM_TRIALS = 500000


winners = []


class new_board:
  
  def __init__(self):
    # p: the win rate
    self.state = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    


class player:
    
  def __init__(self, new_id, epsilon):
      self.playerid = new_id
      self.eps = epsilon
      self.pestimates = {}
      self.state_counts = {}
      self.state_memory = []
      self.move_memory = []
      self.num_times_explored = 0
      self.num_times_exploited = 0
      self.num_wins = 0

      

    
  def readboard(self, state):
      
      #Store current state
      state_string = "".join(str(x) for x in state)
      self.state_memory.append(state_string)
      
      
      
  
  def choosemove(self):
      
      #Split state into list
      state_string = self.state_memory[-1]
      state = [int(char) for char in state_string]
      
      #Determine available spaces
      free_spaces = [i for i, x in enumerate(state) if x == 0]
      
      EPS = self.eps

      
      #Explore
      if np.random.random()<EPS:
          #Make choice
          choice = random.choice(free_spaces)
          
          self.num_times_explored += 1


      #Exploit
      else:
                    
          try:
              a = np.argsort(self.pestimates[state_string], axis=-1, kind='quicksort', order=None)
              for j in range(len(a)):
                  choice = a[-(j+1)]
                  if int(state_string[choice])==0:
                      self.num_times_exploited += 1
                      break
                  
              #If you've seen this state  before
              # choice = np.argmax(self.pestimates[state_string])

          except:
              
              choice = random.choice(free_spaces)
              self.num_times_explored += 1

      
      #Store choice
      self.move_memory.append(choice)
      
      #Make move
      state[choice] = self.playerid
      
      #Return state
      return state
      # state_string = str(state)
      # return str(state_string)
  
  def updateestimates(self, winner):
      
      if winner == self.playerid:
          reward = 1
      elif winner == "None":
          reward = 0
      else:
          reward = -1
      for i in range(len(self.state_memory)):
          try:
              len(self.pestimates[self.state_memory[i]])
              self.state_counts[self.state_memory[i]][self.move_memory[i]] += 1
              self.pestimates[self.state_memory[i]][self.move_memory[i]] = self.pestimates[self.state_memory[i]][self.move_memory[i]] + (1/self.state_counts[self.state_memory[i]][self.move_memory[i]])*(reward - self.pestimates[self.state_memory[i]][self.move_memory[i]])
          except:
              self.pestimates[self.state_memory[i]] = [0, 0, 0, 0, 0, 0, 0, 0, 0]
              self.pestimates[self.state_memory[i]][self.move_memory[i]] = reward
              
              self.state_counts[self.state_memory[i]] = [0, 0, 0, 0, 0, 0, 0, 0, 0]
              self.state_counts[self.state_memory[i]][self.move_memory[i]] = 1

      
      self.state_memory = []
      self.move_memory = []

  def countWins(self, result):
      if result == self.playerid:
          self.num_wins += 1
      
            

  
def gameover(board):
      winner = np.nan
      
      if (board.state[0] == board.state[1]) & (board.state[1] == board.state[2]) & (board.state[0]!=0):
          winner = board.state[0]
          
      elif (board.state[3] == board.state[4]) & (board.state[4] == board.state[5]) & (board.state[3]!=0):
          winner = board.state[3]
          
      elif (board.state[6] == board.state[7]) & (board.state[7] == board.state[8]) & (board.state[6]!=0):
          winner = board.state[6]
          
      elif (board.state[0] == board.state[3]) & (board.state[3] == board.state[6]) & (board.state[0]!=0):
          winner = board.state[0]
          
      elif (board.state[1] == board.state[4]) & (board.state[4] == board.state[7]) & (board.state[1]!=0):
          winner = board.state[1]
          
      elif (board.state[2] == board.state[5]) & (board.state[5] == board.state[8]) & (board.state[2]!=0):
          winner = board.state[2]
          
      elif (board.state[0] == board.state[4]) & (board.state[4] == board.state[8]) & (board.state[0]!=0):
          winner = board.state[0]
          
      elif (board.state[2] == board.state[4]) & (board.state[4] == board.state[6]) & (board.state[2]!=0):
          winner = board.state[2]
          
      elif (board.state[0] != 0) & (board.state[1] != 0) & (board.state[2] != 0) & (board.state[3] != 0) & (board.state[4] != 0) & (board.state[5] != 0) & (board.state[6] != 0) & (board.state[7] != 0) & (board.state[8] != 0):
          winner = "None"
          
      if ~pd.isna(winner)==-1:
          return winner
      else:
          return 0
          

# def experiment():
#Create players
player1 = player(1, 0.1)
player2 = player(2, 0.2)

#Play games
for i in range(NUM_TRIALS):

    board = new_board()

    if i%2==0:
        count = 0
    else:
        count = 1
    while(gameover(board)==0):
        if count%2==0:
            player1.readboard(board.state)
            board.state = player1.choosemove()
        else:
            player2.readboard(board.state)
            board.state = player2.choosemove()
            
        count += 1
 
    result = gameover(board)       
    winners.append(result)
    player1.countWins(result)
    player2.countWins(result)           
    player1.updateestimates(result)
    player2.updateestimates(result)
    
    # print("Trial", i, "Winner", result)        
        

print("Player 1 win rate:", len([x for x in winners if x==1])/len(winners))
print("Player 2 win rate:", len([x for x in winners if x==2])/len(winners))    
print("Tie rate:", len([x for x in winners if x=="None"])/len(winners))  


print("Player 1 num_times_explored:", player1.num_times_explored)
print("Player 1 num_times_exploited:", player1.num_times_exploited) 

print("Player 2 num_times_explored:", player2.num_times_explored)
print("Player 2 num_times_exploited:", player2.num_times_exploited)

print("Player 1 scenarios seen", len(player1.pestimates.keys()))
print("Player 2 scenarios seen", len(player2.pestimates.keys()))

player2wins = [0 if x != 2 else 1 for x in winners]
  # # plot the results
cumulative_rewards = list(np.cumsum(player2wins))
  # win_rates = cumulative_rewards / (np.arange(NUM_TRIALS) + 1)
  # plt.plot(win_rates)
  # plt.plot(np.ones(NUM_TRIALS)*np.max(BANDIT_PROBABILITIES))
  # plt.show()

# if __name__ == "__main__":
#   experiment()

def play_game(playerid, epsilon):
    count = 0
    new_game = 'yes'
    while(new_game=='yes'):
        if playerid==1:
            player=player1
            cpu_id = 2
        else:
            player=player2
            cpu_id = 1
        #Play a game
        board = new_board()
        player.eps=epsilon
        while(gameover(board)==0):
                if count%2==0:
                    iii=0
                    state = board.state
                    print(state[:3])
                    print(state[3:6])
                    print(state[6:])
                    print("Choose move:")
                    move = input()
                    while(iii<1000):
                        if  (int(move)<=8):
                            if state[int(move)]==0:
                                break
                            else:
                                print(move, "is already taken. Choose again:")
                                move = input()
                        else:
                            print(move, "is not a valid choice. Choose again:")
                            move = input()
                    state[int(move)] = cpu_id
                    board.state = state
                else:
                    player.readboard(board.state)
                    board.state = player.choosemove()
                    
                count += 1
        result = gameover(board)       
        winners.append(result)            
        player.updateestimates(result)
        state = board.state
        print(state[:3])
        print(state[3:6])
        print(state[6:])       
        print("Winner:", gameover(board))
        print("Play again?")
        new_game = input()
    
if __name__ == "__main__":
    if player1.num_wins>= player2.num_wins:
        play_game(1, 0)
    else:
        play_game(2, 0)
  