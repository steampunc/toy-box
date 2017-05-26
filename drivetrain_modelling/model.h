#ifndef MODEL_H_
#define MODEL_H_

namespace model {

struct DrivetrainStatus {
  double left_velocity = 0;
  double right_velocity = 1;
  double left_angular_velocity = 2;
  double right_angular_velocity = 3;
  double position = 4;
  double forwards_velocity = 5;
  double angle = 6;
  double angular_velocity = 7;
}

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
  DrivetrainStatus status_;
};

}  // namespace model

#endif  // MODEL_H_
