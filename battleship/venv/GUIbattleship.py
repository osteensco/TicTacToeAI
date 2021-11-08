import random
from tkinter.constants import RADIOBUTTON
from Classes_BS import *
import sys
import tkinter as tk


enemies = []
enemy_ships = 0
_turns = 0
board_size = 0

root = tk.Tk()
root.title('Battleship GUI!')


class Prompt():
    pass





def set_enemyships():
    global enemy_ships
    enemy_ships = E1.get()
    E1.delete(0, 'end')


def set_boardsize():
    global board_size
    board_size = E1.get()
    E1.delete(0, 'end')
    L1["text"] = "How many enemy ships spotted? "
    B1["command"] = set_enemyships


def test_boardsize():
    tk.Label(root, text=f'{board_size}', pady=20, bg='#ffbf00').pack(side="right")

def test_enships():
    tk.Label(root, text=f'{enemy_ships}', pady=20, bg='#ffbf00').pack(side="right")

def reset_var():
    global board_size, enemy_ships
    enemies = []
    enemy_ships = 0
    _turns = 0
    board_size = 0
    B1["command"] = set_boardsize


L1 = tk.Label(root, text="Identify range from farthest enemy ship spotted! ")
L1.pack(side = "left")
E1 = tk.Entry(root, bd =5)
E1.pack(side = "right")
B1 = tk.Button(root, text="Respond", command=set_boardsize)
B1.pack(side="right")

testbutton = tk.Button(root, text="Test Board Size", command=test_boardsize).pack(side="right")
tb2 = tk.Button(root, text="Test Enemy Ships", command=test_enships).pack(side="right")
reset_test = tk.Button(root, text="Test Reset", command=reset_var).pack(side="right")
#on submission, next prompt is activated. This continues until all prompts are complete and variables are set.


#board is generated. a button is generated per [] in the board, set in grid. grid location is same as how we have lists of lists, ie grid[1][2] is row 1, column 3

root.mainloop()