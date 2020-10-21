/* PTimer - a simple microsecond timer based on the getrusage() system 
 *          call, which should be in POSIX.
 *
 * Usage:
 *         void *one, *two;
 *         double measured_time;
 *
 *         one = PTimer();
 *
 *         ... work to be timed ...
 *
 *         two = PTimer();
 *         measured_time = PTimerSubtract(two,one);
 *
 *  Note that the second time (the one taken later in real time) is the 
 *  first argument to PTimerSubtract();
 *
 */

struct PT {
  int sec;
  int usec;
};



void   *PTimer();
double  PTimerSubtract( void *x, void *y);
int     IPTimerSubtract( void *x, void *y );
double  PTimerResolution();
