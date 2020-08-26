from src.Agent import Agent
from src.TicTacToe import TicTacToe


board1 = ['X', 'X', ' ', 'O', 'O', ' ', ' ', ' ', ' ']
drawn_board = ['X', 'X', 'O', 'O', 'O', 'X', 'X', 'X', 'O']
board_O = ['X', 'X', 'O', 'X', 'O', ' ', 'O', ' ', ' ']
O_to_win = ['X', 'X', 'O', 'X', 'O', ' ', ' ', ' ', ' ']

newgame = TicTacToe()
game1 = TicTacToe(board1)
drawn_game = TicTacToe(drawn_board)
game_o = TicTacToe(board_O)
game_o_to_win = TicTacToe(O_to_win)

agentx = Agent()
agento = Agent(token='O')


def test_eval_game_over():
    assert agentx.eval_game_over(drawn_game) == 0
    assert agentx.eval_game_over(game_o) == -10
    assert agento.eval_game_over(game_o) == 10


def test_eval():
    assert agentx.eval(game1) == 9
    assert agento.eval(game1) == -9

def test_choose_move():
    assert agentx.choose_move(game1) == 2
    assert agento.choose_move(game_o_to_win) == 6

def test_block_win():
    board = ['X', 'X', ' ', ' ', 'O', ' ', ' ', ' ', ' ']
    game = TicTacToe(board)

    assert agento.choose_move(game) == 2
