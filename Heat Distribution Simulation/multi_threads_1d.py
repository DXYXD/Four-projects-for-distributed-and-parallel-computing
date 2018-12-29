import threading
import numpy as np 
import Const
import time
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm

# Define Constants
Const.THREAD = 4
Const.ROWS = 12
Const.COLS = 12
Const.STEPS = 100
Const.PART = Const.COLS // Const.THREAD
Const.REMAINDER = Const.COLS % Const.THREAD
Const.TEMPW = 20
Const.TEMPF = 100
Const.FPL = int(Const.ROWS * 0.4)
xl = 1
yl = 1

# Define global arrays/mesh
c = np.zeros([Const.ROWS, Const.COLS], dtype = 'f')

# Create thread class
class myThread (threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID
    def run(self):
        jacobiCompute(self.threadID)

# Define jacobi computing function
def jacobiCompute(threadID):
    # Define heat Mesh/Array for Computing
    if threadID != Const.THREAD - 1:
        mysize = Const.PART + 2
        tA = np.zeros([Const.ROWS, mysize], dtype = 'f')
        cB = np.zeros([Const.ROWS, mysize], dtype = 'f')
    else:
        mysize = Const.PART + Const.REMAINDER + 2
        tA = np.zeros([Const.ROWS, mysize], dtype = 'f')
        cB = np.zeros([Const.ROWS, mysize], dtype = 'f')

    # Assign Data to local arrays
    if threadID == 0:
        begincol = 0
        endcol = mysize - 1
    elif threadID == Const.THREAD - 1:
        begincol = threadID * Const.PART - 1
        endcol = begincol + mysize - 1
    else:
        begincol = threadID * Const.PART - 1
        endcol = begincol + mysize

    for i in range(Const.ROWS):
        for j in range(begincol, endcol):
            if threadID == 0:
                tA[i][1 + j] = c[i][j]
            else:
                tA[i][j - begincol] = c[i][j]

    # Jacobi iteration
    if threadID == 0:
        startcol = 2
        lastcol = mysize - 1
    elif threadID == Const.THREAD - 1:
        startcol = 1
        lastcol = mysize - 2
    else:
        startcol = 1
        lastcol = mysize - 1

    for i in range(1, Const.ROWS - 1):
        for j in range(startcol, lastcol):
            cB[i][j] = 0.25 * (tA[i-1][j] + tA[i + 1][j] + tA[i][j - 1] + tA[i][j + 1])
        # Finish computing
    
    # Reassign data to global array
    for i in range(1, Const.ROWS - 1):
        for j in range(startcol, lastcol):
            if threadID == 0:
                c[i][j - 1] = cB[i][j]
            else:
                c[i][begincol + j] = cB[i][j]

# Finish iteration

def main():
    # Initialize global arrays: set temperature
    for i in range(Const.ROWS):
        b = (Const.ROWS - Const.FPL) // 2 
        if i in range(b, b + Const.FPL):
            c[i][0] = Const.TEMPF
        else:
            c[i][0] = Const.TEMPW
        c[i][Const.COLS - 1] = Const.TEMPW

    for i in range(Const.COLS):
        c[0][i] = Const.TEMPW
        c[Const.COLS - 1][i] = Const.TEMPW

    plt.ion()
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_zlim(-25, 100)
    ax.set_xlim(0,xl)
    ax.set_ylim(0,yl)

    for count in range(Const.STEPS):
        threads = []
        for thread in range(Const.THREAD):
            t = myThread(thread)
            threads.append(t)
        
        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

       # Two arrays with the mid points of each partition
        x = np.linspace(0, xl, Const.ROWS)
        y = np.linspace(0, yl, Const.COLS)
        # Declare a second array, that is the 2D representation of the
        # ones above.
        X,Y = np.meshgrid(x,y)
        Z = c
        ax.plot_surface(X,Y,Z, cmap=plt.get_cmap('rainbow'),linewidth=0, antialiased = False)      
        cf = ax.contourf(X,Y,Z, level = 16, zdir='z',offset=-25, alpha = 0.6)
        plt.show()
        plt.pause(0.01)

if __name__ == '__main__':
    main()
