import numpy as np
from funcions_matrius import *

N = 3
M = 3

class GAME:
    def __init__(self):
        self.win = matriu_guanyadora(N,M)
        
        self.taulell = matriu_random(N, M)

        self.pos_0 = trobar_zero(self.taulell)

    def guanyat(self):
        for i in range(N):
            for j in range(M):
                if self.win[i,j] != self.taulell[i,j]: return False
        
        return True

    """
    (-1,0)  -> 0 cap a dalt
    (1,0) -> 0 cap a baix
    (0,1)  -> 0 cap a dreta
    (0,-1) -> 0 cap a esquerra    
    """

    def is_valid_move(self, move):
        if (self.pos_0[0] + move[0] < 0 or self.pos_0[1]+move[1] < 0): return False
        if (self.pos_0[0] + move[0] > N-1 or self.pos_0[1]+move[1] > M-1): return False
        return True

    def move (self, move):  # el moviment es vàlid
        self.taulell[self.pos_0[0], self.pos_0[1]], self.taulell[self.pos_0[0] + move[0], self.pos_0[1] + move[1]] = self.taulell[self.pos_0[0] + move[0], self.pos_0[1] + move[1]], self.taulell[self.pos_0[0], self.pos_0[1]]
        self.pos_0[0] += move[0]
        self.pos_0[1] += move[1]




def main():
    game = GAME()
    
    print("Taulell:")
    print(game.taulell)

    while(not game.guanyat()):
        user = input("introdueix moviment(wasd): ")

        move = [0,0]
        if (user == "w"): move = [-1,0]
        elif (user == "s"): move = [1,0]
        elif (user == "a"): move = [0,-1]
        elif (user == "d"): move = [0,1]

        if (game.is_valid_move(move)):
            game.move(move)
        else:
            print("Invalid!")

        print("Taulell:")
        print(game.taulell)

    print("has guanyat")


if __name__ == "__main__":
    main()