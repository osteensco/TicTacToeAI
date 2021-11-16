import random
import tkinter as tk


class Board:
    def __init__(self, board_size):
        self.grid = []
        self.enemy_ship_coordinates = []
        self.enemy_ship_anchor_points = []
        self.board_size = board_size

    
    def generate(self):
        for i in range(self.board_size):
            self.grid.append(["[]"] * self.board_size)


    def print_board(self):#add if not GUI logic
        print("________________________________________\n")
        for row in self.grid:
            print(' '.join(row))
        print("________________________________________")


    def enemy_positions(self):
        for coor in self.enemy_ship_coordinates:
            self.grid[coor[0]][coor[1]] = " X"
        self.print_board()



class Enemy:
    def __init__(self, anchor):
        self.x = anchor[0] #random.randint(0, len(board) - 1)
        self.y = anchor[1]  #random.randint(0, len(board) - 1)
        self.orientation = random.choice(['x', 'y'])
        self.direction = random.choice(['u_l', 'd_r'])
        self.length = random.randint(1, 4)
        self.coordinates = [(self.y, self.x)]
        self.destroyed = False
        

    def generate(self, board):
        for i in range(self.length):
            board[self.y][self.x] = '}{'
            if self.orientation == 'x':
                if self.direction == 'u_l':
                    for i in range(self.length):
                        if board[self.y][self.x] != '}{' or self.x > 0:
                            self.x -= 1
                            board[self.y][self.x] = '}{'
                            self.coordinates.append((self.y, self.x))
                        else:
                            break
                if self.direction == 'd_r':
                    for i in range(self.length):
                        if board[self.y][self.x] != '}{' or self.x < len(board) - 1:
                            self.x += 1
                            board[self.y][self.x] = '}{'
                            self.coordinates.append((self.y, self.x))
                        else:
                            break
            if self.orientation == 'y':
                if self.direction == 'u_l':
                    for i in range(self.length):
                        if board[self.y][self.x] != '}{' or self.y > 0:
                            self.y -= 1
                            board[self.y][self.x] = '}{'
                            self.coordinates.append((self.y, self.x))
                        else:
                            break
                if self.direction == 'd_r':
                    for i in range(self.length):
                        if board[self.y][self.x] != '}{' or self.y < len(board) - 1:
                            self.y += 1
                            board[self.y][self.x] = '}{'
                            self.coordinates.append((self.y, self.x))
                        else:
                            break

    def show_position(self, board):
        for coor in self.coordinates:
            board[coor[0]][coor[1]] = "}{"

    def hide_position(self, board):
        for coor in self.coordinates:
            board[coor[0]][coor[1]] = "[]"

