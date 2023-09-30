import numpy as np 

N= 3

class GAME:
    def __init__(self):
        self.win = np.matrix([[0,1,2],
                    [3,4,5],
                    [6,7,8]])
        
        self.taulell = np.matrix([[2,6,4],
                                 [1,5,7],
                                 [0,9,3]])

        self.pos_0 = np.array(np.where(self.taulell == 0))

    def guanyat(self):
        for i in range(3):
            for j in range(3):
                if self.win[i,j] != self.taulell[i,j]: return False
        
        return True

    """
    (-1,0)  -> 0 cap a dalt
    (1,0) -> 0 cap a baix
    (0,1)  -> 0 cap a dreta
    (0,-1) -> 0 cap a esquerra    
    """

    def is_valid_move(self, move):
        if (self.pos_0[0] == 0 and move[0] == -1): return False
        if (self.pos_0[0] == 2 and move[0] == 1): return False
        if (self.pos_0[1] == 0 and move[1] == -1): return False
        if (self.pos_0[1] == 2 and move[1] == 1): return False

    def move (self, move):  # el moviment es vàlid
        self.taulell[self.pos_0], self.taulell[self.pos_0 + move] = self.taulell[self.pos_0 + move], self.taulell[self.pos_0]





def main():
    game = GAME()

    while(not game.guanyat()):
        user = input("introdueix nombre: ")

        move = [0,0]
        if (user == "dalt"): move = [-1,0]
        elif (user == "baix"): move = [1,0]
        elif (user == "esq"): move = [0,-1]
        elif (user == "drt"): move = [0,1]

        print(move)
        

        if (game.is_valid_move(move)):
            game.move(move)
        else:
            print("Invalid!")

        print("Taulell:")
        print(game.taulell)

    print("has guanyat")


if __name__ == "__main__":
    main()