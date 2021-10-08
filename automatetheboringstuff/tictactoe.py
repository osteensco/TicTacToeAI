import random
#board is stored as a dictionary
theBoard = {'top-L': ' ', 'top-M': ' ', 'top-R': ' ',
            'mid-L': ' ', 'mid-M': ' ', 'mid-R': ' ',
            'bot-L': ' ', 'bot-M': ' ', 'bot-R': ' '}


#function to replace each key value so that board is reset
def resetboard():
    for key in theBoard.keys():
        theBoard[key] = ' '
    return theBoard


#function to print board. As dict key values update (aka a move is entered), the board is updated.
def printBoard(board):
    print(board['top-L'] + '|' + board['top-M'] + '|' + board['top-R'])
    print('-+-+-')
    print(board['mid-L'] + '|' + board['mid-M'] + '|' + board['mid-R'])
    print('-+-+-')
    print(board['bot-L'] + '|' + board['bot-M'] + '|' + board['bot-R'])
    print('______________________________________________________')


def check_draw(theBoard):
    for spot in theBoard.keys():
        if theBoard[spot] == ' ':
            return False
    return True

def check_win(turn, winconditions):
    for each in winconditions:
        if list(each.values()) == [turn, turn, turn]:
            return True
    return False


def cpu_move(diff, turn, player, winconditions, theBoard):
    bestscore = -1
    move = []
    for spot in theBoard.keys():
        if theBoard[spot] == ' ':
            theBoard[spot] = turn
            for each in winconditions:
                if spot in each.keys():
                    each[spot] = turn
            score = minimax(diff, turn, player, winconditions, theBoard, False)
            print(score)
            theBoard[spot] = ' '
            for each in winconditions:
                if spot in each.keys():
                    each[spot] = ' '

            if score > bestscore:
                bestscore = score
                move = [spot]

            elif score == bestscore:
                move.append(spot)
    print(move)  
    return random.choice(move)


def minimax(diff, turn, player, winconditions, theBoard, cputurn):
    if check_win(turn, winconditions):
        return 1
    elif check_win(player, winconditions):
        return -1
    elif check_draw(theBoard):
        return 0


    if cputurn:
        bestscore = -diff+2
        for spot in theBoard.keys():
            if theBoard[spot] == ' ':
                theBoard[spot] = turn
                for each in winconditions:
                    if spot in each.keys():
                        each[spot] = turn
                score = minimax(diff, turn, player, winconditions, theBoard, False)
                theBoard[spot] = ' '
                for each in winconditions:
                    if spot in each.keys():
                        each[spot] = ' '
                if score > bestscore:
                    bestscore = score
        return bestscore

    else:
        bestscore = diff-2
        for spot in theBoard.keys():
            if theBoard[spot] == ' ':
                theBoard[spot] = player
                for each in winconditions:
                    if spot in each.keys():
                        each[spot] = player
                score = minimax(diff, turn, player, winconditions, theBoard, True)
                theBoard[spot] = ' '
                for each in winconditions:
                    if spot in each.keys():
                        each[spot] = ' '
                if score < bestscore:
                    bestscore = score
        return bestscore


def pick_turn():
    player = input('X or 0? ')
    if player == 'X' or player == '0':
        return player 
    else:
        print(player)
        print('''please type 'X' or '0' ''')
        pick_turn()


#Main game loop
def play_game():

    
    # winconditions stored as list of lists as reference to check if there is a winner. kept within function to reset itself with each play through.
    winconditions = [['top-L', 'top-M', 'top-R'], ['mid-L', 'mid-M', 'mid-R'], ['bot-L', 'bot-M', 'bot-R'],
                        ['top-L', 'mid-L', 'bot-L'], ['top-M', 'mid-M', 'bot-M'], ['top-R', 'mid-R', 'bot-R'],
                        ['top-L', 'mid-M', 'bot-R'], ['top-R', 'mid-M', 'bot-L']]

    emptyspots = 9
    turn = 'X'
    while True:
        game = True#____block prompts user and checks validity_____
        printBoard(theBoard)
        print('Turn for ' + turn + '. Move on which space?')
        move = str(input())
        if move == 'quit':
            return False
        if move == 'reset':
            print(f'''{turn} has reset the game.''')
            return True
        if move not in theBoard:
            print('please enter top/mid/bot-L/M/R')
            continue
        if theBoard[move] == ' ':
            theBoard[move] = turn
        else:
            print("Space taken, choose another")
            continue

        #block runs through win condition check and places a mark where the input matches an item in each list, kinda like bingo
        emptyspots -= 1
        index = -1
        for each in winconditions:
            index += 1
            if move in each:
                update_wincon = each.index(move)
                winconditions[index][update_wincon] = turn

            #actual win condition check, ends game if there is a winner
            if (each[0] == 'X' and each[1] == 'X' and each[2] == 'X') or (each[0] == '0' and each[1] == '0' and each[2] == '0'):
                print(str(turn) + ' is the winner!')
                game = False

            #checks for a draw, keeps count of empty spots left   
        if game and emptyspots == 0:
            print('''It's a draw!''')
            game = False

        #ends game if a winner or draw has occurred, prompts play again? - will restart game if y end program if n
        if not game:
            replay = input("Play again? y/n: ")
            if replay == "y":
                return True
            else:
                return False
        if turn == 'X':
            turn = '0'
        else:
            turn = 'X'


def play_cpu(diff):


    winconditions =  [
        {'top-L': ' ', 'top-M': ' ', 'top-R': ' '},
        {'mid-L': ' ', 'mid-M': ' ', 'mid-R': ' '},
        {'bot-L': ' ', 'bot-M': ' ', 'bot-R': ' '},
        {'top-L': ' ', 'mid-L': ' ', 'bot-L': ' '},
        {'top-M': ' ', 'mid-M': ' ', 'bot-M': ' '},
        {'top-R': ' ', 'mid-R': ' ', 'bot-R': ' '},
        {'top-L': ' ', 'mid-M': ' ', 'bot-R': ' '},
        {'top-R': ' ', 'mid-M': ' ', 'bot-L': ' '}
    ]

    player = pick_turn()
    turn = 'X'
    while True:
        game = True#____block prompts user and checks validity_____
        printBoard(theBoard)

        if player == turn:
            print('Turn for ' + turn + '. Move on which space?')
            move = str(input())

            if move == 'quit':
                return False
            elif move == 'reset':
                print(f'''{turn} has reset the game.''')
                return True
            elif move not in theBoard:
                print('please enter top/mid/bot-L/M/R')
                continue
            elif theBoard[move] == ' ':
                theBoard[move] = turn
            else:
                print("Space taken, choose another")
                continue
        else:
            move = cpu_move(diff, turn, player, winconditions, theBoard)
            theBoard[move] = turn


        for each in winconditions:
            if move in each:
                each[move] = turn
        if check_win(turn, winconditions):
            print(str(turn) + ' is the winner!')
            game = False
            #checks for a draw, keeps count of empty spots left
        if game and check_draw(theBoard):
            print('''It's a draw!''')
            game = False

        #ends game if a winner or draw has occurred, prompts play again? - will restart game if y end program if n
        if not game:
            replay = input("Play again? y/n: ")
            if replay == "y":
                return True
            else:
                return False
        if turn == 'X':
            turn = '0'
        else:
            turn = 'X'




while True:
    play = True
    resetboard()
    cpu = input('Play cpu? y/n ')
    if cpu == 'y':
        difficulty = int(input('Choose difficulty (1-3) '))
        play = play_cpu(difficulty)
    else:
        play = play_game()
    if not play:
        break





