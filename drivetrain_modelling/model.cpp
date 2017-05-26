#include "model.h"

namespace model {

namespace constants {

constexpr double radius = 0.25;
constexpr double torque_constant = 0;
constexpr double back_emf_constant = 0;
constexpr double resistance = 0;
constexpr double moment_of_intertia = 0;
}

DrivetrainModel::DrivetrainModel() {
  position_ = 0;
  left_velocity_ = 0;
  right_velocity_ = 0;
  left_angular_velocity_ = 0;
  right_angular_velocity_ = 0;
  angle_ = 0;
  angular_velocity_ = 0;
}

void DrivetrainModel::Update(double left_voltage, double right_voltage) {
  double left_angular_accel =
      constants::torque_constant /
          (constants::moment_of_intertia * constants::resistance) *
          left_voltage -
      constants::torque_constant * constants::back_emf_constant /
          (constants::moment_of_intertia * constants::resistance) *
          left_angular_velocity_;

  double right_angular_accel =
      constants::torque_constant /
          (constants::moment_of_intertia * constants::resistance) *
          right_voltage -
      constants::torque_constant * constants::back_emf_constant /
          (constants::moment_of_intertia * constants::resistance) *
          right_angular_velocity_;
}

void DrivetrainModel::Reset() {
  position_ = 0;
  left_velocity_ = 0;
  right_velocity_ = 0;
  left_angular_velocity_ = 0;
  right_angular_velocity_ = 0;
  angle_ = 0;
  angular_velocity_ = 0;
}

// Getters
double DrivetrainModel::get_position() { return position_; }

double DrivetrainModel::get_left_velocity() { return left_velocity_; }

double DrivetrainModel::get_right_velocity() { return right_velocity_; }

double DrivetrainModel::get_forward_velocity() {
  return (left_velocity_ + right_velocity_) / 2.0;
}

double DrivetrainModel::get_angle() { return angle_; }

double DrivetrainModel::get_angular_velocity() {
  return (left_velocity_ - right_velocity_) / constants::radius;
}

}  // namespace model
