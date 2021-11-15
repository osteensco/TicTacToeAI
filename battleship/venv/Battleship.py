import random
from Classes_BS import Board, Enemy


#__________________________________________________________________________
#__gameplay function_________________________________________________
def run_game():
    #reset variables from a previous game if replayed
    enemies = []
    enemy_ships = 0
    _turns = 0
    board_size = 0

    #user sets variables
    print("________________________________________")
    print("________________________________________")
    print("All hands on deck! Captain wants a status report ASAP!")
    print("________________________________________")
    board_size = int(input("\nIdentify range from farthest enemy ship spotted! "))
    if board_size > 20:
        board_size = 20
        print("\nCaptain: Our max weapons range is 20! Do not engage any further out!")
    elif board_size < 2:
        board_size = 2
        print("\nCaptain: They're right on top of us! Set weapons range to 2!")
    else:
        board_size
    enemy_ships = int(input("\nHow many enemy ships spotted? "))
    if enemy_ships > int(board_size / 2):
        enemy_ships = int(board_size / 2)
        print(f"""\nCaptain: Wipe the seasalt from your binos sailor! I only see {enemy_ships}!""")
    elif enemy_ships < 1:
        enemy_ships = board_size
        print("\nCaptain: Pull yourself together sailor! Radar shows at least one enemy ship, maybe more!")
    else:
        enemy_ships
    _turns = int(input("\nHow much ammunition is on hand? "))
    if _turns > (board_size**2):
        _turns = (board_size**2)
        print(f"""\nCaptain: Check again sailor! We can only carry {_turns}!""")
    elif _turns < enemy_ships:
        _turns = enemy_ships
        print(f"""\nCaptain: Check again sailor! We at least have {_turns} rounds of ammunition!""")

    #generate board
    board = Board(board_size)
    board.generate()

    #spawn enemies - MAKE ME A FUNCTION IN GAME CLASS
    for i in range(enemy_ships):
        row = random.randint(0, board_size - 1)
        col = random.randint(0, board_size - 1)
        anchor = (row, col)
        if anchor not in board.enemy_ship_anchor_points:
            board.enemy_ship_anchor_points.append(anchor)
            enemy = Enemy(anchor)
            enemy.generate(board.grid)
            enemies.append(enemy)
        else:
            enemy_ships += 1  
    
    for enemy in enemies:
        enemy.hide_position(board.grid)
        for c in enemy.coordinates:
            board.enemy_ship_coordinates.append(c)


    while _turns > 0:
        board.print_board()
        print(f"""{_turns} rounds remaining! Input coordinates and fire when ready!""")
        while True:
            try:
                guess_row = int(input("Guess Row: ")) - 1
                if guess_row < 0:
                    print('invalid entry, please input whole number greater than 0')
                    continue
                guess_col = int(input("Guess Col: ")) - 1
                if guess_col < 0:
                    print('invalid entry, please input whole number greater than 0')
                    continue
                break
            except ValueError:
                print('Invalid entry, please input an integer')

        guess = (guess_row, guess_col)
        #player fire and result logic
        if (guess_row > (board_size - 1)) or (guess_col > (board_size - 1)):
            print("Captain: Weapons sighted way off course, you won't hit anything there! Don't waste any more ammo sailor!")
        elif board.grid[guess_row][guess_col] == " X" or board.grid[guess_row][guess_col] == " O":
            print("Captain: We already fired there! Don't waste any more ammo sailor!")
        elif guess in board.enemy_ship_coordinates:
            print("Target! Enemy vessel hit!")
            board.grid[guess_row][guess_col] = " X"
            for enemy in enemies:
                if guess not in enemy.coordinates:
                    continue
                else:
                    enemy.coordinates.remove(guess)
                    if not enemy.coordinates:
                        enemies.remove(enemy)
                        print("Target target target! You sunk an enemy battleship!")
                        print(f"""{len(enemies)} enemy ships remaining!""")
        else:
            print("Miss! Recalibrate!")
            board.grid[guess_row][guess_col] = " O"

        if not enemies:
            board.print_board()
            print("Captain: Outstanding! All enemy ships defeated!")
            return
    
        _turns -= 1


    print("________________________________________")
    board.enemy_positions()
    print("We're black on ammo! Retreat!")

def play():
    while True:
        run_game()
        replay = input("Play again? y/n ")
        if replay.lower() == "y" or replay.lower() == "yes":
            continue
        else:
            print("Thanks for playing! Exiting program..")
            break
        

if __name__ == '__main__':
    play()