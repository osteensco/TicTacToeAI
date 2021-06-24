import random

##game is within function to allow for replays.
def guess_the_number():
    secretNumber = random.randint(1, 7)
    print("I am thinking of a number between 1 and 20.")
    user_input = int(input("How many guess do you think you can get it in? "))
    for guessesTaken in range(user_input):
        guess = int(input("Take a guess: "))

        if guess < secretNumber:
            print("Your guess is too low! You have " + str(user_input - (guessesTaken + 1)) + " guesses left!")
        elif guess > secretNumber:
            print("Your guess is too high! You have " + str(user_input - (guessesTaken + 1)) + " guesses left!")
        else:
            if guessesTaken > 1:
                print("Correct! You got it in " + str(guessesTaken) + " tries!")
            else:
                print("Correct! You got it in 1 try!")
            replay = input("Play again? y/n: ")
            if replay == "y" or replay == "Y":
                guess_the_number()
            else:
                break
    if guess != secretNumber:
        print("None of your guesses were correct. The number I chose was " + str(secretNumber) + ".")
        replay = input("Play again? y/n: ")
        if replay == "y" or replay == "Y":
            guess_the_number()
#_____end of function_______________


guess_the_number()
