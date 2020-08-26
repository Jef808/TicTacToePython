import re
import sys
from TicTacToe import TicTacToe
from Agent import Agent


def greet_user():
    print("Hi! Welcome to Tic-Tac-Toe! \n")


def prompt_play():
    print("Would you like to play a game (Y/n)? \n")
    _in = input()
    if re.match("n", _in, re.I):
        sys.exit("Ok, too bad :(")
    else:
        return True


def explain_game():
    print("""Enter your moves by choosing the corresponding square:
(1 corresponds to the upper left square, 5 to the middle square, and 9 to the lower right square.) \n""")


def switch_token(token):
    return {'X': 'O', 'O': 'X'}[token]


def prompt_token():
    print("Would you like to play as 'X' or as 'O' (X/O)? \n")
    _in = input()
    if re.match("x", _in, re.I):
        return 'X'
    elif re.match("o", _in, re.I):
        return 'O'
    else:
        print("Invalid entry, please enter either 'X' or 'O' \n")
        return prompt_token()


def prompt_move():
    print("Choose your next move! \n")
    _in = input()
    while not re.match("[1-9]", _in):
        print("Invalid move, please choose a number from 1 to 9. \n")
        _in = input()
    return int(_in)-1


def play_turn(agent, game):
    if game.current_player() == agent.token:
        mov = agent.choose_move(game)
        game.move(mov)
    else:
        print(game, "\n")
        mov = prompt_move()
        while not game.valid_move(mov):
            print("That square is taken! \n")
            mov = prompt_move()
        game.move(mov)


def play_game(player_token):
    agent = Agent(switch_token(player_token))
    game = TicTacToe([' ']*9)
    while not game.over():
        play_turn(agent, game)
    print(game)
    if game.won():
        winner = game.winner()
        print(f"Better luck next time! {winner} wins!\n")
    else:
        print("Game ends in a draw!\n")


if __name__ == '__main__':
    greet_user()
    play = prompt_play()

    while play:
        token = prompt_token()
        explain_game()
        play_game(token)
        play = prompt_play()
