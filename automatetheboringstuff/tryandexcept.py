def division(user_enter_1, user_enter_2):
    try:
        return user_enter_1 / user_enter_2
    except ZeroDivisionError:
        print("can't divide by 0")


again = True

while True:
    again = input("divde something? y/n ")
    if again != "y":
        again = False
        break
    user_enter_1 = int(input("divide: "))
    user_enter_2 = int(input("by: "))
    print(division(user_enter_1, user_enter_2))



