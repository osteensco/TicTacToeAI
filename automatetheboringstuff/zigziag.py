import time, sys
indent = 0 #how many spaces to indent.
indentincreasing = True #whether the indentation is increasing or not

try:
    while True: #Main program loop
        print(' ' * indent, end='')
        print('*******')
        time.sleep(.5) #this pauses for .5 sec each iteration

        if indentincreasing:
            indent = indent + 1
            if indent == 20:
                indentincreasing = False

        else:
            indent = indent - 1
            if indent == 0:
                indentincreasing = True
except KeyboardInterrupt:
    sys.exit()
