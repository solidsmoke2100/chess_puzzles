import numpy as np

A250000 = (0, 0, 1, 2, 4, 5, 7, 9, 12, 14, 17, 21, 24, 28, 32)

def exclude_squares(pos):
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

def transform(config, sym='i', bw=False):
    board_w = np.asarray([0 if i in config[1] else 1 for i in range(n * n)]).reshape((n, n))
    board_b = np.asarray([0 if i in config[2] else 1 for i in range(n * n)]).reshape((n, n))
    if bw:
        board_w, board_b = board_b, board_w

    if sym == 'i':
        return [config[0],
            set(np.where(board_w == 0)[0]),
            set(np.where(board_b == 0)[0])]
    if sym == 'x':
        return [config[0],
            set(np.where(board_w[::-1, ::] == 0)[0]),
            set(np.where(board_b[::-1, ::] == 0)[0])]
    if sym == 'y':
        return [config[0],
            set(np.where(board_w[::, ::-1] == 0)[0]),
            set(np.where(board_b[::, ::-1] == 0)[0])]
    if sym == 'd1':
        return [config[0],
            set(np.where(board_w.T == 0)[0]),
            set(np.where(board_b.T == 0)[0])]
    if sym == 'd2':
        return [config[0],
            set(np.where(board_w[::-1, ::-1].T == 0)[0]),
            set(np.where(board_b[::-1, ::-1].T == 0)[0])]
    if sym == 'r90':
        return [config[0],
            set(np.where(np.rot90(board_w, k=1) == 0)[0]),
            set(np.where(np.rot90(board_b, k=1) == 0)[0])]
    if sym == 'r180':
        return [config[0],
            set(np.where(np.rot90(board_w, k=2) == 0)[0]),
            set(np.where(np.rot90(board_b, k=2) == 0)[0])]
    if sym == 'r270':
        return [config[0],
            set(np.where(np.rot90(board_w, k=3) == 0)[0]),
            set(np.where(np.rot90(board_b, k=3) == 0)[0])]

def hash_board(board):
    symmetries = ['i', 'x', 'y', 'd1', 'd2', 'r90', 'r180', 'r270']
    configs = [transform(board, sym=sym) for sym in symmetries] + \
              [transform(board, sym=sym, bw=True) for sym in symmetries]
    return min(hash((frozenset(config[1]), frozenset(config[2]))) for config in configs)

def max_army(board):
    #global num_leaves

    color =  1 if board[0] % 2 == 0 else 2
    moves = board[color]
    if len(moves) < 1:
        #num_leaves += 1
        return board[0]

    children = []
    if color == 1:
        children = [[board[0] + 1, board[1] - {move}, board[2] - exclude_squares(move)] for move in moves]
    if color == 2:
        children = [[board[0] + 1, board[1] - exclude_squares(move), board[2] - {move}] for move in moves]
    
    hash_set = set()
    for i in range(len(children)-1, -1, -1):
        if hash_board(children[i]) in hash_set:
            del children[i]
        else:
            hash_set.add(hash_board(children[i]))
    
    return max(max_army(child) for child in children)

n = 4
num_leaves = 0

# [depth, white's moves, black's moves]
board = [0, set(range(n * n)), set(range(n * n))]

import time
start = time.clock()
ans = max_army(board) // 2
elapsed = time.clock() - start
print(ans, ans == A250000[n-1])
#print(num_leaves)
print(elapsed)