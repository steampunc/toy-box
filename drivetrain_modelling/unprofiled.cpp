#include "model.h"

int main() {
  model::DrivetrainModel model;
  double time = 200;
  for (int i = 0; i < time * 200; i++) {
    controller.Update(model.get_forward_position());
    model.Update(12, -12);
  }
}
