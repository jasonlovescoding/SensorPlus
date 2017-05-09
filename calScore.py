import numpy as np

def calScore(data):
    ip1_W = np.load('weight\\ip1_W.npy')
    ip1_b = np.load('weight\\ip1_b.npy')
    ip2_W = np.load('weight\\ip2_W.npy')
    ip2_b = np.load('weight\\ip2_b.npy')
    ip3_W = np.load('weight\\ip3_W.npy')
    ip3_b = np.load('weight\\ip3_b.npy')
    data = np.dot(ip1_W, data) + ip1_b[:, None]
    data[data < 0]=0
    data = np.dot(ip2_W, data) + ip2_b[:, None]
    data[data < 0]=0
    data = np.dot(ip3_W, data) + ip3_b[:, None]
    data = np.exp(data)
    weightval = (data[0]*6+data[1]*7+data[2]*8+data[3]*9+data[4]*10)[0, 0]
    weightval = weightval / sum(data)[0,0]
    #print(sum(data))
    print('call calScore')
    print(data)
    maxval = np.argmax(data)
    if (data[maxval] <= data[2] + data[1]):
        if (data[2] > data[1]):
            maxval = 2
        else:
            maxval = 1
    return min(int(round(weightval)), maxval + 6)