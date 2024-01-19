##
## Player config
##
MIN_USERNAME_LEN    = 2     # Minimum length of usernames
MAX_PLAYER_HEALTH   = 1000  # Maximum health
MAX_STUNNED_ROUNDS  = 10    # Max amount of rounds a player can be stunned

##
## Spells config
##
CHANCE_HEAL_PARTLY          = 25 # Percentage chance a player is healed with 5% of max health when using a defensive spell
CHANCE_HEAL_FULLY           = 5  # Percentage chance a player is fully healed when using a defensive spell
MAX_LEVENSHTEIN_DISTANCE    = 0  # Max Levenshtein distance (max amount of typos a user can make) before considering a spell fails. Setting this to 0 disables it (and in that case also doesn't require the levenshtein package)

##
## Misc
##
DEBUG_MODE = False          # Enable or disable debug mode. Sets all spell chances to 100% when enabled