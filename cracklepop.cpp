#include <iostream>
#include <string> 

int main() {
  for (int i = 1; i<=100; i++) {
    std::cout << ((i % 3 !=0 && i%5 !=0) ? std::to_string(i) : "") // Goodness, this is kinda ugly. I realize now a neater way to do it (adding strings) but this was my first thought.
	      << ((i % 3 == 0) ? "Crackle" : "")
	      << ((i % 5 == 0) ? "Pop" : "") << std::endl;
  }
  return 0;
}
