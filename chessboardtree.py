# chessboardtree.py

num_leaves = 0

import numpy as np
from chessboard import Chessboard

class ChessboardTree(Chessboard):

    def __init__(self, size):
        super().__init__(size)
        self._children = set()

    def depth_first_search(self):
        return self._dfs_recursive(depth=0) // 2

    def _dfs_recursive(self, depth):
        global num_leaves

        color = 'w' if (depth % 2 == 0) else 'b'
        
        # Get all valid moves
        moves = self.get_valid_moves(color)
        if len(moves) < 1:
            num_leaves += 1
            return depth  # if there are none, return
        
        # Create a child for each possible move
        children = [ChessboardTree(self._n) for move in moves]
        for child, move in zip(children, moves):
            child._set_board(self._board, self._attackedw, self._attackedb)
            child.add_piece(color, move)
            self._children.add(child)
        
        del children, moves

        return max(child._dfs_recursive(depth + 1) for child in self._children)

if __name__ == '__main__':
    global num_leaves

    n = 6

    cbt = ChessboardTree(n)

    print('n:', n)
    print('queens:', cbt.depth_first_search())
    print('leaves:', num_leaves)