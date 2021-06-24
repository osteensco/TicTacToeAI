import random

wins = 0
losses = 0
ties = 0

def print_score():
    print(str(wins) + ' Wins, ' + str(losses) + ' Losses, ' + str(ties) + ' Ties')

def rock_paper_scissors():
    global wins
    global losses
    global ties
    while True:
        print('rock, paper, scissors... shoot!')
        player_move = input()
        if player_move == 'rock' or player_move == 'paper' or player_move == 'scissors':
            break
        print('please type rock, paper, or scissors (no capitals)')

    print(player_move + " versus...")

    cpu_move = random.randint(1, 3)
    if cpu_move == 1:
        cpu_move = 'rock'
    elif cpu_move == 2:
        cpu_move = 'paper'
    elif cpu_move == 3:
        cpu_move = 'scissors'
    print(cpu_move + "!")

    if player_move == cpu_move:
        print("It's a tie!")
        ties += 1
    elif player_move == 'rock' and cpu_move == 'scissors':
        print('Yes! Rock beats scissors!')
        wins += 1
    elif player_move == 'paper' and cpu_move == 'rock':
        print('Yes! Paper beats rock!')
        wins += 1
    elif player_move == 'scissors' and cpu_move == 'paper':
        print('Yes! Scissors beats paper!')
        wins += 1
    else:
        print('Damn, you lost that round!')
        losses += 1
    print_score()
    play_again = input('another round? y/n ')
    if play_again == 'y' or play_again == 'Y':
        rock_paper_scissors()

rock_paper_scissors()
