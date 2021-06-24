
Inventory = {'dict_title': 'Inventory', 'rope': 1, 'torch': 6, 'gold coin': 42, 'dagger': 1, 'arrow': 12}

def display(thing):
    print(thing['dict_title'])
    thing_unique = len(thing)
    thing_total = 0
    for key, value in thing.items():
        if isinstance(value, int):
            thing_total += thing.get(key, 0)
            print(str(value) + " " + str(key))
        else:
            continue
    print("Item types: " + str(thing_unique))
    print("Total number of item: " + str(thing_total))


display(Inventory)



