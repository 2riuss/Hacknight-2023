import numpy as np
import time
from funcions_matrius import matriu_random, matriu_guanyadora, trobar_zero
import math
import random
import matplotlib.pyplot as plt

N = 2
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
    def __init__(self, inici, final, caiguda):  # inici=1, final=0.05, caiguda=epsilon
        self.inici = inici
        self.final = final
        self.caiguda = caiguda

    def act_rati_expl(self, pas_actual):
        return self.final + (self.inici - self.final)  * math.exp(-1 * pas_actual * self.caiguda)
    #   0.05 + (0.95)/e^p/10 ben def

class AGENT:
    def __init__(self, estrategia, n_accions):
        self.pas_actual = 0
        self.estrategia = estrategia
        self.n_accions = n_accions
    
    def seleccionar_accio(self, estat, q_table):
        accio = np.argmax(q_table[__codificacio__(estat)])
        if random.random() < self.estrategia.caiguda:
            accio = random.randint(0, self.n_accions - 1)

        return accio   


class GAME:
    def __init__(self):
        self.win = matriu_guanyadora(N, M)
        
        self.taulell_ini = matriu_random(N, M)
        
        self.taulell = self.taulell_ini.copy()

        self.pos_0 = trobar_zero(self.taulell)
        
        self.n_accions = 4
        
        self.accions = [[-1,0],[1,0],[0,1],[0,-1]]
        
        self.n_estats = math.factorial(N*M)
        
        self.q_table = np.zeros((self.n_estats, self.n_accions))

    def guanyat(self):
        for i in range(N):
            for j in range(M):
                if self.win[i,j] != self.taulell[i,j]: return False
        
        return True
    
    def reset(self):
        self.taulell = self.taulell_ini.copy()
        self.pos_0 = trobar_zero(self.taulell)
        return

    """
    (-1,0)  -> 0 cap a dalt
    (1,0) -> 0 cap a baix
    (0,1)  -> 0 cap a dreta
    (0,-1) -> 0 cap a esquerra    
    """ 

    def is_valid_move(self, move):  # move[baix, dreta]
        if (self.pos_0[0] + move[0] < 0 or self.pos_0[1]+move[1] < 0): return False
        if (self.pos_0[0] + move[0] > N-1 or self.pos_0[1]+move[1] > M-1): return False
        return True

    def prendre_nou_estat(self, move):  # el moviment es vàlid
        self.taulell[self.pos_0[0], self.pos_0[1]], self.taulell[self.pos_0[0] + move[0], self.pos_0[1] + move[1]] = self.taulell[self.pos_0[0] + move[0], self.pos_0[1] + move[1]], self.taulell[self.pos_0[0], self.pos_0[1]]
        self.pos_0[0] += move[0]
        self.pos_0[1] += move[1]
        return self.taulell, -1

    def actualitzar_q_table(self, move, alpha, gamma, agent):
        vell_estat = self.taulell.copy()
        if not self.is_valid_move(self.accions[move]):
            nou_estat = self.taulell
            recompensa = -100
        else:
            nou_estat, recompensa = self.prendre_nou_estat(self.accions[move])  # canvia taulell
        nova_accio = agent.seleccionar_accio(nou_estat, self.q_table)
        self.q_table[__codificacio__(vell_estat), move] = alpha*(recompensa + gamma*(self.q_table[__codificacio__(nou_estat), nova_accio]) - self.q_table[__codificacio__(vell_estat), move])



def juga_pas(game):
    index = np.argmax(game.q_table[__codificacio__(game.taulell)])
    accio = game.accions[index]
    if (not game.is_valid_move(accio)):
        raise Exception("puta ia")
    
    game.prendre_nou_estat(accio)
    

def main1():
    game = GAME()
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

    n_episodes = 100
    max_iter = 50

    alpha = 0.5
    gamma = 1   
    epsilon = 0.1

    estrategia = ESTRATEGIA_EXPL(1, 0.05, epsilon)
    game = GAME()
    agent = AGENT(estrategia, game.n_accions)
    pasos = []

    for i in range(n_episodes):
        iter = 0
        while(not game.guanyat() and iter < max_iter):
            accio = agent.seleccionar_accio(game.taulell, game.q_table)
            game.actualitzar_q_table(accio, alpha, gamma, agent)
            iter += 1
        game.reset()
        print(f"Episode: {i}, Moviments: {iter}") #Taulell: \n {game.taulell}
        pasos.append(iter)
    
    plt.plot(pasos)
    print(f"Min pasos: {min(pasos)}")

    print(game.q_table)
    game.reset()
    
    print("Taulell:")
    print(game.taulell)
    while (not game.guanyat()):
        juga_pas(game)
        print("Taulell:")
        print(game.taulell)
        time.sleep(1)
    print("Visca la ia")
    
    
if __name__ == "__main__":
    main2()