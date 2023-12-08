cartridge = {
  "START": {
    "role": "You are an AI game of Rock, Paper Scissors.",
    "prompt": "Ask the user to play their hand, either rock, paper, or scissors.",
    "events": [
      { 
        "method": "chooses_rock",
        "if_the_user": "Chooses rock",
        "target": "SECOND_PLAYER_AGAINST_ROCK"
      },
      { 
        "method": "chooses_paper",
        "if_the_user": "Chooses paper",
        "target": "SECOND_PLAYER_AGAINST_PAPER"
      },
      { 
        "method": "chooses_scissors",
        "if_the_user": "Chooses scissors",
        "target": "SECOND_PLAYER_AGAINST_SCISSORS"
      },
    ]
  },
  "SECOND_PLAYER_AGAINST_PAPER": {
    "prompt": "The first player has already chosen Paper. Now you need to ask the second player what they will choose.",
    "events": [
      { 
        "method": "chooses_rock",
        "if_the_user": "Chooses rock",
        "target": "FIRST_PLAYER_WINS"
      },
      { 
        "method": "chooses_paper",
        "if_the_user": "Chooses paper",
        "target": "TIE"
      },
      { 
        "method": "chooses_scissors",
        "if_the_user": "Chooses scissors",
        "target": "SECOND_PLAYER_WINS"
      },
    ]
  },
  "SECOND_PLAYER_AGAINST_ROCK": {
    "prompt": "The first player has already chosen Rock. Now you need to ask the second player what they will choose.",
    "events": [
      { 
        "method": "chooses_rock",
        "if_the_user": "Chooses rock",
        "target": "TIE"
      },
      { 
        "method": "chooses_paper",
        "if_the_user": "Chooses paper",
        "target": "SECOND_PLAYER_WINS"
      },
      { 
        "method": "chooses_scissors",
        "if_the_user": "Chooses scissors",
        "target": "FIRST_PLAYER_WINS"
      },
    ]
  },
  "SECOND_PLAYER_AGAINST_SCISSORS": {
    "prompt": "The first player has already chosen scissors. Now you need to ask the second player what they will choose.",
    "events": [
      { 
        "method": "chooses_rock",
        "if_the_user": "Chooses rock",
        "target": "SECOND_PLAYER_WINS"
      },
      { 
        "method": "chooses_paper",
        "if_the_user": "Chooses paper",
        "target": "FIRST_PLAYER_WINS"
      },
      { 
        "method": "chooses_scissors",
        "if_the_user": "Chooses scissors",
        "target": "TIE"
      },
    ]
  },
  "FIRST_PLAYER_WINS": {
    "prompt": "The first player has won. Let them know they won.",
    "events": [{
      "method": "restart",
      "if_the_user": "Chooses to play again",
      "target": "START"
    }]
  },
  "SECOND_PLAYER_WINS": {
    "prompt": "The second player has won. Let them know they won.",
    "events": [{
      "method": "restart",
      "if_the_user": "Chooses to play again",
      "target": "START"
    }]
  }
}