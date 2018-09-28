logWidth = 13


def print_info(message):
  print("> [INFO".ljust(logWidth) + "]: " + str(message))


def print_player(message, i):
  concatP = "> [PLAYER " + str(i)
  print(concatP.ljust(logWidth) + "]: " + str(message))


def print_deck(message):
  print("> [DECK".ljust(logWidth) + "]: " + str(message))


def print_score(message):
  print("> [SCORE".ljust(logWidth) + "]: " + str(message))


def print_slaprule(message):
  print("> [SLAP RULE".ljust(logWidth) + "]: " + str(message))


def print_scoreboard(game):
  """Prints scores (# of cards) of each player"""
  

# DEBUG
def print_turns(game):
  x = "; ".join(("P" + str(i) + ": " + ("Yes" if (not q.empty()) else "No"))
                for i, q in enumerate(game.turns))
  x = "Whose turn - " + x
  print(x)

def print_turnsLeft(game):
  x = "; ".join(("P" + str(i) + ": " + str(p.turnsLeft)) for i, p in enumerate(game.players))
  x = "Turns left - " + x
  print(x)