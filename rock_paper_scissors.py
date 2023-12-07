cartridge = {
  "START": {
    "prompt": "You are an AI game of Rock, Paper Scissors. Ask the user to play their hand, either rock, paper, or scissors.",
    "events": [
      { 
        "method": "chooses_rock",
        "user_behavior": "Chooses rock",
        "target": "SECOND_PLAYER_AGAINST_ROCK"
      },
      { 
        "method": "chooses_paper",
        "user_behavior": "Chooses paper",
        "target": "SECOND_PLAYER_AGAINST_PAPER"
      },
      { 
        "method": "chooses_scissors",
        "user_behavior": "Chooses scissors",
        "target": "SECOND_PLAYER_AGAINST_SCISSORS"
      },
    ]
  },
  "SECOND_PLAYER_AGAINST_PAPER": {
    "prompt": "You are an AI game of Rock, Paper Scissors. The first player has already chosen Paper. Now you need to ask the second player what they will choose.",
    "events": [
      { 
        "method": "chooses_rock",
        "user_behavior": "Chooses rock",
        "target": "FIRST_PLAYER_WINS"
      },
      { 
        "method": "chooses_paper",
        "user_behavior": "Chooses paper",
        "target": "TIE"
      },
      { 
        "method": "chooses_scissors",
        "user_behavior": "Chooses scissors",
        "target": "SECOND_PLAYER_WINS"
      },
    ]
  },
  "SECOND_PLAYER_AGAINST_ROCK": {
    "prompt": "You are an AI game of Rock, Paper Scissors. The first player has already chosen Rock. Now you need to ask the second player what they will choose.",
    "events": [
      { 
        "method": "chooses_rock",
        "user_behavior": "Chooses rock",
        "target": "TIE"
      },
      { 
        "method": "chooses_paper",
        "user_behavior": "Chooses paper",
        "target": "SECOND_PLAYER_WINS"
      },
      { 
        "method": "chooses_scissors",
        "user_behavior": "Chooses scissors",
        "target": "FIRST_PLAYER_WINS"
      },
    ]
  },
  "SECOND_PLAYER_AGAINST_SCISSORS": {
    "prompt": "You are an AI game of Rock, Paper Scissors. The first player has already chosen scissors. Now you need to ask the second player what they will choose.",
    "events": [
      { 
        "method": "chooses_rock",
        "user_behavior": "Chooses rock",
        "target": "SECOND_PLAYER_WINS"
      },
      { 
        "method": "chooses_paper",
        "user_behavior": "Chooses paper",
        "target": "FIRST_PLAYER_WINS"
      },
      { 
        "method": "chooses_scissors",
        "user_behavior": "Chooses scissors",
        "target": "TIE"
      },
    ]
  },
  "FIRST_PLAYER_WINS": {
    "prompt": "You are an AI game of Rock, Paper Scissors. The first player has won. Let them know they won.",
    "events": [{
      "method": "restart",
      "user_behavior": "Chooses to play again",
      "target": "START"
    }]
  },
  "SECOND_PLAYER_WINS": {
    "prompt": "You are an AI game of Rock, Paper Scissors. The second player has won. Let them know they won.",
    "events": [{
      "method": "restart",
      "user_behavior": "Chooses to play again",
      "target": "START"
    }]
  }
}