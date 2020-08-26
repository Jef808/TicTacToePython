from src.TicTacToe import TicTacToe
import pytest

board1 = ['X', 'X', ' ', ' ', 'O', ' ', ' ', ' ', ' ']
drawn_board = ['X', 'X', 'O', 'O', 'O', 'X', 'X', 'X', 'O']
board_O = ['X', 'X', 'O', 'X', 'O', ' ', 'O', ' ', ' ']

newgame = TicTacToe()
game1 = TicTacToe(board1)
drawn_game = TicTacToe(drawn_board)
game_o = TicTacToe(board_O)


def test_newgame():
    assert newgame.board == [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
    assert game1.board == ['X', 'X', ' ', ' ', 'O', ' ', ' ', ' ', ' ']


def test_str(capsys):
    print(game1)
    captured = capsys.readouterr()
    assert captured.out == """ X | X |   \n-----------
   | O |   \n-----------
   |   |   \n"""


def test_clone():
    game2 = game1.clone()
    assert game1.board == game2.board
    assert game1 is not game2


def test_turn_number():
    assert newgame.turn_number() == 0
    assert game1.turn_number() == 3
    assert drawn_game.turn_number() == 9


def test_current_player():
    assert newgame.current_player() == 'X'
    assert game1.current_player() == 'O'


def test_won():
    board2 = ['X', 'X', 'X', ' ', 'O', 'O', ' ', ' ', ' ']

    game2 = TicTacToe(board2)

    assert game1.won() is False
    assert game2.won() is True
    assert game_o.won() is True


def test_winner():
    assert game_o.winner() == 'O'


def test_drawn():
    assert drawn_game.drawn() is True
    assert game1.drawn() is False


def test_over():
    assert game1.over() is False
    assert drawn_game.over() is True


def test_possible_moves():
    assert newgame.possible_moves() == [0, 1, 2, 3, 4, 5, 6, 7, 8]
    assert game1.possible_moves() == [2, 3, 5, 6, 7, 8]


def test_valid_move():
    assert game1.valid_move(2) is True
    assert game1.valid_move(4) is False
    assert game1.valid_move(11) is False


def test_move():
    assert game1.move(2).board == ['X', 'X', 'O', ' ', 'O', ' ', ' ', ' ', ' ']
    with pytest.raises(AttributeError) as excinfo:
        game1.move(2)
        assert "Invalid Move" in str(excinfo.value)
