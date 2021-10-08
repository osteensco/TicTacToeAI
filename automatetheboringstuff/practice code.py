

theBoard = {'top-L': 'X', 'top-M': '0', 'top-R': '0',
            'mid-L': ' ', 'mid-M': 'X', 'mid-R': ' ',
            'bot-L': ' ', 'bot-M': ' ', 'bot-R': ' '}

winconditions =  [
        {'top-L': 'X', 'top-M': '0', 'top-R': '0'},
        {'mid-L': ' ', 'mid-M': 'X', 'mid-R': ' '},
        {'bot-L': ' ', 'bot-M': ' ', 'bot-R': ' '},
        {'top-L': 'X', 'mid-L': ' ', 'bot-L': ' '},
        {'top-M': '0', 'mid-M': 'X', 'bot-M': ' '},
        {'top-R': '0', 'mid-R': ' ', 'bot-R': ' '},
        {'top-L': 'X', 'mid-M': 'X', 'bot-R': ' '},
        {'top-R': '0', 'mid-M': 'X', 'bot-L': ' '}
    ]

# bestscore = 0
# move = ''
# for k in theBoard:
#     if theBoard[k] == ' ':
#         count = 0
#         for each in winconditions:
#             if k in each:
#                 if sum(x == player for x in each.values()) < 2:
#                     for e in each:
#                         if each[e] != player:
#                             count += 1
#                         if each[e] == turn:
#                             count += 1
#                     if count == bestscore:
#                         count += sum(x == turn for x in each.values())
#                 else:
#                     return k
#         if count > bestscore:
#             bestscore = count
#             move = k
#         print(f'''{move}, {bestscore}''')

