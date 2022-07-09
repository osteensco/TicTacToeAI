import random


#board is stored as a dictionary
theBoard = {'top-l': ' ', 'top-m': ' ', 'top-r': ' ',
            'mid-l': ' ', 'mid-m': ' ', 'mid-r': ' ',
            'bot-l': ' ', 'bot-m': ' ', 'bot-r': ' '}


#function to replace each key value so that board is reset
def resetboard():
    for key in theBoard.keys():
        theBoard[key] = ' '
    return theBoard


#function to print board. As dict key values update (aka a move is entered), the board is updated.
def printBoard(board):
    print(board['top-l'] + '|' + board['top-m'] + '|' + board['top-r'])
    print('-+-+-')
    print(board['mid-l'] + '|' + board['mid-m'] + '|' + board['mid-r'])
    print('-+-+-')
    print(board['bot-l'] + '|' + board['bot-m'] + '|' + board['bot-r'])
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
    highscore = -1
    move = []
    for spot in theBoard.keys():
        if theBoard[spot] == ' ':
            theBoard[spot] = turn
            for each in winconditions:
                if spot in each.keys():
                    each[spot] = turn
            score = minimax(diff, turn, player, winconditions, theBoard, False)
            # print(score)
            theBoard[spot] = ' '
            for each in winconditions:
                if spot in each.keys():
                    each[spot] = ' '

            if score > highscore:
                highscore = score
                move = [spot]

            elif score == highscore:
                move.append(spot)
    # print(move)  
    return random.choice(move)


def minimax(diff, turn, player, winconditions, theBoard, cputurn):
    if check_win(turn, winconditions):
        return 1
    elif check_win(player, winconditions):
        return -1
    elif check_draw(theBoard):
        return 0

    if cputurn:
        highscore = -diff+2
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
                if score > highscore:
                    highscore = score
        return highscore

    else:
        highscore = diff-2
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
                if score < highscore:
                    highscore = score
        return highscore


def pick_turn():
    while True:#loop for response validation check
        #uses dictionary to account for response variations
        valid = {
            'X': ['x', 'X'],
            '0': ['o', 'O', '0', 0]
        }
        player = input('X or 0? ')
        if player in valid['X']:
            return 'X'
        elif player in valid['0']:
            return '0'
        else:
            print('''input not recognized, please type 'X' or '0' ''')
            continue


def choose_difficulty():
    while True:
        try:
            diff = int(input('Choose difficulty (1-3) '))
        except:
            print('Value is not an integer, please try again. ')
            continue
        if 0 < diff < 4:
            return diff
        else:
            print('difficulty choice is out of range, please try again. ')
            continue
        

#game function, designed to play against an AI
def play_cpu(diff):

    winconditions =  [
        {'top-l': ' ', 'top-m': ' ', 'top-r': ' '},
        {'mid-l': ' ', 'mid-m': ' ', 'mid-r': ' '},
        {'bot-l': ' ', 'bot-m': ' ', 'bot-r': ' '},
        {'top-l': ' ', 'mid-l': ' ', 'bot-l': ' '},
        {'top-m': ' ', 'mid-m': ' ', 'bot-m': ' '},
        {'top-r': ' ', 'mid-r': ' ', 'bot-r': ' '},
        {'top-l': ' ', 'mid-m': ' ', 'bot-r': ' '},
        {'top-r': ' ', 'mid-m': ' ', 'bot-l': ' '}
    ]

    player = pick_turn()
    turn = 'X'
    while True:
        game = True#____block prompts user and checks validity_____
        printBoard(theBoard)

        if player == turn:
            print('Turn for ' + turn + '. Move on which space?')
            move = str(input()).lower()
            
            if move == 'quit':
                return False
            elif move == 'reset':
                print(f'''{turn} has reset the game.''')
                return True
            elif move not in theBoard:
                print('''input not recognized, please enter top/mid/bot-L/M/R \nEX. 'top-L' ''')
                continue
            elif theBoard[move] == ' ':
                theBoard[move] = turn
            else:
                print("Space taken, choose another")
                continue
        else:
            move = cpu_move(diff, turn, player, winconditions, theBoard)
            theBoard[move] = turn
            print(f'''{turn} places move on {move}''')

        #loop to update winconditions list of dictionaries and check if there's a winner
        for each in winconditions:
            if move in each:
                each[move] = turn
        if check_win(turn, winconditions):
            print(str(turn) + ' is the winner!')
            printBoard(theBoard)
            game = False
            #checks for a draw, keeps count of empty spots left
        if game and check_draw(theBoard):
            printBoard(theBoard)
            print('''It's a draw!''')
            game = False

        #ends game if a winner or draw has occurred, play again prompt, while loop provides response validation check
        if not game:
            while True:
                replay = input("Play again? y/n: ")
                if replay.lower() == "y":
                    return True
                elif replay.lower() != "n":
                    print('''Response not recognized, please type 'y' or 'n' ''')
                    continue
                else:
                    return False
        if turn == 'X':
            turn = '0'
        else:
            turn = 'X'


#main loop
while True:
    play = True
    resetboard()
    difficulty = choose_difficulty()
    play = play_cpu(difficulty)
    if not play:
        break





