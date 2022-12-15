import numpy as np

def Gaussian_filtering(data):
    # 高斯滤波 过滤异常值
    mean = np.mean(data)
    std = np.std(data)
    temp = np.array(data)
    
    #［μ+0.15σ, μ+3.09σ］
    # temp = np.extract((temp > mean + 0.15 * std) & (temp < mean + 3.09 * std), temp)
    
    # [μ-2σ, μ+2σ］
    # temp = np.extract((temp > mean - 2 * std) & (temp < mean + 2 * std), temp)
    
    # [μ-3σ, μ+3σ］
    temp = np.extract((temp > mean - 3 * std) & (temp < mean + 3 * std), temp)
    
    # 取平均
    return np.mean(temp)