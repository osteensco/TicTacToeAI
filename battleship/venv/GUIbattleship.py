import random
from Classes_BS import Board, Enemy
import sys
import tkinter as tk



#TO DO:

#   -validate responses
#   -class for user coordinate input (aka Class Shot)?
#       -each shot is an object, contains coor and hit/miss status?
#   -board generation
#       -board is generated. a button is generated per [] in the board, set in a grid. grid location is same as how we have lists of lists, ie grid[1][2] is row 1, column 3



#basic design concept:
#   -menu options at top of window with drop downs as needed
#   -prompt container at top, right of text widget
#   -board below prompt container

#________________________________#
#Menu----------------------------#
#text  | Prompt Container        #
#      |-------------------------#
#      | Board                   #
#      |                         #
#      |                         #
#      |                         #
#      |                         #
#--------------------------------#






class MainApp:
    def __init__(self, parent) -> None:#tkinter functionality and flow goes in here
        parent.title('Battleship GUI!')
        self.gameinstance = Game()
        #prompt container
        self.promptcon = tk.Frame(parent)
        self.promptcon.pack(side='right', anchor='n')
        #board container
        self.boardcon = tk.Frame(parent)
        self.boardcon.pack(side='right', expand=True, fill='both')
        #console container
        self.textcon = tk.Frame(parent)
        self.textcon.pack(side='left', anchor='w', expand=True, fill='both')
        self.console = tk.Text(self.textcon, state='disabled', bg="black", fg="white", wrap="word", width=40)
        self.console.pack(expand=True, fill='both')
        self.consoleprinter = GUIConsole(self.console)
        sys.stdout = self.consoleprinter
        self.menu = MenuBar(self, parent)
        print("Battleship GUI!")

    def new_game(self):
        self.E1 = tk.Entry(self.promptcon, bd=5)
        self.E1.pack(side = "left")
        self.B1 = tk.Button(self.promptcon, text="Respond", command=None)
        self.B1.pack(side="right")
        self.gameinstance.new_game(self.B1, self.E1)


class MenuBar:
    def __init__(self, app, parent) -> None:
        self.obj = tk.Menu(parent)
        self.options = tk.Menu(self.obj, tearoff=0)
        self.options.add_command(label="New Game", command=app.new_game)
        self.obj.add_cascade(label="Options", menu=self.options)
        parent.config(menu=self.obj)


class GUIConsole():
    def __init__(self, console) -> None:
        self.console = console

    def write(self, str):
        self.console.configure(state='normal')
        self.console.insert('end', str)
        self.console.configure(state='disabled')

    def flush(self):
        pass


class Game:
    def __init__(self) -> None:
        self.enemies = []
        self.enemy_ships = 0
        self._turns = 0
        self.board_size = 0
        self.user_prompts = None
        self.board = None

    def reset_var(self):
        self.enemies = []
        self.enemy_ships = 0
        self._turns = 0
        self.board_size = 0

    def new_game(self, buttoncommand, entry):
        self.reset_var()
        print("________________________________________")
        print("________________________________________")
        print("All hands on deck! Captain wants a status report ASAP!")
        print("________________________________________")
        self.user_prompts = Prompts(self, buttoncommand, entry)
        self.board = Board(self.board_size)
        self.board.generate()


class Prompts:#creating instance of this class should run through prompts one by one waiting on user input and clicking button to continue
    def __init__(self, game, button, entry) -> None:
        self.game = game
        self.button = button
        self.entry = entry
        self.assets = [self.button, self.entry]
        self.button["command"] = None
        self.next_prompt(self.set_boardsize, "Identify range from farthest enemy ship spotted! ")

    def validate_response(entry):
        pass

    def next_prompt(self, button, label):
        self.button["command"] = button
        print(label)

    def set_boardsize(self):
        self.game.board_size = self.entry.get()
        print(self.game.board_size)
        self.entry.delete(0, 'end')
        self.next_prompt(self.set_enemyships, "How many enemy ships spotted? ")

    def set_enemyships(self):
        self.game.enemy_ships = self.entry.get()
        print(self.game.enemy_ships)
        self.entry.delete(0, 'end')
        self.next_prompt(self.set_turns, "How much ammunition is on hand? ")

    def set_turns(self):
        self.game._turns = self.entry.get()
        print(self.game._turns)
        for asset in self.assets:
            asset.destroy()


class Shoot:
    def __init__(self) -> None:
        pass











def play():
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()

if __name__ == '__main__':
    play()