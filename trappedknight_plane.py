# trappedknight_quadrant.py

import numpy as np
import matplotlib.pyplot as plt

def generate_spiral(n):
    i = 0
    valdict = {}
    x, y = (0, 0)
    step = 1
    index = 1
    for i in range(2 * n):
        for j in range(i+1):
            valdict[(x,y)] = index
            x += step
            index += 1
        for j in range(i+1):
            valdict[(x,y)] = index
            y += step
            index += 1
        step *= -1
    return valdict

spiraldict = generate_spiral(100)

visited = set()

xs = np.zeros(1)
ys = np.zeros(1)
x = xs[0]
y = ys[0]

visited.add((x, y))

for i in range(10000):

    # Calculate all valid moves from current position
    moves = [(x+1, y+2), (x+2, y+1), (x+2, y-1), (x+1, y-2),
             (x-1, y-2), (x-2, y-1), (x-2, y+1), (x-1, y+2)]
    moves = [mv for mv in moves if not mv in visited]

    # Find move with smallest value
    values = [spiraldict[(int(u),int(v))] for (u,v) in moves]
    if len(values) < 1:
        break  # stop when there are no valid moves
    minval = 10 ** 7
    minpos = 0
    for j in range(len(values)):
        if values[j] < minval:
            minval = values[j]
            minpos = j

    # Move to new position; store position for plotting
    x, y = moves[minpos]
    xs = np.append(xs, x)
    ys = np.append(ys, y)

    # Mark current square as visited
    visited.add((x, y))

fig = plt.figure()
plt.plot(xs, ys, linewidth=1, c='k')
plt.scatter(xs, ys, s=5,
    c=np.linspace(0, 1, len(xs)),
    cmap=plt.cm.spring, zorder=10000)
plt.scatter(xs[-1], ys[-1], s=50, c='r', marker='x', zorder=20000)
plt.show()