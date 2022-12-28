import numpy as np
import matplotlib.pyplot as plt
from filter import Gaussian_filtering
index = {'FE:18:FE:AC:CA:E4':1 , 'E9:7A:DF:3E:53:8D':2 , 'E3:62:47:30:DE:6C':3 , 
         'D3:10:7E:CD:51:A2':4 , 'D9:F8:2F:94:4D:C2':5 , 'FC:60:5F:4C:CF:D4':6 ,
         'EA:08:B1:68:E7:88':7 , 'D8:DF:B3:A6:33:8F':8 , '12:3B:6A:1B:48:5D':9}

pos =  {1: (4.8, 1.8) , 2: (1.8, 1.8) , 3: (4.8, 4.8) , 
        4: (1.8, 4.8) , 5: (4.8, 7.8) , 6: (1.8, 7.8) ,
        7: (4.8, 13.8), 8: (1.8, 13.8), 9: (7.25, 6.25)}

data_index = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 19, 20]


def gendata():
    '''
    生成原始数据
    '''
    open("./data/data.txt", 'w').close()
    for i in data_index:
        with open('./data/' + str(i) + '.txt', 'r', encoding='UTF-8') as file:
            cur = {}
            position = []
            for line in file:
                if line == '#\n' and len(position) != 0:
                    with open('./data/data.txt', 'a', encoding='UTF-8') as data:
                        data.write('(' + ','.join(position) + ') ')
                        data.write(' '.join(['(' + ','.join([str(key), str(v)]) + ')' for key, value in cur.items() for v in value]))
                        data.write('\n')
                        cur.clear()
                else:
                    token = line[1:-2].split(' ')
                    position = token[0][1:-1].split(',')
                    for dist in token[1:]:
                        pair = dist[1:-1].split(',')
                        if pair[0] not in index:
                            continue
                        pair = (index[pair[0]], float(pair[1]))
                        if pair[0] in cur:
                            cur[pair[0]].append(pair[1])
                        else:
                            cur[pair[0]] = [pair[1]]


def calc_dist(point1, point2):
    '''
    point* : (x, y) 
    计算距离
    '''
    return np.sqrt(np.square(point1[0] - point2[0]) + np.square(point1[1] - point2[1]))


def gentest():
    '''
    生成测试文件
    '''
    with open('./data/data.txt', 'r', encoding='UTF-8') as file, open('./data/test.txt', 'w', encoding='UTF-8') as test:
        for line in file:
            data = {}
            if line == '\n':
                continue
            token = line[:-1].split(' ')
            position = tuple(map(float, token[0][1:-1].split(',')))
            for dist in token[1:]:
                id, RSSI = tuple(dist[1:-1].split(','))
                id, RSSI = int(id), float(RSSI)
                if id in data:
                    data[id].append(RSSI)
                else:
                    data[id] = [RSSI]
            data = {k: Gaussian_filtering(v) for k, v in data.items()}
            data = {k: v for k, v in data.items() if v == v}
            if (len(data) < 3):
                continue
            test.write('(' + str(position[0]) + ',' + str(position[1]) + ') ')
            test.write(' '.join(['(' + ','.join([str(key), str(value)]) + ')' for key, value in data.items()]))
            test.write('\n')

def genparam():
    '''
    生成参数
    '''
    data = {i:[] for i in range(1, 10)}
    with open('./data/data.txt', 'r', encoding='UTF-8') as file:
        for line in file:
            if line == '\n':
                continue
            token = line[:-1].split(' ')
            position = tuple(map(float, token[0][1:-1].split(',')))
            for dist in token[1:]:
                id, RSSI = tuple(dist[1:-1].split(','))
                id, RSSI = int(id), float(RSSI)
                data[id].append(tuple([calc_dist(pos[id], position), RSSI]))
    open('./data/param.txt', 'w', encoding='UTF-8').close()
    
    for id in range(1, 10):
        dist_rssi = {}
        
        for dist, rssi in data[id]:
            if dist in dist_rssi:
                dist_rssi[dist].append(rssi)
            else:
                dist_rssi[dist] = [rssi]
                
        for key in dist_rssi.keys():
            dist_rssi[key] = Gaussian_filtering(dist_rssi[key])
            
        dist_rssi = dict(sorted({k: v for k, v in dist_rssi.items() if v == v}.items(), key=lambda item: item[0]))
        if len(dist_rssi) == 0:
            continue
        with open('./data/param.txt', 'a', encoding='UTF-8') as file:
            # RSSI = a * log(dist) + b
            x_data = np.array(list(dist_rssi.keys()))
            y_data = np.array(list(dist_rssi.values()))
            log_x_data = np.log10(x_data)
            param = np.polyfit(log_x_data, y_data, 1)
            file.write(str(id) + ' ')
            file.write(' '.join([str(i) for i in param]))
            file.write('\n')
            fitting_y_data = np.array(list(map(lambda x: param[0] * x + param[1], log_x_data)))
            plt.title('sensor ' + str(id))
            plt.xlabel('dist')
            plt.ylabel('RSSI')
            plt.plot(x_data, y_data, '.b-')
            plt.plot(x_data, fitting_y_data, '.g-.')
            plt.show()

if __name__ == '__main__':
    gendata()
    genparam()
    gentest()
