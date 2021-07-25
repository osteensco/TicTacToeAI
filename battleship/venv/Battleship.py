import random
import Classes_BS

#board starts as empty list so user can create their own size
board = []
hit_enemy_ship = []
enemies = []
enemy_ships = 0
_turns = 0
board_size = 0
#hit enemy ship list is used to track how many ships are sunk, it's then compared to total number of enemy ships (see botom) as victory condition

#_____user prompts is function so it can be called by player to play again
#_____user prompts with size limitations for each prompt______________________________________
#_____captain will chew out player for inputting silly info
#_____prompt defaults to minimum values if user input is too small______________________________
def user_prompts():
  
  print("All hands on deck! Captain wants a status report ASAP!")

  board_size = int(input("Identify range from farthest enemy ship spotted! "))
  if board_size > 20:
    board_size = 20
    print("Captain: Our max weapons range is 20! Do not engage any further out!")
  elif board_size < 2:
    board_size = 2
    print("Captain: They're right on top of us! Set weapons range to 2!")
  else:
    board_size

  enemy_ships = int(input("How many enemy ships spotted? "))
  if enemy_ships > int(board_size / 2):
    enemy_ships = int(board_size / 2)
    print(f"""Captain: Wipe the seasalt from your binos sailor! I only see {enemy_ships}!""")
  elif enemy_ships < 1:
    enemy_ships = board_size
    print("Captain: Pull yourself together sailor! Radar shows at least one enemy ship, maybe more!")
  else:
    enemy_ships

  _turns = int(input("How much ammunition is on hand? "))
  if _turns > (board_size**2):
    _turns = (board_size**2)
    print(f"""Captain: Check again sailor! We can only carry {_turns}!""")
  elif _turns < enemy_ships:
    _turns = enemy_ships
    print(f"""Captain: Check again sailor! We at least have {_turns} rounds of ammunition!""")

  
  for i in range(board_size):
    board.append(["[]"] * board_size)
  print_board(board)
  run_game()

#__________________________________________________________________
#____functions______________________________________________________________

def print_board(board):
  for row in board:
    print(' '.join(row))

def random_row(board):
  return random.randint(0, len(board) - 1)

def random_col(board):
  return random.randint(0, len(board[0]) - 1)

def enemy_positions(board):
  for coor in enemy_ship_coordinates:
    board[coor[0]][coor[1]] = " X"
  print_board(board)


#functions for randomized ship sizes_____(not working)

enemy_ship_anchor_points = []
enemy_ship_coordinates = []

#________________________________________________________________________________
#_____random enemy ship generator____________________________________________________________

#while loop will generate coordinates of enemy ships up until we have enough for all enemy ships, if condition ensures no repeats
def spawn_enemies():
  for i in range(enemy_ships):
    while True:
      row = random_row(board)
      col = random_col(board)
      anchor = (row, col)
      if anchor not in enemy_ship_anchor_points:
        enemy_ship_anchor_points.append(anchor)
        break
      else:
        continue
    enemy = Classes_BS.Enemy(anchor)
    enemy.generate(board)
    enemies.append(enemy)
    enemy_ship_coordinates.append(enemy.coordinates)

#__________________________________________________________________________
#__gameplay placed in a loop inside function for replayability__________________________________________________
def run_game():
  spawn_enemies()
  for shot in range(_turns):
    print("hello")
    print(str(_turns - shot) + " rounds remaining! Input coordinates and fire when ready!")
    guess_row = int(input("Guess Row: ")) - 1
    guess_col = int(input("Guess Col: ")) - 1

    guess = [guess_row, guess_col]
#move if statement below to consolidate under the else statement
    if board[guess_row][guess_col] == "X":
      print("Captain: We already fired there! Don't waste any more ammo sailor!")
    if guess in enemy_ship_coordinates and board[guess_row][guess_col] != "X":
      print("Target target target! You sunk an enemy battleship!")
      board[guess_row][guess_col] = "X"
      hit_enemy_ship.append(1)
      print_board(board)
    else:
      if (guess_row > (board_size - 1)) or (guess_col > (board_size - 1)):
        print("Captain: Weapons sighted way off course, you won't hit anything there! Don't waste any more ammo sailor!")
      elif board[guess_row][guess_col] == " O":
        print("Captain: We already fired there! Don't waste any more ammo sailor!")
      else:
        print("Miss! Recalibrate!")
        board[guess_row][guess_col] = " O"

        print_board(board)


    if int(len(hit_enemy_ship)) == enemy_ships:
      print("Captain: Outstanding! All enemy ships defeated!")
      replay = input("Play again? y/n ")
      if replay == "y" or replay == "Y":
        user_prompts()
    if shot == int(_turns-1):
      print("________________________________________")
      enemy_positions(board)
      print("We're black on ammo! Retreat!")
      replay = input("Play again? y/n ")
      if replay == "y" or replay == "Y":
        user_prompts()


user_prompts() #runs user prompts so ships will generate

#____________________________________________________________________________________________