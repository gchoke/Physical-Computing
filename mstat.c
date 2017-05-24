
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

#define MAX 250

int cmp (float *num1, float *num2)
{
  if (*num1 < *num2) return -1;
  else if (*num1 == *num2) return 0;
  return 1;
}

int main(int argc, char *argv[])
{
    char *buffer = NULL;
    size_t len;
    int read = 0;
    float x[MAX];
    int i = 0;
    float sum = 0.0;

    while ( (read = getline(&buffer, &len, stdin)) != EOF ) { 

        if ( i < MAX-1 ) {
            x[i] = atof(buffer);
            sum += x[i];
        } else {
            printf("Maximum data points exceeded(%d)\n", MAX);
            exit(1);
        }
        i++;
    }
    int n = i;

    /*
    printf("Before: \n");
       for (int i=0; i < n; i++)
            printf("%g\n", x[i]);
    */

    qsort (x,n,sizeof(float),
             (int (*)(const void *, const void *)) cmp);

    /*
    printf("After: \n");
       for (int i=0; i < n; i++)
            printf("%g\n", x[i]);
    */
    int mid = n / 2;
    float median;

    if ( n % 2 == 0 ) 
        median = (x[mid-1] + x[mid])/2;
    else
        median = x[mid];

    float mean, sd, var, dev,
    sdev = 0.0, cv;

    mean = sum / n;

    for(i = 1; i <= n; ++i){
        dev = (x[i] - mean)*(x[i] - mean);
        sdev = sdev + dev;
    }

    var = sdev / (n - 1);

    sd = sqrt(var);

    cv = (sd / mean) * 100;

    /*
    printf("Variance: %6.3f\n", var);

    printf("Standard Deviation: %6.3f\n", sd);

    printf("Coefficient of Variation: %6.3f%%\n", cv);
    */

    printf(" N      Min     Med      Max      Avg      Var      SD       CV%%\n");
    printf("%3d  %g  %g  %g  %g  %g  %g  %g\n",
    n, x[0], median, x[n-1], mean, var, sd, cv);
    return 0;

}
