#include "model.h"
#include <iostream>

namespace model {

namespace constants {
constexpr double dt = 0.005;

constexpr double wheel_radius = 0.03; 
constexpr double robot_radius = 0.25;

constexpr double stall_current = 133;
constexpr double stall_torque = 2.42;
constexpr double torque_constant = stall_torque / stall_current;
constexpr double back_emf_constant = torque_constant;

constexpr double gear_ratio = 1.0 / 7.0;
constexpr double resistance = 12.0 / stall_current;
constexpr double moment_of_intertia = 120.0 * (0.4 * 0.4 + 0.35 * 0.35) / 12.0;
}

DrivetrainModel::DrivetrainModel() {
  std::cout << "Left Voltage, Right Voltage, Left Velocity, Right Velocity, Left Angular Velocity, Right Angular Velocity, Left Angular Acceleration, Right Angular Acceleration, Forward Velocity, Angular Velocity" << std::endl;
  status_->position_ = 0.0;
  status_->left_velocity_ = 0.0;
  status_->right_velocity_ = 0.0;
  status_->left_angular_velocity_ = 0.0;
  status_->right_angular_velocity_ = 0.0;
  statangle_ = 0.0;
  angular_velocity_ = 0.0;
}

void DrivetrainModel::Update(double left_voltage, double right_voltage) {
  double left_angular_accel =
      (constants::torque_constant /
          (constants::moment_of_intertia * constants::resistance * constants::gear_ratio)) *
          left_voltage -
      (constants::torque_constant * constants::back_emf_constant /
          (constants::moment_of_intertia * constants::resistance * constants::gear_ratio * constants::gear_ratio)) *
          left_angular_velocity_;

  double right_angular_accel =
      (constants::torque_constant /
          (constants::moment_of_intertia * constants::resistance * constants::gear_ratio)) *
          right_voltage -
      (constants::torque_constant * constants::back_emf_constant /
          (constants::moment_of_intertia * constants::resistance * constants::gear_ratio * constants::gear_ratio)) *
          right_angular_velocity_;

  left_angular_velocity_ += left_angular_accel * constants::dt;
  right_angular_velocity_ += right_angular_accel * constants::dt;

  left_velocity_ = left_angular_velocity_ * constants::wheel_radius;
  right_velocity_ = right_angular_velocity_ * constants::wheel_radius; 

  std::cout << left_voltage << ", " << right_voltage << ", " << left_velocity_ << ", " << right_velocity_ << ", " << left_angular_velocity_ << ", " << right_angular_velocity_ << ", " << left_angular_accel << ", " << right_angular_accel << ", " << get_forward_velocity() << ", " << get_angular_velocity() << std::endl;

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
  return (left_velocity_ - right_velocity_) / constants::robot_radius;
}

}  // namespace model
