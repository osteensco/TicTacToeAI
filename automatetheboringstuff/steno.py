from itertools import combinations
steno_order = (
    'S', 'T', 'K', 'P', 'W', 'H',
    'R', 'A', 'O', '*', 'E',
)


all_cords = []
def combinations_of_steno_order(min_keys, max_keys):
    for i in range(min_keys, max_keys):
        for chord in combinations(steno_order, i):
            stringatize = ''.join(list(chord))
            all_cords.append(stringatize)
    return all_cords


with open('other_steno.txt', 'a') as writer:
    for x in combinations_of_steno_order(1, len(steno_order)):
        writer.write(f'''{x}\n''')


