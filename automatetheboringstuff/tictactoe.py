#board is stored as a dictionary
global theBoard = {'top-L': ' ', 'top-M': ' ', 'top-R': ' ',
            'mid-L': ' ', 'mid-M': ' ', 'mid-R': ' ',
            'bot-L': ' ', 'bot-M': ' ', 'bot-R': ' '}

#funtion to convert dictionary into visual board

def printBoard(board):
    print(board['top-L'] + '|' + board['top-M'] + '|' + board['top-R'])
    print('-+-+-')
    print(board['mid-L'] + '|' + board['mid-M'] + '|' + board['mid-R'])
    print('-+-+-')
    print(board['bot-L'] + '|' + board['bot-M'] + '|' + board['bot-R'])

#winconditions stored as dictionary for reference to check if there is a winner
global winconditions = [['top-L', 'top-M', 'top-R'], ['mid-L', 'mid-M', 'mid-R'], ['bot-L', 'bot-M', 'bot-R'],
                 ['top-L', 'mid-L', 'bot-L'], ['top-M', 'mid-M', 'bot-M'], ['top-R', 'mid-R', 'bot-R'],
                 ['top-L', 'mid-M', 'bot-R'], ['top-R', 'mid-M', 'bot-L']]

global turn = 'X'

def play_game():
    while True:
        game = 0
        printBoard(theBoard)
        print('Turn for ' + turn + '. Move on which space?')
        move = str(input())
        if move not in theBoard:
            print('please enter top/mid/bot-L/M/R')
            continue
        theBoard[move] = turn
        index = -1
        for each in winconditions:
            index += 1
            if move in each:
                update_wincon = each.index(move)
                winconditions[index][update_wincon] = turn
            if (each[0] == 'X' and each[1] == 'X' and each[2] == 'X') or (each[0] == '0' and each[1] == '0' and each[2] == '0'):
                game = 1
                print(str(turn) + ' is the winner!')
                break
        if game == 1:
            break
        if turn == 'X':
            turn = '0'
        else:
            turn = 'X'

play_game()






