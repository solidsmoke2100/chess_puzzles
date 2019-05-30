# chessboard.py
# Refer to OEIS A250000

import numpy as np

A250000 = (0, 0, 1, 2, 4, 5, 7, 9, 12, 14, 17, 21, 24, 28, 32)

class Chessboard():
    
    def __init__(self, size):
        self._n = size
        self._m = 0
        self._board = np.zeros((size, size), int)
        self._attackedb = np.zeros((size, size), bool)
        self._attackedw = np.zeros((size, size), bool)

    def __str__(self):
        return str(self._board)

    def __repr__(self):
        return str(self._board)

    def __hash__(self):
        return min(hash(tuple(self.transform(sym).flatten())) for sym in
            ['i', 'bw', 'x', 'y', 'd1', 'd2', 'r90', 'r180', 'r270', ('x', 'bw'), ('y', 'bw'), ('d1', 'bw'), ('d2', 'bw'), ('r90', 'bw'), ('r180', 'bw'), ('r270', 'bw')])

    def __eq__(self, other):
        """Chessboards are treated as equivalent if they are in the same symmetry class"""
        return (type(other) == type(self)) and (self._n == other._n) and (hash(other) == hash(self))

    def get_board(self):
        return self._board

    def _set_board(self, board, attkw, attkb):
        self._board = np.copy(board)
        self._attackedw = np.copy(attkw)
        self._attackedb = np.copy(attkb)

    def get_attacked_squares(self, color):
        if color == 'w':
            return self._attackedw
        if color == 'b':
            return self._attackedb

    def get_max_queens(self):
        return self._m

    def reset(self):
        """Clears all pieces off the board"""
        self._board = np.zeros((self._n, self._n), int)
        self._attackedb = np.zeros((self._n, self._n), bool)
        self._attackedw = np.zeros((self._n, self._n), bool)

    def _is_attacked(self, color, pos):
        """Returns boolean indicating whether the specified position is attacked by a queen of the specified color"""
        if color == 'w':
            return self._attackedw[pos]
        if color == 'b':
            return self._attackedb[pos]

    def _update_attack(self, color, pos):
        """Update attacked arrays after adding a queen"""
        if color == 'w':
            attk = self._attackedw
            val = 1
        if color == 'b':
            attk = self._attackedb
            val = 2

        (y, x) = pos
        
        # left
        for i in range(x, -1, -1):
            attk[y, i] = True
            if i != x and self._board[y, i] == val:
                break  # if we encounter another queen of the same color, break

        # right
        for i in range(x, self._n):
            attk[y, i] = True
            if i != x and self._board[y, i] == val:
                break  # if we encounter another queen of the same color, break

        # up
        for j in range(y, -1, -1):
            attk[j, x] = True
            if j != y and self._board[j, x] == val:
                break  # if we encounter another queen of the same color, break

        # down
        for j in range(y, self._n):
            attk[j, x] = True
            if j != y and self._board[j, x] == val:
                break  # if we encounter another queen of the same color, break

        # upleft
        i = x
        j = y
        while i >= 0 and j >= 0:
            attk[j, i] = True
            if (j, i) != (y, x) and self._board[j, i] == val:
                break  # if we encounter another queen of the same color, break
            i -= 1
            j -= 1

        # upright
        i = x
        j = y
        while i < self._n and j >= 0:
            attk[j, i] = True
            if (j, i) != (y, x) and self._board[j, i] == val:
                break  # if we encounter another queen of the same color, break
            i += 1
            j -= 1

        # downleft
        i = x
        j = y
        while i >= 0 and j < self._n:
            attk[j, i] = True
            if (j, i) != (y, x) and self._board[j, i] == val:
                break  # if we encounter another queen of the same color, break
            i -= 1
            j += 1

        # upleft
        i = x
        j = y
        while i < self._n and j < self._n:
            attk[j, i] = True
            if (j, i) != (y, x) and self._board[j, i] == val:
                break  # if we encounter another queen of the same color, break
            i += 1
            j += 1

    def get_valid_moves(self, color):
        if color == 'w':
            arr = np.asarray(np.where((self._attackedb == 0) * (self._board == 0))).transpose()
            np.random.shuffle(arr)
            return [tuple(mv) for mv in arr]
        if color == 'b':
            arr = np.asarray(np.where((self._attackedw == 0) * (self._board == 0))).transpose()
            np.random.shuffle(arr)
            return [tuple(mv) for mv in arr]

    def add_piece(self, color, pos):
        """Add a queen of the specified color to the chessboard"""
        if (color == 'w') and (not self._is_attacked('b', pos)):
            self._board[pos] = 1
            self._update_attack('w', pos)
            return True
        if (color == 'b') and (not self._is_attacked('w', pos)):
            self._board[pos] = 2
            self._update_attack('b', pos)
            return True
        return False

    def populate_randomly(self):
        self.reset()

        num_queens = 0
        while num_queens < (self._n * self._n / 2):
            backup = np.copy(self._board)

            # Add white queen
            candidates = self.get_valid_moves('w')
            if len(candidates) < 1:
                self._board = backup
                break
            self.add_piece('w', candidates[0])
            
            # Add black queen
            candidates = self.get_valid_moves('b')
            if len(candidates) < 1:
                self._board = backup
                break
            self.add_piece('b', candidates[0])

            # If both succeed, increment number of queens
            num_queens += 1
        
        if num_queens > self._m:
            self._m = num_queens
        return num_queens

    def transform(self, symmetries):
        """Transform the board with respect to the specified symmetries"""

        if type(symmetries) == type(()) or type(symmetries) == type([]):
            result = self._board
            for sym in symmetries:
                result = self._transform_single(result, sym)
            return result
        else:
            return self._transform_single(self._board, symmetries)

    def _transform_single(self, board, sym):
        if sym == 'i':
            return board
        if sym == 'bw':
            w = board == 1
            b = board == 2
            return (w * 2) + (b * 1)
        if sym == 'x':
            return board[::-1, ::]
        if sym == 'y':
            return board[::, ::-1]
        if sym == 'd1':
            return board.T
        if sym == 'd2':
            return board[::-1, ::-1].T
        if sym == 'r90':
            return np.rot90(board, k=1)
        if sym == 'r180':
            return np.rot90(board, k=2)
        if sym == 'r270':
            return np.rot90(board, k=3)


