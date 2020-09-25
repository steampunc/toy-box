#include <fftw3.h>
//
// Created by finn on 3/1/20.
//

double *duplicateReal(double *a, int N) {
  double *b;
  b = (double *) fftw_malloc(sizeof(double) * N);
  for (int i = 0; i < N; i++) {
    b[i] = a[i];
  }
  return b;

}

fftw_complex *duplicateComplex(fftw_complex *a, int N) {
  fftw_complex *b;
  b = (fftw_complex *) fftw_malloc(sizeof(fftw_complex) * (N / 2 + 1));
  for (int i = 0; i < N/2 + 1; i++) {
    b[i][0] = a[i][0];
    b[i][1] = a[i][1];
  }
  return b;
}
