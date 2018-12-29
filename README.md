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

