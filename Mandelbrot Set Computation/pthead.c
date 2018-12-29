#include <X11/Xlib.h>
#include <X11/Xutil.h>
#include <X11/Xos.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <pthread.h>
#include <time.h>
#define  X_RESN  500       
#define  Y_RESN  500       
#define  N 2
#define  NUM_THREADS 5
#define  MAXITER  100

long *task_num[NUM_THREADS];
typedef struct {
	double real, imag;
} Compl;

void *worker(void *thread_id);
void print();

int main(int argc, char *argv[]) {	
	pthread_t threads[NUM_THREADS];
	int rc, thread_id, i;
	int width = X_RESN, height = Y_RESN;

	clock_t start_time = clock();
	for (thread_id = 0; thread_id < NUM_THREADS; thread_id++) {
		rc = pthread_create(&threads[thread_id], NULL, worker, (void *)(intptr_t)thread_id);
		if (rc) {
			printf("ERROR; return code from pthread_create() is %d\n", rc);
			exit(-1);
		}
	}

	for (thread_id = 0; thread_id < NUM_THREADS; thread_id++) {
		rc = pthread_join(threads[thread_id], NULL);
		if (rc) {
			printf("ERROR; return code from pthread_join() is %d\n", rc); 
			exit(-1);
		}
	}

	print();

	clock_t end_time = clock();
	printf("The run time is: %fs", (double)(end_time - start_time - 0.03)/CLOCKS_PER_SEC);
	for (i = 0; i < NUM_THREADS; i++)
		free(task_num[i]);

	pthread_exit(NULL);
}

void *worker(void *thread_id) {
	int task_id;
	int width = X_RESN, height = Y_RESN;
	int rows = height / NUM_THREADS;
	int reminder = height % NUM_THREADS;
	int cal_rows;
	int r, col, the_row;
	double real_min = -N, 
		   real_max = N, 
		   imag_min = -N, 
		   imag_max = N;
	double scale_real, scale_imag;

  task_id = (intptr_t) thread_id;
	if (task_id == NUM_THREADS - 1) {
		cal_rows = rows + reminder;
		task_num[task_id] = (long *)malloc(sizeof(long)*(cal_rows * width));
	}
	else {
		cal_rows = rows;
		task_num[task_id] = (long *)malloc(sizeof(long)*(rows * width));
	}

	scale_real = (double)(real_max - real_min) / (double)width;
	scale_imag = (double)(imag_max - imag_min) / (double)height;

	for (r = 0; r < cal_rows; r++) {
		the_row = task_id * rows + r - 1;
		for (col = 0; col < width; col++) {
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
			} while (lengthsq < (N*N) && k < MAXITER);

			long color = (long)(k - 1);
			task_num[task_id][r * width + col] = color;
		}	
	}
}


void print() {
	Display *display;
	Window win;
	GC gc;
	char *window_name = "Mandelbrot Set";
	char *display_name = NULL;
	int screen;
	int display_width, display_height;
	int x, y;
	int width = X_RESN, height = Y_RESN;
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

	x = 0;
	y = 0;

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
	white = WhitePixel(display, screen);       
	black = BlackPixel(display, screen);      
	XSetBackground(display, gc, WhitePixel(display, screen));
	XSetLineAttributes(display, gc, 1, LineSolid, CapRound, JoinRound);

	attr[0].backing_store = Always;
	attr[0].backing_planes = 1;
	attr[0].backing_pixel = BlackPixel(display, screen);

	XChangeWindowAttributes(display, win, CWBackingStore | CWBackingPlanes | CWBackingPixel, attr);

	XMapWindow(display, win);
	XSync(display, 0);

	/*---------------------------------------------------------------------------------------------*/
	
	int this_row, r, c;
	int rows = height / NUM_THREADS;
	long id;
	long min_color = 0, max_color = 0;
	double scale_color;

	min_color = (white > black) ? black : white;
	max_color = (white > black) ? white : black;

	scale_color = (double)(min_color - max_color) / (double)(MAXITER - 1);

	for (r = 0; r < height; r++) {
		id = r / rows;
		for (c = 0; c < width; c++) {
			long color = (long)(task_num[id][(r % rows)*width + c - 1] * scale_color) + min_color;
			XSetForeground(display, gc, color);
			XDrawPoint(display, win, gc, c, r);
		}
	}
	XFlush(display);
	sleep(30);
}

