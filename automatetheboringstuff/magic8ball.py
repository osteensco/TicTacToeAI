import random

possible_answers = ['It is certain', 'It is decidedly so', 'Yes',
           'Fog clouds the visions of the future, try again',
            'The path that leads to the answer you seek is unpaved for now, try again later',
            'Look within yourself and ask once more', 'Of course not, you knew that',
            'Outlook is bleak', 'Hard no']

positives = ["Yes", "y", "yes", "sure", "Y", "fuck yea", "yes please"]

def get_answer():
    print(possible_answers[random.randint(0, len(possible_answers) - 1)])



while True:
    prompt = input("Do you wish to consult the spirits?")

    if prompt in positives:
        input("Ask the spirits your question: ")
        get_answer()
    else:
        print("The spirits find you unworthy")
        break


