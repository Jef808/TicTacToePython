from random import randrange as rand
# from random import choice


class Agent():

    def __init__(self, token='X'):
        self.token = token

    def agent_to_play(self, game):
        return self.token == game.current_player()

    def eval_game_over(self, game):
        score = 0
        if game.won():
            score = {False: 10, True: -10}[self.agent_to_play(game)]
        else:
            score = 0
        return score

    def eval(self, game):
        if game.over():
            return self.eval_game_over(game)
        else:
            if self.agent_to_play(game):
                return max(self.eval(game.clone().move(mov)) for mov in game.possible_moves())-1
            else:
                return min(self.eval(game.clone().move(mov)) for mov in game.possible_moves())+1

    def choose_move(self, game):
        if game.turn_number() == 0:
            return rand(9)
        if game.turn_number() == 1:
            return 4 if game.valid_move(4) else 0
        return max(game.possible_moves(), key=lambda m: self.eval(game.clone().move(m)))
