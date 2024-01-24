#######################################################################################
## Run Parametric Studies in PyCharm
#######################################################################################
import numpy as np
import subprocess
from os import path
from numpy import floor
import os
curr_dir = os.getcwd()

if not os.path.exists(curr_dir + '//FEModelFiles'):
    os.mkdir(curr_dir + '//FEModelFiles')

n_hoop = np.array([12])
n_vertical = np.array([7])
g = np.array([3.0,5.8,7.45])

mu = np.array([0.125])
R = np.array([15.5])
alpha = np.array([10.0])
vvv = np.array([50.0])

jobName ='exTube'

U = np.zeros(len(g))
for i in range(len(g)):
    DirName = jobName + '_g_' + '%g'%g[i] 
    if path.exists(curr_dir + '//FEModelFiles//' + DirName) == True:
        print(curr_dir + '//FEModelFiles//' + DirName + "already exists!")
        data = np.genfromtxt(curr_dir + '//FEModelFiles//' + DirName + "//exTube.csv", dtype = float, delimiter=',', skip_header=1)
        g[i] = data[0]
        U[i] = data[1]
    elif path.exists(curr_dir + '//FEModelFiles//' + DirName) == False:
        f = open("Parameters_for_exTube.py", "w")
        f.write("n_hoop = " + "%g"%n_hoop[0] + '\n')
        f.write("n_vertical = " + "%g"%n_vertical[0] + '\n')
        f.write("g = " + "%g"%g[i] + '\n')
        f.write("mu = " + "%g"%mu[0] + '\n')
        f.write("R = " + "%g"%R[0] + '\n')
        f.write("alpha = " + "%g"%alpha[0] + '\n')
        f.write("vvv = " + "%g"%vvv[0] + '\n')
        f.close()
        print(curr_dir + '//FEModelFiles//' + DirName + 'is running!!')
        try:
            subprocess.call(['sh', 'run3828.sh'])
            data = np.genfromtxt(curr_dir + '//FEModelFiles//' + DirName + "//exTube.csv", dtype = float, delimiter=',', skip_header=1)
            g[i] = data[0]
            U[i] = data[1]
        except:
            print("unexpected error!!!!!")   
print(g)
print(U)
