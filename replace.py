from gen import index

mp = {v: k for k, v in index.items()}

if __name__ == '__main__':
    with open('./data/2.txt', 'r', encoding='UTF-8') as file, open('./data/temp.txt', 'w') as data:
            position = []
            for line in file:
                curline = ''
                if line == '#\n' or line == '#':
                    data.write(line)
                    continue
                else:
                    data.write('{')
                    token = line[1:-2].split(' ')
                    position = token[0][1:-1].split(',')
                    data.write('(' + ','.join(position) + ')')
                    for dist in token[1:]:
                        pair = dist[1:-1].split(',')
                        pair = (int(pair[0]), pair[1])
                        if pair[0] not in mp:
                            continue
                        pair = (mp[pair[0]], pair[1])
                        data.write(' (' + ','.join(list(pair)) + ')')
                    data.write('}\n')