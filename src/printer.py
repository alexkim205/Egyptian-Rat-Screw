logWidth = 13

def print_info(message):
    print("[INFO".ljust(logWidth) + "]: " + str(message))

def print_player(message, i):
    concatP = "[PLAYER " + str(i)
    print(concatP.ljust(logWidth) + "]: " + str(message))

def print_deck(message):
    print("[DECK".ljust(logWidth) + "]: " + str(message))

def print_score(message):
    print("[SCORE".ljust(logWidth) + "]: " + str(message))

def print_slaprule(message):
    print("[SLAP RULE".ljust(logWidth) + "]: " + str(message))