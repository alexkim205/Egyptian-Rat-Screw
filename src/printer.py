logWidth = 10

def print_info(message):
    print("[INFO".ljust(10) + "]: " + message)

def print_player(message, i):
    concatP = "[PLAYER " + str(i)
    print(concatP.ljust(10) + "]: " + message)

def print_deck(message):
    print("[DECK".ljust(10) + "]: " + message)

def print_score(message):
    print("[SCORE".ljust(10) + "]: " + message)

def print_slaprule(message):
    print("[SLAP RULE".ljust(10) + "]: " + message)