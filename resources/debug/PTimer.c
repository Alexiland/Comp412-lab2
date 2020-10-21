#include "PTimer.h"
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <sys/time.h>
#include <sys/times.h>
#include <sys/resource.h>
#include <math.h>

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

#define log10(x) ((int) (log((double) x) / log(10.0)))


static struct rusage Pool[10];
static int counter = 0;

static int resolution = 0;
static int Save;

/* Simple (and portable) routine to compute integer exponents                     */
static int power( int base, int exponent)
{
  int ans = 1;

  while(exponent-- > 0)
    {
      ans = ans * base;
    }
  return ans;
}



double PTimerResolution()
{
  int inner, outer, i, j;

  void *start, *finish;

  double clock_time = 0.0;

  inner = 1;
  outer = 1;

  while(clock_time == 0.0)
  {
    if (inner < 1000000000)
      inner = inner + inner;
    else 
      outer++;
  
    start = PTimer();

    i = outer;
    while (i > 0)
    {
      j = inner;
      while(j > 0)
      {
	j--;
      }
      i--;
    }

    finish = PTimer();
    clock_time = PTimerSubtract(finish,start);
    fprintf(stderr,"--> <%d : %d> in %f seconds.\n",outer,inner,clock_time);
    Save = j;
  }

  /* Take floor to nearest unit... 0.004 becomes 0.001  */
  return pow(10,floor(log10(clock_time)));
}



void *PTimer()
{
  struct rusage *p;

  p = &Pool[counter];

  if (getrusage(RUSAGE_CHILDREN, p) != 0)
  {
    fprintf(stderr,"Call to getrusage(RUSAGE_CHILDREN, *) failed.\n");
    fprintf(stderr,"Fatal problem running PTimer().\n");
    exit(-1);
  }

  counter++;
  if (counter > 9)
    counter = 0;

  return (void *) p;
}

double PTimerSubtract( void * x, void * y)
{
  struct rusage *xp, *yp;
  struct timeval *xtu, *xts, *ytu, *yts;
  int usec, sec;

  double result;

  xp = (struct rusage *) x;
  yp = (struct rusage *) y;

  xtu = &xp->ru_utime;  /* user time */
  xts = &xp->ru_stime;  /* system time */
  ytu = &yp->ru_utime;  /* user time */
  yts = &yp->ru_stime;  /* system time */

  /* subtract microseconds and seconds separately */
  usec = (int) ((xtu->tv_usec + xts->tv_usec) - (ytu->tv_usec + yts->tv_usec));
  sec  = (int) ((xtu->tv_sec  + xts->tv_sec ) - (ytu->tv_sec  + yts->tv_sec ));

  /* now, combine them into a double precision floating point number */
  result = (double) sec + ((double) usec / 1000000.0);
  return result;
}


int IPTimerSubtract( void * x, void * y)
{
  struct rusage *xp, *yp;
  struct timeval *xtu, *xts, *ytu, *yts;
  int usec, sec;

  int result;

  xp = (struct rusage *) x;
  yp = (struct rusage *) y;

  xtu = &xp->ru_utime;  /* user time */
  xts = &xp->ru_stime;  /* system time */
  ytu = &yp->ru_utime;  /* user time */
  yts = &yp->ru_stime;  /* system time */

  /* subtract microseconds and seconds separately */
  usec = (xtu->tv_usec + xts->tv_usec) - (ytu->tv_usec + yts->tv_usec);
  sec  = (xtu->tv_sec  + xts->tv_sec ) - (ytu->tv_sec  + yts->tv_sec );

  if (sec > 2000)
  {
    fprintf(stderr,"IPTimerSubtract() used on an interval of > 2000 seconds.\n");
    fprintf(stderr,"Use PTimerSubtract() instead.\n");
    exit(-1);
  }

  result = sec * 1000000 + usec;

  return result;
}



