#include <cmath>
#include <fstream>
#include <iostream>
#include <random>
#include <sstream>
#include <vector>

int main() {

  int image_continuity = 17;
  std::random_device rd;
  std::mt19937 gen(rd());

  int offset = rand() % 3000;
  int r_off = rand() % 1230;
  int g_off = rand() % 120;
  int b_off = rand() % 4000;
  int new_range = 10000;

  for (int k = 1; k <= 1259; k++) {
    unsigned int size = 0;
    unsigned int width = 0;
    unsigned int height = 0;
    unsigned int nr_lines = 0;
    unsigned int nr_columns = 0;
    unsigned int max_col_val = 0;

    std::vector<int> r;
    std::vector<int> g;
    std::vector<int> b;

    std::ifstream input_image("source/image-" + std::to_string(k) + ".ppm",
                              std::ios::in | std::ios::binary);
    // COPIED FROM https://github.com/sol-prog/Perlin_Noise because I didn't
    // want to spend all my time parsing a ppm file.
    if (input_image.is_open()) {
      std::string line;
      std::getline(input_image, line);
      if (line != "P3") {
        std::cout << "Error. Unrecognized file format." << std::endl;
      }
      std::getline(input_image, line);
      while (line[0] == '#') {
        std::getline(input_image, line);
      }
      std::stringstream dimensions(line);

      try {
        dimensions >> width;
        dimensions >> height;
        nr_lines = height;
        nr_columns = width;
      } catch (std::exception &e) {
        std::cout << "Header file format error. " << e.what() << std::endl;
      }

      std::getline(input_image, line);
      std::stringstream col_val(line);
      try {
        col_val >> max_col_val;
      } catch (std::exception &e) {
        std::cout << "Header file format error. " << e.what() << std::endl;
      }

      size = width * height;

      r.reserve(size);
      g.reserve(size);
      b.reserve(size);

      for (unsigned int i = 0; i < size; ++i) {
        int value = 0;
        input_image >> value;
        r[i] = value;
        input_image >> value;
        g[i] = value;
        input_image >> value;
        b[i] = value;
      }
    } else {
      std::cout << "Error. Unable to open file" << std::endl;
    }
    input_image.close();

    std::ofstream out_file("out/out-" + std::to_string(k) + ".ppm",
                           std::ios::out | std::ios::binary);
    if (out_file.is_open()) {

      out_file << "P3\n";
      out_file << width;
      out_file << " ";
      out_file << height << "\n";
      out_file << max_col_val << "\n";

      std::normal_distribution<> d(0, 100);
      std::normal_distribution<> dist_2(0, 150);

      for (unsigned int i = 0; i < size; ++i) {
        if (k % image_continuity == 0) {
          if (i % new_range == 0) {
            offset = int(d(gen)) % size;
            r_off = int(dist_2(gen));
            g_off = int(dist_2(gen));
            b_off = int(dist_2(gen));
            new_range = int(rand()) % 200000 + 10000;
          }
        }
        int real = (offset + i) % size;

        out_file << r[(real + r_off) % size] << " " << g[(real + g_off) % size]
                 << " " << b[(real + b_off) % size] << "\n";
      }
    } else {
      std::cout << "Error. Unable to open." << std::endl;
    }
    std::cout << "Generated image " << k << std::endl;
    if (k % image_continuity == 0) {
      image_continuity = int(rand()) % 83 + 20;
    }
    out_file.close();
  }
}
