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
The mandelbrot set is the set obtained from the quadratic recurrence equation $$z_{n+1} = z_n^2+C$$ with $z_0=C$, where points $C$ in the complex plane for which the orbit of $z_n$ does not tend to infinity are in the set. Setting $z_0$ equal to any in the set that is not a periodic point give the same result. The Mandelbrot set is connected. A plot of the Mandelbrot set is shown below in which values of $C$ in the complex plane are colored according to the number of steps required to reach $r_max=2$. The kidney bean-shaped portion of the Mandelbrot set turn out to be bordered by a cardioid with equations. $$4x=2\cos t-\cos(2t)$$ $$4y=2\sin t-\sin(2t)$$ This specific Mandelbrot set was implemented in this homework by using parallel methods MPI and Pthread.

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

Mathematically is the N-body problem formulated by the system of ordinary differential equations (ODE) coming from Newton’s laws of motion expressed as
$$\frac{d \vec{r_i} }{dt} = \vec{v_i} \eqno(1.1)$$
$$m_i \cdot \frac{d \vec{v_i}}{dt}=\vec{F_i} \eqno(1.2)$$
where $m_i, \vec{r_i}$ and $\vec{v_i}$ are the mass, position and velocity of the $i-th$ partical, respectively, and $i=1,2,3,...,N$. The force $\vec{F_i}$ is usually the sum of external forces. When dealing with systems of stars or stellar systems, we will use Newton's gravitational force.

## Project 4
- Environment
1. Platform: x86\_64 CPU/Windows
2. Multi-core processor: 4
3. CPU rate: 2.40GHZ
4. language: Python
5. Library: mpl\_toolkits/matplotlib(GUI), mpi4py(Process), threading(multi-threads)

- Description
The temperature of the wall is 20$^\circ$C, and the temperature of the fireplace is 100$^\circ$C. In this program, I use Jacobi iteration to compute the temperature inside the room and plot(in color) the temperature contour at 5$^\circ$C intervals using matplotlib. 
