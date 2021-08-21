import random
fast_food = ["5 guys/Moes", "Waffle House","chinese", "grandma's pizza", "thai"]
sit_down_food = ["McCray's", "Buff WW", "Hibachi", "Sonny's"]
fun = ["park", "Fernbank", "sex", "Go karts", "top golf", "mall of georgia", "beltline", "atlantic station"]

choice = 0
activity = int(input("choose activity number (1.fast_food, 2.sit_down_food, 3.fun)"))

if activity == 1:
    choice = random.randint(0, (len(fast_food) - 1))
    decision = fast_food[choice]
    print(decision)
elif activity == 2:
    choice = random.randint(0, (len(sit_down_food) - 1))
    decision = sit_down_food[choice]
    print(decision)
elif activity == 3:
    choice = random.randint(0, (len(fun) - 1))
    decision = fun[choice]
    print(decision)

#added a comment for testing out git