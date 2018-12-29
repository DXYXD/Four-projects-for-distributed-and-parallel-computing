# Four-projects-for-distributed-and-parallel-computing
They are four project practice focusing on MPI and Pthread for distributed and parallel computing. The first project use C++, the second one use C and the last two use Python.
## Project 1
- Environment
1. Platform: Windows 10 x64
2. Language: C++
3. Compiler: Mirosoft Visual C++
4. MPI: MS-MPI v9.0.1

- Description
1. For each process with odd rank P, send its number to the process with rank P-1.
2. For each process with rank P-1, compare its number with the number sent by the process with rank P and send the larger one back to the process with rank P.
3. For each process with even rank Q, send its number to the process with rank Q-1.
4. For each process with rank Q-1, compare its number with the number sent by the process with rank Q and send the larger one back to the process with rank Q.

Repeat 1-4 until the numbers are sorted.

## Project 2
- Environment 
1. Platform: x86 64 GNU/Linux 
2. language: C 
3. Parallel Computing Interface: openMPI, POSIX 
4. Library: X11/Xlib(GUI), pthread.h(thread), mpi.h(process)

- Description

The term Mandelbrot set is used to refer both to a general class of fractal sets and to a particular instance of such a set. In general, a Mandelbrot set marks the set of points in the complex plane such that the corresponding connected and not computable.\par
The mandelbrot set is the set obtained from the quadratic recurrence equation 
<a href="https://www.codecogs.com/eqnedit.php?latex=$$z_{n&plus;1}&space;=&space;z_n^2&plus;C$$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?$$z_{n&plus;1}&space;=&space;z_n^2&plus;C$$" title="$$z_{n+1} = z_n^2+C$$" /></a>
with 
<a href="https://www.codecogs.com/eqnedit.php?latex=$z_0=C$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?$z_0=C$" title="$z_0=C$" /></a>
, where points C in the complex plane for which the orbit of 
<a href="https://www.codecogs.com/eqnedit.php?latex=$z_n$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?$z_n$" title="$z_n$" /></a>
does not tend to infinity are in the set. Setting 
<a href="https://www.codecogs.com/eqnedit.php?latex=$z_0$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?$z_0$" title="$z_0$" /></a> 
equal to any in the set that is not a periodic point give the same result. The Mandelbrot set is connected. A plot of the Mandelbrot set is shown below in which values of C in the complex plane are colored according to the number of steps required to reach 
<a href="https://www.codecogs.com/eqnedit.php?latex=$r_max=2$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?$r_max=2$" title="$r_max=2$" /></a>
. The kidney bean-shaped portion of the Mandelbrot set turn out to be bordered by a cardioid with equations. 
<a href="https://www.codecogs.com/eqnedit.php?latex=$$4x=2\cos&space;t-\cos(2t)$$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?$$4x=2\cos&space;t-\cos(2t)$$" title="$$4x=2\cos t-\cos(2t)$$" /></a>
<a href="https://www.codecogs.com/eqnedit.php?latex=$$4y=2\sin&space;t-\sin(2t)$$" target="_blank"><img src="https://latex.codecogs.com/gif.latex?$$4y=2\sin&space;t-\sin(2t)$$" title="$$4y=2\sin t-\sin(2t)$$" /></a>
This specific Mandelbrot set was implemented in this homework by using parallel methods MPI and Pthread.

## Project 3
- Environment
1. Platform: x86\_64 CPU/Windows
2. Multi-core processor: 4
3. CPU rate: 2.40GHZ
4. language: Python
5. Library: mpl\_toolkits/matplotlib(GUI), mpi4py(Process), threading(multi-threads)

- Description

Dynamics is interested in more than a pure description of motion. Dynamics is a study of how a system of bodies evolves over time under the presence of force. Bodies are represented by mass particles (or mass points) that are under the influence of force. The N-body simulation is used to determine the evolution of N-body system.

The N-body problem is defined as follows. We have initial conditions i.e. initial positions and initial velocities of all bodies in the system. Interactions (forces) between all bodies in the system have to be evaluated to receive new positions and new velocities. This evaluation is performed repeatedly so that we are getting information about the time evolution of the system. 


## Project 4
- Environment
1. Platform: x86\_64 CPU/Windows
2. Multi-core processor: 4
3. CPU rate: 2.40GHZ
4. language: Python
5. Library: mpl\_toolkits/matplotlib(GUI), mpi4py(Process), threading(multi-threads)

- Description
The temperature of the wall is 20<img src="https://latex.codecogs.com/gif.latex?$^\circ$C" title="$^\circ$C" />, and the temperature of the fireplace is 100<img src="https://latex.codecogs.com/gif.latex?$^\circ$C" title="$^\circ$C" />. In this program, I use Jacobi iteration to compute the temperature inside the room and plot(in color) the temperature contour at 5<img src="https://latex.codecogs.com/gif.latex?$^\circ$C" title="$^\circ$C" /> intervals using matplotlib. 
