'''

mpiexec -n 4 python mpiCHD1D_display.py

'''

from mpi4py import MPI
import numpy as np 
import Const
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from time import sleep

# MPI Initialization
sleep(5)
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# plt.ion() allows continuous plotting
if rank == 0:
    plt.ion()
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_zlim(-25, 100)
    ax.set_xlim(0,10)
    ax.set_ylim(0,10)


# Define Constants
Const.ROWS = 20
Const.COLS = 20
Const.STEPS = 100
Const.PART = Const.COLS // size 
Const.REMAINDER = Const.COLS % size
Const.TEMPW = 20
Const.TEMPF = 100
Const.FPL = int(Const.ROWS * 0.2)

# Initialize heat Mesh/Array for Computing
if rank != size - 1:
    mysize = Const.PART + 2
    tA = np.zeros([Const.ROWS, mysize], dtype = 'f')
    cB = np.zeros([Const.ROWS, mysize], dtype = 'f')
else:
    mysize = Const.PART + Const.REMAINDER + 2
    tA = np.zeros([Const.ROWS, mysize], dtype = 'f')
    cB = np.zeros([Const.ROWS, mysize], dtype = 'f')

c = np.zeros([Const.ROWS, Const.COLS], dtype = 'f')
buf = np.zeros(Const.ROWS, dtype = 'f')
buf2 = np.zeros([mysize - 2, Const.ROWS], dtype = 'f')

# Temperature Simulation
# Wall
if rank == 0:
    for i in range(Const.ROWS):
        tA[i][1] = Const.TEMPW
if rank == size - 1:
    for i in range(Const.COLS):
        tA[i][mysize - 2] = Const.TEMPW

for i in range(1, mysize - 1):
    tA[0][i] = Const.TEMPW
    tA[Const.ROWS - 1][i] = Const.TEMPW

# Fire
if size % 2 == 0:
    if rank == (size // 2) - 1:
        b = (Const.ROWS - Const.FPL) // 2 
        for i in range(b, b + Const.FPL):
            tA[i][mysize - 2] = Const.TEMPF
    if rank == size // 2:
        b = (Const.ROWS - Const.FPL) // 2 
        for i in range(b, b + Const.FPL):
            tA[i][1] = Const.TEMPF        

# Jacobi iteration
for count in range(Const.STEPS):
    # send data to the next processor
    if rank < size - 1:
        for i in range(Const.ROWS):
            buf[i] = tA[i][mysize - 2]
        comm.Send(buf, dest = rank + 1, tag = 1)
    
    # receive data from the previous processor
    if rank > 0:
        comm.Recv(buf, source = rank - 1, tag = 1)
        for i in range(Const.ROWS):
            tA[i][0] = buf[i]

    # send data to the previous processor
    if rank > 0:
        for i in range(Const.ROWS):
            buf[i] = tA[i][1]
        comm.Send(buf, dest = rank - 1, tag = 2)

    # reveive data from the next processor
    if rank < size - 1:
        comm.Recv(buf, source = rank + 1, tag = 2)
        for i in range(Const.ROWS):
            tA[i][mysize - 1] = buf[i]

    # Jacobi computing
    begincol = 1
    endcol = mysize - 2
    if rank == 0:
        begincol = 2
    if rank == size - 1:
        endcol = mysize - 3

    for j in range(begincol, endcol + 1):
        for i in range(1, Const.ROWS - 1):
            cB[i][j] = 0.25 * (tA[i-1][j] + tA[i+1][j] + tA[i][j-1] + tA[i][j+1])
    
    for j in range(begincol, endcol + 1):
        for i in range(1, Const.ROWS - 1):
            if tA[i][j] != Const.TEMPF:
                tA[i][j] = cB[i][j]

    # Finish computing
    comm.Barrier()
    ct = []
    disp = []
    for i in range(size):
        if i != size - 1:
            ct.append(Const.PART * Const.ROWS)
        else:
            ct.append((Const.REMAINDER + Const.PART) * Const.ROWS)
        disp.append(i * Const.PART * Const.ROWS)

    start = 1
    end = mysize - 2
    for i in range(Const.ROWS):
        for j in range(start, end + 1):
            buf2[j-1][i] = tA[i][j]

    comm.Gatherv(sendbuf = buf2, recvbuf = [c, ct, disp, MPI.FLOAT], root = 0)
# Finish iteration

    # Display
    if rank == 0:
        # Two arrays with the mid points of each partition
        x = np.linspace(0, 10, Const.ROWS)
        y = np.linspace(0, 10, Const.COLS)
        # Declare a second array, that is the 2D representation of the
        # ones above.
        X,Y = np.meshgrid(x,y)
        Z = np.transpose(c)
        ax.plot_surface(X,Y,Z, cmap=plt.get_cmap('rainbow'),linewidth=0, antialiased = False)      
        cf = ax.contourf(X,Y,Z, 16, zdir='z',offset=-25, alpha = 0.6)
        plt.show()       
        plt.pause(0.01)
