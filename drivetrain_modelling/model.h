#ifndef MODEL_H_
#define MODEL_H_

namespace model {

class DrivetrainModel {
 public:
  DrivetrainModel();
  ~DrivetrainModel() = default;

  void Update(double left_voltage, double right_voltage);

  void Reset();

  double get_position();
  double get_left_velocity();
  double get_right_velocity();
  double get_forward_velocity();
  double get_angle();
  double get_angular_velocity();

 private:
  double position_, left_velocity_, right_velocity_, left_angular_velocity_,
      right_angular_velocity_, angle_, angular_velocity_;
};

}  // namespace model

#endif  // MODEL_H_
