class TicTacToe():

    WIN_COMBIN = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]

    def __init__(self, ary=[' '] * 9):
        self.board = ary

    def __str__(self):
        return_ary = [f" {self.board[3*i]} | {self.board[3*i + 1]} | {self.board[3*i + 2]} "
                      for i in range(3)]
        for i in (2, 1):
            return_ary.insert(i, '-'*11)
        return '\n'.join(return_ary)

    def clear(self):
        self.board = [' '] * 9

    def clone(self):
        cloned_board = list(self.board)
        return TicTacToe(cloned_board)

    def turn_number(self):
        return 9 - self.board.count(' ')

    def current_player(self):
        return {0: 'X', 1: 'O'}[self.turn_number() % 2]

    def won(self):
        ret = False
        for combin in self.WIN_COMBIN:
            if [self.board[i] for i in combin] in [['X']*3, ['O']*3]:
                ret = True
        return ret

    def winner(self):
        for combin in self.WIN_COMBIN:
            if [self.board[i] for i in combin] in [['X']*3, ['O']*3]:
                return self.board[combin[0]]

    def over(self):
        return self.won() or self.turn_number() == 9

    def drawn(self):
        return self.over() and not self.won()

    def possible_moves(self):
        return list(filter(lambda m: self.board[m] == ' ', range(9)))

    def valid_move(self, move):
        return 0 <= move <= 8 and move in self.possible_moves()

    def move(self, move):
        token = self.current_player()
        if self.valid_move(move):
            self.board[move] = token
            return self
        else:
            raise AttributeError('Invalid Move')
