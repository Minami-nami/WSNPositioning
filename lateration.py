from gen import pos
import sympy as sy
import math
import numpy as np

def least_square(A:np.matrix, b:np.matrix):
    # X = (A^TA)^-1A^Tb
    X = np.linalg.pinv(A).dot(b)
    return tuple(map(lambda x: float(x[0][0]), X))


def multilateration(RSSIs, params):
    '''
    RSSIs:[(id, rssi), ...]
    params:[(a, b), ...]
    len(RSSIs) >= 3
    '''
    # dist = 10 ^ ((RSSI - b) / a)
    edges = len(RSSIs)
    if edges <= 2:
        raise ValueError("Need more than 3 datas")
    dists = [math.pow(10, (rssi - params[id][1]) / params[id][0]) for id, rssi in RSSIs]
    positions = list(map(lambda x: pos[x], [pair[0] for pair in RSSIs]))
    xn, yn = positions.pop()
    dn = dists.pop()
    
    n = len(dists)
    A, b = [], []
    
    for i in range(n):
        A.append([2 * (positions[i][0] - xn), 2 * (positions[i][1] - yn)])
        b.append([np.square(positions[i][0] - xn) + np.square(positions[i][1] - yn) - np.square(dists[i] - dn)])
    
    A = np.matrix(A)
    b = np.matrix(b)
    # AX = b
    
    if len(RSSIs) > 3:
        return least_square(A, b)
    else:
        return tuple(map(lambda x: float(x[0][0]), np.linalg.inv(A).dot(b)))
    
if __name__ == '__main__':
    x, y = sy.symbols("x y")
    print(sy.solve([x**2+y**2-1, x-1], [x, y]))