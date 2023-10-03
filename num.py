import numpy as np
from funcions_matrius import matriu_random, matriu_guanyadora, trobar_zero
import math
import random
import matplotlib.pyplot as plt

N = 1
M = 2

def __codificacio__(taulell):
    taulell = taulell.reshape(N*M)
    index = 0
    aux = np.arange(N*M)
    for i in range(N*M):
        index += math.factorial(N*M-i-1) * aux[taulell[i]]
        aux[taulell[i]:] -= np.ones(N*M-taulell[i], dtype=int)

    return index

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
            return q_table[__codificacio__(estat)].argmax()


    


class GAME:
    def __init__(self):
        self.win = matriu_guanyadora(N, M)
        
        self.taulell_ini = matriu_random(N, M)
        
        self.taulell = self.taulell_ini.copy()

        self.pos_0 = trobar_zero(self.taulell)
        
        self.n_accions = 4
        
        self.accions = [[-1,0],[1,0],[0,-1],[0,1]]
        
        self.n_estats = math.factorial(N*M)
        
        self.q_table = np.zeros((self.n_estats, self.n_accions))

    def guanyat(self):
        for i in range(N):
            for j in range(M):
                if self.win[i,j] != self.taulell[i,j]: return False
        
        return True
    
    def reset(self):
        self.taulell = self.taulell_ini.copy()
        return

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

    def actualitzar_q_table(self, move, alpha, gamma, agent):
        if not self.is_valid_move(self.accions[move]):
            nou_estat = self.taulell
            recompensa = -10
        else: 
            nou_estat, recompensa = self.prendre_nou_estat(self.accions[move])
        nova_accio = agent.seleccionar_accio(nou_estat, self.q_table)
        self.q_table[__codificacio__(self.taulell), move] = alpha*(recompensa + gamma*self.q_table[__codificacio__(nou_estat), nova_accio] - self.q_table[__codificacio__(self.taulell), move])

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
            game.prendre_nou_estat(move)
        else:
            print("Invalid!")

        print("Taulell:")
        print(game.taulell)

    print("has guanyat")

def main2():

    n_episodes = 10000
    max_iter = 20

    alpha = 0.5
    gamma = 1
    epsilon = 0.1

    estrategia = ESTRATEGIA_EXPL(1, 0.05, epsilon)
    game = GAME()
    agent = AGENT(estrategia, game.n_accions)
    pasos = []

    for i in range(n_episodes):
        iter = 0
        game.reset()
        while(not game.guanyat() and iter < max_iter):
            accio = agent.seleccionar_accio(game.taulell, game.q_table)
            game.actualitzar_q_table(accio, alpha, gamma, agent)
            iter += 1
        print(f"Episode: {i}, Moviments: {iter}")
        pasos.append(iter)
    
    plt.plot(pasos)
    print(f"Min pasos: {min(pasos)}")
    
main2()