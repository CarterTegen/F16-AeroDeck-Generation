
import matplotlib.pyplot as plt
import numpy as np
import csv


filePaths = ["../800k Coarse Results/CoarseMesh_800k.csv", \
             "../960k Coarse Results/CoarseMeshRefinedLE_960k.csv"]

numFiles = len(filePaths)
rows = 110
cols = 9

d = {"Mach": 0,\
     "Beta": 1,\
     "Alpha": 2,\
     "Lift": 3,\
     "Drag": 4,\
     "Moment": 5,\
     "LD": 6,\
     "CL": 7,\
     "CD": 8}

data = np.empty([numFiles, rows, cols])

def importData():
    for i, fileP in enumerate(filePaths):
        data[i,:,:] = np.loadtxt(fileP, delimiter=",", skiprows=1)
        #print(data[i])

def createPlots():
    plt.figure(1)
    dragPolar()

    plt.figure(2)
    liftMach()

    plt.show()


def dragPolar(Mach = 0.1):
    for i in range(numFiles):
        plt.plot(data[i, data[i, :, d["Mach"]] == Mach, d["CD"]], data[i, data[i, :, d["Mach"]] == Mach, d["CL"]], label=filePaths[i][filePaths[i].index("/",5)+1:-4])
        
    plt.xlabel("CD")
    plt.ylabel("CL")
    plt.legend()


def liftMach(aoa = 0):
    for i in range(numFiles):
        mask = data[i,:,d["Alpha"]] == aoa
        plt.plot(data[i, mask, d["Mach"]], data[i, mask, d["CL"]], label=filePaths[i][filePaths[i].index("/",5)+1:-4])
    


if __name__ == "__main__":
    importData()
    createPlots()