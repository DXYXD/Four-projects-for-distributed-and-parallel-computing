#include "mpi.h"
#include <stdio.h>
#include <stdlib.h>
#include <iostream>
using namespace std;

void oddSort(int *A, int n);
void evenSort(int *A, int n);

int main(int argc, char **argv) {
	int const N = 100000;		    		
	int sequence[N];					
	int rank, size;						
	int reminder;						
	int revNum;							
	double Start, End;					
	int *sendCounts = NULL;				
	int *displs = NULL;					
	int *revSeq = NULL;				    


	MPI_Init(&argc, &argv);
	MPI_Comm_size(MPI_COMM_WORLD, &size);
	MPI_Comm_rank(MPI_COMM_WORLD, &rank);


	if (rank == 0) {
		cout << "\nNAME: Ding Xinyi" << endl;
		cout << "ID: 116010035" << endl;
		cout << "\nStart! The sequence: " << endl;
	}

	Start = MPI_Wtime();			    


	sendCounts = new int[size];         
	reminder = N % size;			    


	for (int i = 0; i < size; i++) {
		sendCounts[i] = int(N / size);
	}

	sendCounts[size - 1] = sendCounts[size - 1] + reminder;    

	displs = new int[size];										
	for (int i = 0; i < size; i++) {
		displs[i] = 0;
		for (int j = 0; j < i; j++) {
			displs[i] = displs[i] + sendCounts[j];
		}
	}
	revSeq = new int[sendCounts[rank]];                        


	MPI_Scatterv(sequence, sendCounts, displs, MPI_INT, revSeq, sendCounts[rank], MPI_INT, 0, MPI_COMM_WORLD);

	for (int i = 0; i < N; i++) {

		if (i % 2 == 0) {
			evenSort(revSeq, sendCounts[rank] - 1);
			if (sendCounts[0] % 2 == 0) {
				if (rank != 0) {
					MPI_Send(&revSeq[0], 1, MPI_INT, rank - 1, 0, MPI_COMM_WORLD);
					MPI_Recv(&revSeq[0], 1, MPI_INT, rank - 1, 1, MPI_COMM_WORLD, MPI_STATUSES_IGNORE);  // put recv after send
				}
				if (rank != size - 1) {
					MPI_Recv(&revNum, 1, MPI_INT, rank + 1, 0, MPI_COMM_WORLD, MPI_STATUSES_IGNORE);
					if (revSeq[sendCounts[rank] - 1] > revNum) {
						int a = revNum;
						revNum = revSeq[sendCounts[rank] - 1];
						revSeq[sendCounts[rank] - 1] = a;
					}
					MPI_Send(&revNum, 1, MPI_INT, rank + 1, 1, MPI_COMM_WORLD);
				}
			}
			else {
				if ((rank % 2 == 0) and (rank != 0)) {
					MPI_Send(&revSeq[0], 1, MPI_INT, rank - 1, 0, MPI_COMM_WORLD);
					MPI_Recv(&revSeq[0], 1, MPI_INT, rank - 1, 1, MPI_COMM_WORLD, MPI_STATUSES_IGNORE);
				}
				if ((rank % 2 == 1) and (rank != size - 1)) {
					MPI_Recv(&revNum, 1, MPI_INT, rank + 1, 0, MPI_COMM_WORLD, MPI_STATUSES_IGNORE);
					if (revSeq[sendCounts[rank] - 1] > revNum) {
						int a = revNum;
						revNum = revSeq[sendCounts[rank] - 1];
						revSeq[sendCounts[rank] - 1] = a;
					}
					MPI_Send(&revNum, 1, MPI_INT, rank + 1, 1, MPI_COMM_WORLD);
				}
			}
		}
		else {
			oddSort(revSeq, sendCounts[rank] - 1);
			if (sendCounts[0] % 2 == 1) {
				if (rank % 2 == 1) {
					MPI_Send(&revSeq[0], 1, MPI_INT, rank - 1, 0, MPI_COMM_WORLD);
					MPI_Recv(&revSeq[0], 1, MPI_INT, rank - 1, 1, MPI_COMM_WORLD, MPI_STATUSES_IGNORE);
				}
				if ((rank % 2 == 0) and (rank != size - 1)) {
					MPI_Recv(&revNum, 1, MPI_INT, rank + 1, 0, MPI_COMM_WORLD, MPI_STATUSES_IGNORE);
					if (revSeq[sendCounts[rank] - 1] > revNum) {
						int a = revNum;
						revNum = revSeq[sendCounts[rank] - 1];
						revSeq[sendCounts[rank] - 1] = a;
					}
					MPI_Send(&revNum, 1, MPI_INT, rank + 1, 1, MPI_COMM_WORLD);
				}
			}
		}
	}

	MPI_Gatherv(revSeq, sendCounts[rank], MPI_INT, sequence, sendCounts, displs, MPI_INT, 0, MPI_COMM_WORLD);

	End = MPI_Wtime();					

	if (rank == 0) {
		printf("\n\nDone! The sorted sequence: \n");
	}

	MPI_Barrier(MPI_COMM_WORLD);
	double time = End - Start;
	if (rank == 0) {
		printf("\n\nThe whole process comsumes time: %f ms\n", time * 1000);
	}

	delete[] sendCounts;
	delete[] displs;
	delete[] revSeq;

	MPI_Finalize();
	return 0;
}
		
void oddSort(int *A, int n) {
	for (int i = 1; i <= n; i += 2) {
		if (A[i] < A[i - 1]) {
			int a = A[i];
			A[i] = A[i - 1];
			A[i - 1] = a;
		}
	}
}

void evenSort(int *A, int n) {
	for (int i = 2; i <= n; i += 2) {
		if (A[i] < A[i - 1]) {
			int a = A[i];
			A[i] = A[i - 1];
			A[i - 1] = a;
		}
	}
}
