import matplotlib.pyplot as plt
import numpy as np

def evaluate(data:dict):
    '''
    data:{real_pos:(calc_pos, dif), ...}
    '''
    if len(data) == 0:
        raise ValueError("Error input")
    real_x_data = [p[0] for p in data.keys()]
    real_y_data = [p[1] for p in data.keys()]
    calc_x_data = [p[0][0] for p in data.values()]
    calc_y_data = [p[0][1] for p in data.values()]
    average_dif = sum([p[1] for p in data.values()]) / len(data)
    plt.title('average_dif: ' + str(average_dif))
    if len(data) == 1:
        color = np.array(np.random.randint(0, 100))
    else:
        color = np.arange(0, 100, 100.0/(len(data)))
    sizesR = np.linspace(10, 10, len(data))
    sizesC = np.linspace(20, 20, len(data))
    plt.scatter(real_x_data, real_y_data, sizes=sizesR, c=color, cmap='viridis')
    plt.scatter(calc_x_data, calc_y_data, sizes=sizesC, c=color, cmap='viridis')
    plt.xlabel('x-coordinate')
    plt.ylabel('y-coordinate')
    plt.show()