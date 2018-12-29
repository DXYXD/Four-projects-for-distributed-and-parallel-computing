# Four-projects-for-distributed-and-parallel-computing
They are four project practice focusing on MPI and Pthread for distributed and parallel computing. The first project use C++, the second one use C and the last two use Python.
## Project 1
- Environment
1. Platform: Windows 10 x64
2. Language: C++
3. Compiler: Mirosoft Visual C++
4. MPI: MS-MPI v9.0.1

- Description
1. **Even sort, the first size – 1 processes have even numbers, rank is not equal to 0.** The processes except for rank 0 process send head number to the previous process and compare tail number of the previous prcess. Numbers in other places within one process do even sort sequentially. The program in all processes are parallel.
2. **Even sort, the first size – 1 processes have even numbers, rank is not equal to size – 1**.The processes except for rank size - 1 processes send back a larger number to the next process Numbers in other places within one process do even sort sequentially. The program in all processes are parallel.
3. **Even sort, the first size – 1 processes have odd numbers, rank is even and not equal to 0**. The even rank processes except for rank 0 send head number to the previous process and compare tail number of the previous prcess. Numbers in other places within one process do even sort sequentially. The program in all processes is parallel.
4. **Even sort, the first size – 1 processes have odd numbers, rank is odd and not equal to size -1**. The odd rank processes except for rank size - 1 send back a larger number to the next process Numbers in other places within one process do even sort sequentially. The program in all processes are parallel.
5. **Odd sort, the first size – 1 processes have odd numbers, rank is odd**. The odd rank processes send head number to the previous processes and compare with tail number of the previous prcess. Numbers in other places within one process do odd sort sequentially. The program in all processes are parallel.
6. ****
