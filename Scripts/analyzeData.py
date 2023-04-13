
import matplotlib.pyplot as plt
import numpy as np
import csv


filePaths = ["Coarse_NoRefinement_Results.csv", \
             "Coarse_Refinement_Results.csv", \
             "Fine_NoRefinement_Results.csv", \
                "Fine_Refinement_Results.csv"]

numFiles = len(filePaths)
rows = 110
cols = 9

viscid_rows = 25
viscid_cols = 9

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
viscous_data = np.empty([1, viscid_rows, viscid_cols])

def importData():
    for i, fileP in enumerate(filePaths):
        data[i,:,:] = np.loadtxt(fileP, delimiter=",", skiprows=1)
        #print(data[i])

def importViscousData():
    viscous_data[0,:,:] = np.loadtxt("Viscous_Results.csv", delimiter=",", skiprows=1)

def createPlots():
    plt.rcParams.update({'font.size': 14})
    plt.rc('legend', fontsize=12)

    plt.figure(1)
    dragPolar(Mach = 0.3)
    plt.savefig("Photos/DragPolarM0_3.png", dpi=600)
    
    plt.figure(2)
    dragPolar(Mach = 1)
    plt.savefig("Photos/DragPolarM1.png", dpi=600)

    plt.figure(3)
    dragPolar(Mach = 1.6)
    plt.savefig("Photos/DragPolarM1_6.png", dpi=600)

    plt.figure(4)
    liftMach()
    plt.savefig("Photos/LiftAndMach.png", dpi=600)

    plt.figure(5)
    dragMach()
    plt.savefig("Photos/DragAndMach.png", dpi=600)

    plt.figure(6)
    liftCurve(Mach = 0.3)
    plt.savefig("Photos/LiftCurveM0_3.png", dpi=600)
    
    plt.figure(7)
    liftCurve(Mach = 1)
    plt.savefig("Photos/LiftCurveM1.png", dpi=600)

    plt.figure(8)
    liftCurve(Mach = 1.6)
    plt.savefig("Photos/LiftCurveM1_6.png", dpi=600)

    plt.figure(9)
    LDCurveAOA(Mach = 0.3)
    plt.savefig("Photos/LDCurveM0_3.png", dpi=600)

    plt.figure(10)
    LDCurveAOA(Mach = 1)
    plt.savefig("Photos/LDCurveM1.png", dpi=600)

    plt.figure(11)
    LDCurveAOA(Mach = 1.6)
    plt.savefig("Photos/LDCurveM1_6.png", dpi=600)

    plt.figure(12)
    LDCurveMach(0)
    plt.savefig("Photos/LDCurveMach_0deg", dpi=600)

    plt.figure(13)
    LDCurveMach(3)
    plt.savefig("Photos/LDCurveMach_3deg", dpi=600)

    plt.figure(14)
    LDCurveMach(11)
    plt.savefig("Photos/LDCurveMach_11deg", dpi=600)

    plt.figure(15)
    dragPolarAndViscous()
    plt.savefig("Photos/DragPolarAndViscousM0_3.png", dpi=600)

    plt.show()


def dragPolar(Mach = 0.1):
    for i in range(numFiles):
        plt.plot(data[i, data[i, :, d["Mach"]] == Mach, d["CD"]], \
            data[i, data[i, :, d["Mach"]] == Mach, d["CL"]], 
            label=filePaths[i][:-12], marker = '.')
        
    plt.xlabel("CD")
    plt.ylabel("CL")
    plt.xlim(left=0)
    plt.legend()
    plt.grid(alpha = 0.4)
    plt.suptitle("Drag Polar, Mach: %.1f" % Mach )

def dragPolarAndViscous(Mach = 0.3):
    for i in range(numFiles):
        plt.plot(data[i, data[i, :, d["Mach"]] == Mach, d["CD"]], \
            data[i, data[i, :, d["Mach"]] == Mach, d["CL"]], 
            label=filePaths[i][:-12], marker = '.')
    
    print(viscous_data)
    plt.plot(viscous_data[0, 1:, d["CD"]], viscous_data[0, 1:, d["CL"]],
            label="Viscous Case", marker = '.')
        
    plt.xlabel("CD")
    plt.ylabel("CL")
    plt.xlim(left=0)
    plt.legend()
    plt.grid(alpha = 0.4)
    plt.suptitle("Drag Polar With Viscous Case, Mach: %.1f" % Mach )

def liftMach(aoa = 0):
    for i in range(numFiles):
        mask = data[i,:,d["Alpha"]] == aoa
        plt.plot(data[i, mask, d["Mach"]], data[i, mask, d["CL"]], \
            label=filePaths[i][:-12], marker = '.')

    plt.legend()
    plt.xlabel("Mach Number")
    plt.ylabel("CL")
    plt.grid(alpha = 0.4)
    plt.suptitle("Coefficient of lift and Mach Number")

def dragMach(aoa = 0):
    for i in range(numFiles):
        mask = data[i,:,d["Alpha"]] == aoa
        plt.plot(data[i, mask, d["Mach"]], data[i, mask, d["CD"]], \
             label=filePaths[i][:-12], marker = '.')

    plt.legend()
    plt.xlabel("Mach Number")
    plt.ylabel("CD")
    plt.grid(alpha = 0.4)
    plt.suptitle("Coefficient of drag and Mach Number")

def liftCurve(Mach = 0.3):
    for i in range(numFiles):
        mask = data[i, :, d["Mach"]] == Mach
        mask
        plt.plot(data[i, mask, d["Alpha"]], data[i, mask, d["CL"]], \
            label = filePaths[i][:-12], marker = '.')
    
    plt.legend()
    plt.xlabel("Angle of Attack")
    plt.ylabel("CL")
    plt.grid(alpha = 0.4)
    plt.suptitle("Lift Curve, Mach: %.1f" % Mach )

def LDCurveAOA(Mach = 0.3):
    for i in range(numFiles):
        mask = data[i, :, d["Mach"]] == Mach
        plt.plot(data[i, mask, d["Alpha"]], data[i, mask, d["LD"]], \
            label = filePaths[i][:-12], marker = '.')
    
    plt.legend()
    plt.xlabel("Angle of Attack")
    plt.ylabel("L/D")
    plt.grid(alpha = 0.4)
    plt.suptitle("Lift/Drag Curve wrt Alpha, Mach: %.1f" % Mach )

def LDCurveMach(aoa = 3):
    for i in range(numFiles):
        mask = data[i, :, d["Alpha"]] == aoa
        mask
        plt.plot(data[i, mask, d["Mach"]], data[i, mask, d["LD"]], \
            label = filePaths[i][:-12], marker = '.')
    
    plt.legend()
    plt.xlabel("Mach Number")
    plt.ylabel("L/D")
    plt.grid(alpha = 0.4)
    plt.suptitle("Lift/Drag Curve wrt Mach, Angle of Attack: %.1f" % aoa )


if __name__ == "__main__":
    importData()
    importViscousData()
    createPlots()