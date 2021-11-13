import random
from tkinter.constants import RADIOBUTTON
from Classes_BS import *
import sys
import tkinter as tk







class MainApp:
    def __init__(self, parent) -> None:
        pass

class Game:
    def __init__(self, assets) -> None:
        self.enemies = []
        self.enemy_ships = 0
        self._turns = 0
        self.board_size = 0
        self.assets = assets
        self.current_prompt = None
    

    def next_prompt(self, prompt):
        self.current_prompt = prompt


    def reset_var(self):
        self.enemies = []
        self.enemy_ships = 0
        self._turns = 0
        self.board_size = 0


class Prompt:
    def __init__(self, button, label) -> None:
        self.button = button
        self.label = label

    
    def activate(self, button, label):
        button["command"] = self.button
        label["text"] = self.label
    

        
#make these functions methods inside of Prompt class to be able to adjust class variables by calling method
def set_turns():
    global _turns
    _turns = E1.get()
    E1.delete(0, 'end')
    for asset in assets:
        asset.delete(0, 'end')


def set_enemyships(self):
    global enemy_ships
    enemy_ships = E1.get()
    E1.delete(0, 'end')
    L1["text"]  = "How much ammunition is on hand? "
    B1["command"] = self.set_turns


def set_boardsize(self):
    global board_size
    board_size = E1.get()
    E1.delete(0, 'end')
    L1["text"] = "How many enemy ships spotted? "
    B1["command"] = self.set_enemyships






L1 = tk.Label(root, text="Identify range from farthest enemy ship spotted! ")
L1.pack(side = "left")
E1 = tk.Entry(root, bd =5)
E1.pack(side = "right")
B1 = tk.Button(root, text="Respond", command=set_boardsize)
B1.pack(side="right")


#on submission, next prompt is activated. This continues until all prompts are complete and variables are set.


#board is generated. a button is generated per [] in the board, set in grid. grid location is same as how we have lists of lists, ie grid[1][2] is row 1, column 3
def play():
    root = tk.Tk()
    app = MainApp(root)
    root.title('Battleship GUI!')
    root.mainloop()

if __name__ == '__main__':
    play()