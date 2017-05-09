import re
import random
import math
import matplotlib.pyplot as plt
import numpy as np
exec(open('calScore.py', 'r').read())
data = [700,565.256777185,545.471744387,528.741260761,460.439789868]

def filte(pitch):
    l,r = 0,0
    n = len(pitch)
    for i in range(0,n-1,1):
        if (pitch[i]>180):
            l = i
            break
    return l,l+149

def distance(S1_Ax,S1_Ay,S1_Az,tS1_Ax,tS1_Ay,tS1_Az):
    return math.sqrt((S1_Ax-tS1_Ax)**2+(S1_Ay-tS1_Ay)**2+(S1_Az-tS1_Az)**2)

def closest(x,ten,nine,eight,seven,six):
    temp = [abs(x-six),abs(x-seven),abs(x-eight),abs(x-nine),abs(x-ten)]
    return np.argmin(temp)+6
def _scoreAlg(activity,logReader):
    AcceleratedSpeed = []
    ret = re.compile(r":.*?\]")
    std = [] 
    # for index in range(110):
    #     AcceleratedSpeed = []
    #     with open(str(index)+".txt","r") as f:
    #         lines = f.readlines()
    #         if int(lines[-1])==10:
    #             pitch,sensor1,sensor2 = [],[],[]
    #             for line in lines:
    #                 temp = ret.findall(line
    #                 if 'roll1' in line:
    #                     pitch.append(float(temp[1][1:-1]))
    #                     sensor1.append([float(temp[3][1:-1]),float(temp[4][1:-1]),float(temp[5][1:-1])])
    #                 if 'roll2' in line:
    #                     sensor2.append([float(temp[3][1:-1]),float(temp[4][1:-1]),float(temp[5][1:-1])])
    #             for i in range(len(sensor1)):
    #                 AcceleratedSpeed.append(sensor1[i])
    #             l,r = filte(pitch)
    #             AcceleratedSpeed = AcceleratedSpeed[l:l+80]
    #             std.append(AcceleratedSpeed)
    # for index in range(len(std)):
    #     np.savetxt("std_"+str(index)+".txt",std[index])
    # FILE_NUM = 110
    # error = set()
    # grades = [[] for i in range(11)]
    # for index in range(FILE_NUM):
    #     tpitch,tSensor1,tSensor2 = [],[],[]
    #     tAcceleratedSpeed = []
    #     with open(str(index)+".txt","r") as f:
    #         lines = f.readlines()
    #         label = int(lines[-1])
    #         for line in lines:
    #             temp = ret.findall(line)
    #             if 'roll1' in line:
    #                 tpitch.append(float(temp[1][1:-1]))
    #                 tSensor1.append([float(temp[3][1:-1]),float(temp[4][1:-1]),float(temp[5][1:-1])])
    #             if 'roll2' in line:
    #                 tSensor2.append([float(temp[3][1:-1]),float(temp[4][1:-1]),float(temp[5][1:-1])])
    #     for i in range(len(tSensor1)):
    #         tAcceleratedSpeed.append(tSensor1[i])
    #     bl,br = filte(tpitch)
    #     tAcceleratedSpeed = tAcceleratedSpeed[bl:bl+80]
    #     if len(tAcceleratedSpeed)==80:
    #         for AcceleratedSpeed in std:
    #             D = [[0 for i in range(len(tAcceleratedSpeed)+1)] for j in range(len(AcceleratedSpeed)+1)]
    #             for i in range(1,len(AcceleratedSpeed)+1):
    #                 for j in range(1,len(tAcceleratedSpeed)+1):
    #                     D[i][j] = distance(AcceleratedSpeed[i-1][0],AcceleratedSpeed[i-1][1],AcceleratedSpeed[i-1][2],\
    #                                     tAcceleratedSpeed[j-1][0],tAcceleratedSpeed[j-1][1],tAcceleratedSpeed[j-1][2])\
    #                                     +min(D[i][j-1],D[i-1][j],D[i-1][j-1])
    #             grades[label].append(D[len(AcceleratedSpeed)][len(tAcceleratedSpeed)])
    # for i in grades:
    #     print(np.mean(i))
    for index in range(12):
        std.append(np.loadtxt("std_"+str(index)+".txt"))
    threshold = data[0] * 1.1
    Matrix = np.matrix((np.ones((480,1))))
    Label = np.matrix((np.ones((1,1))))
    mat = np.matrix((np.ones((480,1))))
    dtwDistance = []
    tpitch,tSensor1,tSensor2 = [],[],[]
    tAcceleratedSpeed1 = []
    tAcceleratedSpeed2 = []
    logReader.seek(0)
    lines = logReader.readlines()
    for line in lines:
        temp = ret.findall(line)
        if 'roll1' in line:
            tpitch.append(float(temp[1][1:-1]))
            tSensor1.append([float(temp[3][1:-1]),float(temp[4][1:-1]),float(temp[5][1:-1])])
        if 'roll2' in line:
            tSensor2.append([float(temp[3][1:-1]),float(temp[4][1:-1]),float(temp[5][1:-1])])
    for i in range(len(tSensor1)):
        tAcceleratedSpeed1.append(tSensor1[i])
        tAcceleratedSpeed2.append(tSensor2[i])
    bl,br = filte(tpitch)
    tAcceleratedSpeed1 = tAcceleratedSpeed1[bl:bl+80]
    tAcceleratedSpeed2 = tAcceleratedSpeed2[bl:bl+80]
    flag = False
    if len(tAcceleratedSpeed1)==80:
        mark = []
        for AcceleratedSpeed in std:
            D = [[0 for i in range(len(tAcceleratedSpeed1)+1)] for j in range(len(AcceleratedSpeed)+1)]
            for i in range(1,len(AcceleratedSpeed)+1):
                for j in range(1,len(tAcceleratedSpeed1)+1):
                    D[i][j] = distance(AcceleratedSpeed[i-1][0],AcceleratedSpeed[i-1][1],AcceleratedSpeed[i-1][2],\
                                    tAcceleratedSpeed1[j-1][0],tAcceleratedSpeed1[j-1][1],tAcceleratedSpeed1[j-1][2])\
                                    +min(D[i][j-1],D[i-1][j],D[i-1][j-1])
            mark.append(D[len(AcceleratedSpeed)][len(tAcceleratedSpeed1)])
        print(np.mean(mark))
        if np.mean(mark)<= threshold:
            flag = True
            AcceleratedSpeed = AcceleratedSpeed[:80]
            dtwDistance.append(np.mean(mark))
            ax1 = [tAcceleratedSpeed1[i][0] for i in range(len(tAcceleratedSpeed1))]
            ay1 = [tAcceleratedSpeed1[i][1] for i in range(len(tAcceleratedSpeed1))]
            az1 = [tAcceleratedSpeed1[i][2] for i in range(len(tAcceleratedSpeed1))]
            ax2 = [tAcceleratedSpeed2[i][0] for i in range(len(tAcceleratedSpeed2))]
            ay2 = [tAcceleratedSpeed2[i][1] for i in range(len(tAcceleratedSpeed2))]
            az2 = [tAcceleratedSpeed2[i][2] for i in range(len(tAcceleratedSpeed2))]
            mat = np.column_stack((mat,np.matrix(np.array(ax1+ay1+az1+ax2+ay2+az2)).T))

    label = [closest(i,data[4],data[3],data[2],data[1],data[0]) for i in dtwDistance]
    Matrix = np.column_stack((Matrix,mat[:,1:]))
    if flag:
        score = calScore(Matrix[:,1:])
        return "*"+str(score),activity
    else:
        return "*"+str(random.randint(1,5)),activity
def scoreAlg(activity,logReader):
    grades,activity = _scoreAlg(activity,logReader)
    return grades,activity