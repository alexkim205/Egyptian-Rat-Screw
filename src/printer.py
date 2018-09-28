logWidth = 16


def print_info(message):
  print("> [INFO".ljust(logWidth) + "]: " + str(message))


def print_player(message, player):
  concatP = "> [PLAYER %d (%d)" % (player.id, player.hand.size)
  print(concatP.ljust(logWidth) + "]: " + str(message))


def print_deck(message):
  print("> [DECK".ljust(logWidth) + "]: " + str(message))


def print_slaprule(message):
  print("> [SLAP RULE".ljust(logWidth) + "]: " + str(message))


def print_scoreboard(game):
  """Prints scores (# of cards) of each player"""
  scores = "; ".join(("Player " + str(i) + ": " + str(p.hand.size)) for i,p in enumerate(game.players))
  print(scores)


# DEBUG
def print_turns(game):
  x = "; ".join(("P" + str(i) + ": " + ("Yes" if (not q.empty()) else "No"))
                for i, q in enumerate(game.turns))
  x = "Whose turn - " + x
  print(x)


def print_turnsLeft(game):
  x = "; ".join(("P" + str(i) + ": " + str(p.turnsLeft))
                for i, p in enumerate(game.players))
  x = "Turns left - " + x
  print(x)