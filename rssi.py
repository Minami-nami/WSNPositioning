from lateration import multilateration
from gen import calc_dist
from evaluate import evaluate


if __name__ == '__main__':
    params = {}
    with open('./data/param.txt', 'r') as file:
        for line in file:
            if (line == '\n'):
                continue
            token = line[:-1].split(' ')
            params[int(token[0])] = tuple(map(float, token[1:]))
    testdata = {}
    with open('./data/test.txt', 'r', encoding='UTF-8') as file:
        for line in file:
            if line == '\n':
                continue
            token = line[:-1].split(' ')
            # position = tuple(map(float, token[0][1:-1].split(',')))
            position = tuple(token[0][1:-1].split(','))
            testdata[position] = []
            ref = testdata[position]
            for dist in token[1:]:
                id, RSSI = tuple(dist[1:-1].split(','))
                ref.append((int(id), float(RSSI)))
    result, dif = {}, []
    line = 1
    for k, v in testdata.items():
        locate = multilateration(v, params)
        # result[k] = (locate, calc_dist(locate, k))
        result[k] = (k, locate)
        print('given_pos:', k, 'calc_pos:', locate)
        line += 1
    # evaluate(result)