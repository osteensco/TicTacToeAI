import random

class Enemy:
    def __init__(self, anchor):
        self.x = anchor[0] #random.randint(0, len(board) - 1)
        self.y = anchor[1]  #random.randint(0, len(board) - 1)
        self.orientation = random.choice('x', 'y')
        self.direction = random.choice('u_l', 'd_r')
        self.length = random.randint(1, 4)
        self.coordinates = []
        
    def generate(self, board):
        board[self.y][self.x] = '0'
        if self.orientation is 'x':
            if self.direction is 'u_l':
                for i in range(self.length):
                    if board[self.y][self.x] is not '0' or self.x > 0:
                        self.x -= 1
                        board[self.y][self.x] = '0'
                        self.coordinates.append((self.y, self.x))
                    else:
                        break
            if self.direction is 'd_r':
                for i in range(self.length):
                    if board[self.y][self.x] is not '0' or self.x < len(board) - 1:
                        self.x += 1
                        board[self.y][self.x] = '0'
                        self.coordinates.append((self.y, self.x))
                    else:
                        break
        if self.orientation is 'y':
            if self.direction is 'u_l':
                for i in range(self.length):
                    if board[self.y][self.x] is not '0' or self.y > 0:
                        self.y -= 1
                        board[self.y][self.x] = '0'
                        self.coordinates.append((self.y, self.x))
                    else:
                        break
            if self.direction is 'd_r':
                for i in range(self.length):
                    if board[self.y][self.x] != '0' or self.y < len(board) - 1:
                        self.y += 1
                        board[self.y][self.x] = '0'
                        self.coordinates.append((self.y, self.x))
                    else:
                        break