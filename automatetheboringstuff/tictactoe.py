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

#Main game loop
def play_game():
    # winconditions stored as list of lists as reference to check if there is a winner. kept within function to reset itself with each play through.
    winconditions = [['top-L', 'top-M', 'top-R'], ['mid-L', 'mid-M', 'mid-R'], ['bot-L', 'bot-M', 'bot-R'],
                     ['top-L', 'mid-L', 'bot-L'], ['top-M', 'mid-M', 'bot-M'], ['top-R', 'mid-R', 'bot-R'],
                     ['top-L', 'mid-M', 'bot-R'], ['top-R', 'mid-M', 'bot-L']]

    turn = 'X'
    while True:
        game = True#____block prompts user and checks validity_____
        printBoard(theBoard)
        print('Turn for ' + turn + '. Move on which space?')
        move = str(input())
        if move == 'quit':
            break
        if move == 'reset':
            print(f'''{turn} has reset the game.''')
            resetboard()
            play_game()
        if move not in theBoard:
            print('please enter top/mid/bot-L/M/R')
            continue
        if theBoard[move] == ' ':
            theBoard[move] = turn
        else:
            print("Space taken, choose another")
            continue

        #block runs through win condition check and places a mark where the input matches an item in each list, kinda like bingo
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
            emptyspots = 9
            for key in theBoard.keys():
                if game == True and theBoard[key] != ' ':
                    emptyspots -= 1
            if emptyspots == 0:
                print('''It's a draw!''')
                game = False

        #ends game if a winner or draw has occurred, prompts play again? - will restart game if y end program if n
        if game == False:
            replay = input("Play again? y/n: ")
            if replay == "y":
                resetboard()
                play_game()
            else:
                break
        if turn == 'X':
            turn = '0'
        else:
            turn = 'X'

play_game()






