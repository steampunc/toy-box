#include <array>
#include <fftw3.h>
#include <fstream>
#include <iostream>
#include <math.h>
#include <stdio.h>

// Used everywhere to determine ground truths.
// Complex arrays have N/2 + 1 datapoints.
// Real arrays have N datapoints.
static const int N = 256;

// Used for debugging and so forth.

int main() {
  // Number of collocation points in R

  // Defining datastructures for FFT
  double *in;
  fftw_complex *out;
  fftw_plan forwardPlan, backPlan;

  // Memory allocation
  in = (double *)fftw_malloc(sizeof(double) * N);
  out = (fftw_complex *)fftw_malloc(sizeof(fftw_complex) * (N / 2 + 1));

  // Plan creation - currently 1d but will be 3d
  backPlan = fftw_plan_dft_c2r_1d(N, out, in, FFTW_MEASURE);
  forwardPlan = fftw_plan_dft_r2c_1d(N, in, out, FFTW_MEASURE);

  // Initializing input data - initial conditions will go here
  for (int i = 0; i < N; i++) {
    float theta = M_PI * float(i) / float(N);
    in[i] = std::sin(100 * theta) + std::cos(40 * theta);
  }

  // Way of performing fft
  fftw_execute(forwardPlan); /* repeat as needed */

  // Array lengths go from
  // in: [0, N - 1]
  // out: [0, N/2]

  // Logging the results
  remove("logs.csv");
  std::ofstream logFile;
  logFile.open("logs.csv");
  logFile << "i, in, out_r, out_c, mag" << std::endl;
  for (int i = 0; i < N; i++) {
    if (i <= N / 2) {
      logFile << i << ", " << in[i] << ", " << out[i][0] << ", " << out[i][1]
              << ", " << sqrt(out[i][0] * out[i][0] + out[i][1] * out[i][1])
              << std::endl;
    } else {
      logFile << i << ", " << in[i] << std::endl;
    }
  }
  logFile.close();

  // Unallocating fft-related stuff
  fftw_destroy_plan(forwardPlan);
  fftw_destroy_plan(backPlan);
  fftw_free(in);
  fftw_free(out);

  return 0;
}