class ChessboardCompressed():

    def __init__(self, n):
        self._n = n
        self._w = set(range(n * n))
        self._b = set(range(n * n))

    def print_set(self, s):
        print(np.asarray([i if i in s else -1 for i in range(self._n * self._n)]).reshape((self._n, self._n)))

    def reset(self):
        self._w = set(range(self._n * self._n))
        self._b = set(range(self._n * self._n))

    def exclude_squares(self, pos):
        n = self._n
        row = pos // n
        col = pos - (row * n)

        # Eight directions: up, down, left, right, leftup, leftdown, rightup, rightdown
        return {i for i in range(pos, -1, -n)} | \
               {i for i in range(pos, n * n, n)} | \
               {i for i in range(pos, int(np.floor(pos / n) * n) - 1, -1)} | \
               {i for i in range(pos, int(np.ceil((pos + 1) / n) * n), 1)} | \
               {pos - (i * (n + 1)) for i in range(col + 1)} | \
               {pos + (i * (n - 1)) for i in range(col + 1)} | \
               {pos - (i * (n - 1)) for i in range(n - col)} | \
               {pos + (i * (n + 1)) for i in range(n - col)}

    def populate_randomly(self):
        self.reset()
        for i in range(n * n):
            # Add white queen
            if len(self._w) < 1:
                return i
            pos = np.random.choice(tuple(self._w))
            self._w = self._w - {pos}
            self._b = self._b - self.exclude_squares(pos)
            # Add black queen
            if len(self._b) < 1:
                return i - 1
            pos = np.random.choice(tuple(self._b))
            self._b = self._b - {pos}
            self._w = self._w - self.exclude_squares(pos)

if __name__ == '__main__':
    import time

    n = 10  # board size
    N = 10000  # number of experiments

    cb = ChessboardCompressed(n)

    ans = max(cb.populate_randomly() for i in range(N))
    print(ans, ans == A250000[n-1])
    
    """
    cb = Chessboard(n)

    experiments = [None] * N
    for i in range(N):
        experiments[i] = (cb.populate_randomly(), cb.get_board())
        print(i+1, '/', N)
    
    boards = [b for (m,b) in experiments if m == cb.get_max_queens()]

    print("size:", n)
    print("num queens:", cb.get_max_queens(), 'exact:', A250000[n-1])
    print("experiments:", len(boards), '/', N, '=', round(len(boards) / N, 4))
    print(boards[0])
    """