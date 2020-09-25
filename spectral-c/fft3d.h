#ifndef SPECTRAL_C_LIBRARY_H
#define SPECTRAL_C_LIBRARY_H

#include <fftw3.h>

class FFT3d {
public:
  FFT3d(int Nx, int Ny, int Nz, double *in, fftw_complex *out);
  void forward();
  void backward();
};

#endif // SPECTRAL_C_LIBRARY_H
