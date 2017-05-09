import os
import re
import math
import matplotlib.pyplot as plt

def generateImage(logReader, imageName):
    def graph(ax, ay, az, bx, by, bz):
        plt.figure(1)
        #switch to x subgraph
        dst = []
        for i in range(min(len(ax),len(bx))):
            dst.append(math.sqrt((ax[i] - bx[i])**2 + (ay[i] - by[i])**2 + (az[i]-bz[i])**2))
        plt.plot(dst)
        #plt.plot(bx)
        plt.title("three dimension acceleration comparation")
        #switch to y subgraph
        #plt.sca(y)
        #plt.plot(ay)
        #plt.plot(by)
        #plt.title("y axis acceleration comparation")
        #switch to z subgraph
        #plt.sca(z)
        #plt.plot(az)
        #plt.plot(bz)
        #plt.title("z axis acceleration comparation")
        plt.savefig(imageName)

    def getData(file, aAx, aAy, aAz):
        lines = file.readlines()
        count = 0
        for line in lines:
            temp = re.findall(r":.*?\]",line)
            if (count % 2 == 0) & (len(temp) > 5):
                aAx.append(float(temp[3][1:-1]))
                aAy.append(float(temp[4][1:-1]))
                aAz.append(float(temp[5][1:-1]))
            #if (count % 2 == 1):
            #    bAx.append(float(temp[3][1:-1]))
             #   bAy.append(float(temp[4][1:-1]))
             #   bAz.append(float(temp[5][1:-1]))
            count = count + 1

    ax = []
    ay = []
    az = []
    bx = []
    by = []
    bz = []
    logReader.seek(0)
    getData(logReader, ax, ay, az)
    file = open("G:\\C_Code\\SensorPlus_RC1\\straightPunch\\17.txt","r")
    getData(file , bx, by, bz)
    graph(ax, ay, az, bx, by, bz)
    # no need to return anything. just generate the image
