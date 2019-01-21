#include <cmath>
#include <complex>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <memory>
#include <vector>

int main() {
  double width = 4096;
  double height = 2160;
  double cx = 0;
  double cy = -0.5;
  double sx = 0.25;
  double sy = (width / height) * sx;
  uint32_t max_iter = 255;
  uint32_t threshold = 2;

  std::ofstream image("image.ppm");
  image << "P3\n"
	<< int(width) << " " << int(height) << " "
	<< "255\n";

  using namespace std::complex_literals;

  std::complex<double> c = 1.0 + 2i;

  for (int y = 0; y < height; y++) {
    for (int x = 0; x < width; x++) {
      double a = ((y - height / 2) * (1 / sy)) / height + cy;
      double b = ((x - width / 2) * (1 / sx)) / width + cx;
      std::complex<double> c = a + b * 1i;
      std::complex<double> z = 0;

      int color = 0;

      for (int i = 0; i <= max_iter; i++) {
	z = z * z + c;
	if (abs(z) > threshold) {
	  color = i;
	  break;
	} else {
	  color = 255;
	}
      }
      image << color << " " << color << " " << color << "\n";
    }
  }
}
