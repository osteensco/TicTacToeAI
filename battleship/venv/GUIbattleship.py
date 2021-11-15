import random
from Classes_BS import Board, Enemy
import sys
import tkinter as tk



#TO DO:
#   -set up print statements to also print in text widget located on left side of window
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
        self.gameinstance = Game()
        #prompt container
        self.promptcon = tk.Frame(parent)
        self.promptcon.pack(side='right', anchor='n')
        self.L1 = tk.Label(self.promptcon, text=None)
        self.L1.pack(side = "left")
        self.E1 = tk.Entry(self.promptcon, bd=5)
        self.E1.pack(side = "right")
        self.B1 = tk.Button(self.promptcon, text="Respond", command=None)
        self.B1.pack(side="right")
        #board container
        self.boardcon = tk.Frame(parent)
        self.boardcon.pack(side='right', expand=True, fill='both')
        #console container
        self.textcon = tk.Frame(parent)
        self.textcon.pack(side='left', anchor='w', expand=True, fill='both')
        self.console = tk.Text(self.textcon, bg="black", fg="white", wrap="word")
        self.console.pack(expand=True, fill='both')
        self.consoleprinter = GUIConsole(self.console)
        self.start_text()
        self.gameinstance.user_prompts = Prompts(self.gameinstance, self.B1, self.L1, self.E1)


    def start_text(self):
        print("________________________________________")
        print("________________________________________")
        print("All hands on deck! Captain wants a status report ASAP!")
        print("________________________________________")


class Game:
    def __init__(self) -> None:
        self.enemies = []
        self.enemy_ships = 0
        self._turns = 0
        self.board_size = 0
        self.user_prompts = None


    def reset_var(self):
        self.enemies = []
        self.enemy_ships = 0
        self._turns = 0
        self.board_size = 0


class Prompts:#creating instance of this class should run through prompts one by one waiting on user input and clicking button to continue
    def __init__(self, game, button, label, entry) -> None:
        self.game = game
        self.button = button
        self.label = label
        self.entry = entry
        self.assets = [self.button, self.label, self.entry]
        self.button["command"] = self.set_boardsize
        self.label["text"]  = "Identify range from farthest enemy ship spotted! "


    def validate_response(entry):
        pass


    def next_prompt(self, button, label):
        self.button["command"] = button
        self.label["text"] = label


    def set_boardsize(self):
        self.game.board_size = self.entry.get()
        self.entry.delete(0, 'end')
        self.next_prompt(self.set_enemyships, "How many enemy ships spotted? ")


    def set_enemyships(self):
        self.game.enemy_ships = self.entry.get()
        self.entry.delete(0, 'end')
        self.next_prompt(self.set_turns, "How much ammunition is on hand? ")


    def set_turns(self):
        self.game._turns = self.entry.get()
        for asset in self.assets:
            asset.destroy()


class GUIConsole():
    def __init__(self, printer) -> None:
        self.printer = printer


    def write(self, str):
        self.printer.insert(tk.END, str)











def play():
    root = tk.Tk()
    app = MainApp(root)
    sys.stdout = app.consoleprinter
    root.title('Battleship GUI!')
    root.mainloop()

if __name__ == '__main__':
    play()