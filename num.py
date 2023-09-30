import numpy as np
from funcions_matrius import *
import math
import random

N=3


def __codificacio__(taulell):
    taulell = taulell.reshape(9,1)
    print(taulell.shape)
    index = 0
    aux = [0,1,2,3,4,5,6,7,8]
    for i in range(9):
        index += math.factorial(8-i) * (aux[int(taulell[i])])
        aux[int(taulell[i]):] -= np.ones(9-int(taulell[i]))

    return int(index)

class ESTRATEGIA_EXPL():
    def __init__(self, inici, final, caiguda):
        self.inici = inici
        self.final = final
        self.caiguda = caiguda

    def act_rati_expl(self, pas_actual):
        return self.final + (self.inici - self.final)  * math.exp(-1 * pas_actual * self.caiguda)

class AGENT:
    def __init__(self, estrategia, n_accions):
        self.pas_actual = 0
        self.estrategia = estrategia
        self.n_accions = n_accions
    
    def seleccionar_accio(self, estat, q_table):
        rati = self.estrategia.act_rati_expl(self.pas_actual)
        self.pas_actual += 1

        if rati > random.random():
            return random.randrange(self.n_accions)
        else:
            return q_table(self.__codificacio__(estat)).argmax(dim=1)


    


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

    def prendre_nou_estat(self, move):  # el moviment es vàlid
        self.taulell[self.pos_0[0], self.pos_0[1]], self.taulell[self.pos_0[0] + move[0], self.pos_0[1] + move[1]] = self.taulell[self.pos_0[0] + move[0], self.pos_0[1] + move[1]], self.taulell[self.pos_0[0], self.pos_0[1]]
        self.pos_0[0] += move[0]
        self.pos_0[1] += move[1]
        return self.taulell, -1

    def actualitzar_q_table(self, move, q_table, alpha, gamma, agent):
        if not self.is_valid_move(move):
            nou_estat = self.taulell
            recompensa = -10
        else: 
            nou_estat, recompensa = self.prendre_nou_estat(move)
        nova_accio = agent.seleccionar_accio(nou_estat)
        q_table[__codificacio__(self.taulell), move] = alpha*(recompensa + gamma*q_table[nou_estat, nova_accio] - q_table[self.taulell, move])

def main1():
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

def main2():
    n_estats = math.factorial(9)
    n_accions = 4

    q_table = np.zeros((n_estats, n_accions))
    
    n_episodes = 10000
    max_iter = 76
    iter = 0

    alpha = 0.5
    gamma = 1
    epsilon = 0.1

    estrategia = ESTRATEGIA_EXPL(1, 0.05, epsilon)
    game = GAME()
    agent = AGENT(estrategia, n_accions)

    for i in range(n_episodes):
        while(not game.guanyat() and iter < max_iter):
            accio = agent.seleccionar_accio(game.taulell, q_table)
            game.actualitzar_q_table(accio, q_table, alpha, gamma, agent)
            iter += 1


if __name__ == "__main__":
    main2()
