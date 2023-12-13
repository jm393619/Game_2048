import random


class Game:
    def __init__(self, dim):
        self.dim = dim
        self.board = self.new_board()

        self.set_number(5)

        self.cache = self.set_cache()

    def set_cache(self):
        to_ret = {}

        for i in range(1, len(self.board)):
            for j in range(1, len(self.board)):
                to_ret[f"{i}-{j}"] = self.board[i][j]

        return to_ret

    def new_board(self):
        to_ret = [[1]*(self.dim+2)]

        for i in range(self.dim):
            to_ret.append([1] + [0]*self.dim + [1])

        to_ret.append([1]*(self.dim+2))
        return to_ret

    def set_number(self, n):

        lst = self.zeros()

        if len(lst) >= n:

            for i in random.sample(lst, k=n):

                a, b = i.split('-')
                self.board[int(a)][int(b)] = 2

        else:
            return None

    def zeros(self):

        lst = []

        board_len = len(self.board)

        for i in range(1, board_len):
            for j in range(1, board_len):
                if self.board[i][j] == 0:
                    lst.append(f"{i}-{j}")

        return lst

    def __str__(self):

        to_ret = ''
        for i in self.board:
            to_ret += f"{i}"
            to_ret += '\n'

        return to_ret

    def move_left(self):

        was_shift = False

        for k in range(1, len(self.board[0]) - 1):

            i = 1
            j = 2

            while j < len(self.board)-1:

                if self.board[k][j] != 0:

                    if self.board[k][j] != self.board[k][i]:
                        if self.board[k][i] == 0:
                            self.board[k][i] = self.board[k][j]
                            self.board[k][j] = 0
                            was_shift = True

                        else:
                            if j-i != 1:
                                i += 1
                                self.board[k][i] = self.board[k][j]
                                self.board[k][j] = 0
                                was_shift = True
                            else:
                                i += 1

                    elif self.board[k][j] == self.board[k][i]:
                        self.board[k][i] *= 2
                        i += 1
                        self.board[k][j] = 0
                        was_shift = True

                j += 1

        return was_shift

    def move_right(self):

        was_shift = False

        for k in range(1, len(self.board[0]) - 1):
            i = self.dim
            j = self.dim-1

            while j > 0:

                if self.board[k][j] != 0:

                    if self.board[k][j] != self.board[k][i]:
                        if self.board[k][i] == 0:
                            self.board[k][i] = self.board[k][j]
                            self.board[k][j] = 0
                            was_shift = True

                        else:
                            if i - j != 1:
                                i -= 1
                                self.board[k][i] = self.board[k][j]
                                self.board[k][j] = 0
                                was_shift = True
                            else:
                                i -= 1

                    elif self.board[k][j] == self.board[k][i]:
                        self.board[k][i] *= 2
                        i -= 1
                        self.board[k][j] = 0
                        was_shift = True

                j -= 1

        return was_shift

    def move_up(self):

        was_shift = False

        for k in range(1, len(self.board[0])-1):
            i = 1
            j = 2

            while j < len(self.board) - 1:

                # print(f"{i}-{j}")
                if self.board[j][k] != 0:

                    if self.board[j][k] != self.board[i][k]:
                        if self.board[i][k] == 0:
                            self.board[i][k] = self.board[j][k]
                            self.board[j][k] = 0
                            was_shift = True

                        else:
                            if j - i != 1:

                                i += 1
                                self.board[i][k] = self.board[j][k]
                                self.board[j][k] = 0
                                was_shift = True
                            else:
                                i += 1

                    elif self.board[j][k] == self.board[i][k]:
                        self.board[i][k] *= 2
                        i += 1
                        self.board[j][k] = 0
                        was_shift = True

                j += 1
        return was_shift

    def move_down(self):

        was_shift = False

        for k in range(1, len(self.board[0])-1):
            i = self.dim
            j = self.dim-1

            while j > 0:

                if self.board[j][k] != 0:

                    if self.board[j][k] != self.board[i][k]:
                        if self.board[i][k] == 0:
                            self.board[i][k] = self.board[j][k]
                            self.board[j][k] = 0
                            was_shift = True

                        else:
                            if i - j != 1:
                                i -= 1
                                self.board[i][k] = self.board[j][k]
                                self.board[j][k] = 0
                                was_shift = True
                            else:
                                i -= 1

                    elif self.board[j][k] == self.board[i][k]:
                        self.board[i][k] *= 2
                        i -= 1
                        self.board[j][k] = 0
                        was_shift = True

                j -= 1
        return was_shift

    def is_zero_in(self):
        f = False
        for i in self.board:
            if 0 in i:
                f = True
                break
        return f

    def is_game_over(self):

        f = self.is_zero_in()

        if f:
            return False

        else:

            for i, j in enumerate(self.board[1:-1], 1):
                for k, l in enumerate(j[1:-1], 1):
                    c1 = self.board[i][k + 1] == l
                    c2 = self.board[i+1][k] == l

                    if c1 is True or c2 is True:
                        return False

            return True

    def start_game(self):

        print('-'*30)
        print(self)

        d = {'a': self.move_left, 'w': self.move_up, 'd': self.move_right, 's': self.move_down}

        while True:

            direction = input('Choose direction: ').lower()

            d[direction]()
            self.set_number(1)
            print('-' * 30)
            print(self)

    def new_game(self):
        self.board = self.new_board()
        self.set_number(5)


if __name__ == '__main__':

    game = Game(4)
    game.start_game()
