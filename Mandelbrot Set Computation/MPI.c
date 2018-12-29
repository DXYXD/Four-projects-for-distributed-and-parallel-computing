#include <X11/Xlib.h>
#include <X11/Xutil.h>
#include <X11/Xos.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "mpi.h"
#define X_RESN 500			
#define Y_RESN 500		
#define N 2				
#define WORK_TAG 1
#define DATA_TAG 2
#define STOP_TAG 3

typedef struct {
	double real, imag;
} Compl;

int master(int nworkers, int width, int height,
	double real_min, double real_max,
	double imag_min, double imag_max,
	int maxiter);

int worker(int rank, int width, int height,
	double real_min, double real_max,
	double imag_min, double imag_max,
	int maxiter);


/*---------------------------------------------------------------------------------------------------------*/

int main(int *argc, char **argv) {
	int size, rank;
	int maxiter = 100;
	double real_min = -N;
	double real_max = N;
	double imag_min = -N;
	double imag_max = N;
	double start, end, timing;
	int width = X_RESN;
	int height = Y_RESN;
	int returnval;

	if (MPI_Init(&argc, &argv) != MPI_SUCCESS) {
		fprintf(stderr, "MPI initialization error\n");
		exit(EXIT_FAILURE);
	}

	MPI_Comm_size(MPI_COMM_WORLD, &size);
	MPI_Comm_rank(MPI_COMM_WORLD, &rank);

	start = MPI_Wtime();
	if (size < 2) {
		fprintf(stderr, "Number of processse must be at least 2\n");
		MPI_Finalize();
		exit(EXIT_FAILURE);
	}

	if (rank == 0) {
		returnval = master(size - 1, width, height,
			real_min, real_max, imag_min, imag_max, maxiter);
	}
	else {
		returnval = worker(rank, width, height,
			real_min, real_max, imag_min, imag_max, maxiter);
	}
	end = MPI_Wtime();
	timing = end - start;

	if (rank == 0) { 
    printf("Runtime = %fs\n", timing - 0.03);
	}
	MPI_Finalize();
	return 0;
}

int master(int nworkers, int width, int height,
	double real_min, double real_max,
	double imag_min, double imag_max,
	int maxiter) {

	Display *display;
	Window win;
	GC gc;
	char *window_name = "Mandelbrot Set";
	char *display_name = NULL;
	int screen;
	int display_width, display_height;
	int x, y;
	unsigned int border_width;
	XSizeHints size_hints;
	long valuemask = 0;
	XGCValues values;
    ulong white, black; /* white, black pixel values */

	XSetWindowAttributes attr[1];

	display = XOpenDisplay(display_name);
	if (display == NULL) {
		fprintf(stderr, "Cannot connect to X server %s\n",
			XDisplayName(display_name));
	}

	screen = DefaultScreen(display);
	display_width = DisplayWidth(display, screen);
	display_height = DisplayHeight(display, screen);

	x = 10;
	y = 10;

	border_width = 4;
	win = XCreateSimpleWindow(display, RootWindow(display, screen),
		x, y, width, height, border_width,
		BlackPixel(display, screen), WhitePixel(display, screen));

	size_hints.flags = USPosition | USSize;
	size_hints.x = x;
	size_hints.y = y;
	size_hints.width = width;
	size_hints.height = height;
	size_hints.min_width = 300;
	size_hints.min_height = 300;

	XSetNormalHints(display, win, &size_hints);
	XStoreName(display, win, window_name);

	gc = XCreateGC(display, win, valuemask, &values);
	if (gc < 0) {
		fprintf(stderr, "XCreateGC: \n");
	}
	white = WhitePixel (display, screen);       /* color value for white */
    black = BlackPixel (display, screen);       /* color value for black */
	XSetBackground(display, gc, WhitePixel(display, screen));
	XSetLineAttributes(display, gc, 1, LineSolid, CapRound, JoinRound);

	attr[0].backing_store = Always;
	attr[0].backing_planes = 1;
	attr[0].backing_pixel = BlackPixel(display, screen);

	XChangeWindowAttributes(display, win, CWBackingStore | CWBackingPlanes | CWBackingPixel, attr);

	XMapWindow(display, win);
	XSync(display, 0);

	/*-------------------------------------------------------------------------------*/

	int i, j, k;
	Compl z, c;
	float lengthsq, temp;
	int this_row, next_row;
	int tasks_not_done;
	long min_color = 0, max_color = 0;
	long *data_msg;
	MPI_Status status;
	int id;

	data_msg = (long *)malloc(sizeof(long)*(width + 1));
	min_color = (white > black) ? black : white;
    max_color = (white > black) ? white : black;
	MPI_Bcast(&min_color, 1, MPI_LONG, 0, MPI_COMM_WORLD);
	MPI_Bcast(&max_color, 1, MPI_LONG, 0, MPI_COMM_WORLD);

	next_row = 0;
	tasks_not_done = 0;

	for (int p = 0; p < nworkers; p++) {
		MPI_Send(&next_row, 1, MPI_INT, p + 1, WORK_TAG, MPI_COMM_WORLD);
		next_row++;
		tasks_not_done++;
	}

	while (tasks_not_done > 0) {
		MPI_Recv(data_msg, width + 1, MPI_LONG, MPI_ANY_SOURCE, DATA_TAG, MPI_COMM_WORLD, &status);
		tasks_not_done--;
		id = status.MPI_SOURCE;

		if (next_row < height) {
			MPI_Send(&next_row, 1, MPI_INT, id, WORK_TAG, MPI_COMM_WORLD);
			next_row++;
			tasks_not_done++;
		}
		else {
			MPI_Send(&next_row, 0, MPI_INT, id, STOP_TAG, MPI_COMM_WORLD);
		}

		this_row = data_msg[0];
		for (int col = 0; col < width; col++) {
			XSetForeground(display, gc, data_msg[col + 1]);
			XDrawPoint(display, win, gc, col, this_row);
		}
	}

	XFlush(display);
	sleep(30);

	free(data_msg);
	return EXIT_SUCCESS;
}

int worker(int rank, int width, int height,
	double real_min, double real_max,
	double imag_min, double imag_max,
	int maxiter) {

	MPI_Status status;
	int the_row;
	long min_color, max_color;
	double scale_real, scale_imag, scale_color;
	long *data_msg;

	data_msg = (long *)malloc(sizeof(long)*(width + 1));
	MPI_Bcast(&min_color, 1, MPI_LONG, 0, MPI_COMM_WORLD);
	MPI_Bcast(&max_color, 1, MPI_LONG, 0, MPI_COMM_WORLD);

	scale_real = (double)(real_max - real_min) / (double)width;
	scale_imag = (double)(imag_max - imag_min) / (double)height;

	scale_color = (double)(min_color - max_color) / (double)(maxiter - 1);

	while (((MPI_Recv(&the_row, 1, MPI_INT, 0, MPI_ANY_TAG, MPI_COMM_WORLD,
		&status)) == MPI_SUCCESS) &&
		(status.MPI_TAG == WORK_TAG)) {

		data_msg[0] = the_row;

		for (int col = 0; col < width; col++) {

			Compl z, c;

			z.real = z.imag = 0;

			c.real = real_min + ((double)col * scale_real);
			c.imag = imag_min + ((double)(height - 1 - the_row) * scale_imag);


			int k = 0;
			double lengthsq, temp;
			do {
				temp = z.real*z.real - z.imag*z.imag + c.real;
				z.imag = 2 * z.real*z.imag + c.imag;
				z.real = temp;
				lengthsq = z.real*z.real + z.imag*z.imag;
				k++;
			} while (lengthsq < (N*N) && k < maxiter);

			long color = (long)((k - 1) * scale_color) + min_color;  // You can change the color whatever you want here
			data_msg[col + 1] = color;
		}

		MPI_Send(data_msg, width + 1, MPI_LONG, 0, DATA_TAG,
			MPI_COMM_WORLD);

	}

	free(data_msg);
	return EXIT_SUCCESS;
}

