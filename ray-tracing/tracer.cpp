#include <opencv2/opencv.hpp>
#include <iostream>
#include <limits>
#include <memory>
#include "eigen/Eigen/Dense"

using namespace cv;
using namespace Eigen;

class Ray {
 public:
  Ray(Vector3d position, Vector3d direction)
      : position_(position), direction_(direction) {
    nearest_intersection = std::numeric_limits<double>::infinity();
  }

  Vector3d position_, direction_;
  double nearest_intersection;
};

class Light {
 public:
  Light(Vector3d position, Vec3b color) : position_(position), color_(color) {}
  Vector3d position_;
  Vec3b color_;
};

class Object {
 public:
  virtual bool CheckIntersection(Ray* ray) { return false; }
  virtual Vec3b CalculateLight(Ray ray, std::vector<Light> lights) {
    return Vec3b(0, 0, 0);
  }
};

class Sphere : public Object {
 public:
  Sphere(Vector3d position, double radius)
      : position_(position), radius_(radius) {}

  bool CheckIntersection(Ray* ray) override {
    std::cout << "HELLO??" << std::endl;
    Vector3d hypotenuse = position_ - ray->position_;

    double line_to_point = hypotenuse.dot(ray->direction_);
    if (line_to_point < 0) return false;

    double d = hypotenuse.dot(hypotenuse) - line_to_point * line_to_point;
    if (d < 0 || d > radius_ * radius_) return false;

    double l = sqrt(radius_ * radius_ - d);
    double t0 = line_to_point - l;
    double t1 = line_to_point + l;

    if (t0 < 0 && t1 < 0) return false;
    if (t0 < 0) t0 = std::numeric_limits<double>::infinity();
    if (t1 < 0) t1 = std::numeric_limits<double>::infinity();
    if (ray->nearest_intersection > std::min(t0, t1)) {
      ray->nearest_intersection =
          std::min(ray->nearest_intersection, std::min(t0, t1));
      return true;
    }
    return false;
  }

  Vec3b CalculateLight(Ray ray, std::vector<Light> lights) override {
    Vector3d intersect =
        ray.position_ + ray.direction_ * ray.nearest_intersection;

    Vector3d normal = (intersect - position_).normalized();

    Vec3b color = Vec3b(0, 0, 0);
    for (uint32_t i = 0; i < lights.size(); i++) {
      Vector3d light_source = (lights[i].position_ - position_).normalized();
      double intensity = normal.dot(light_source);
      intensity = std::max(intensity, 0.0);
      color += intensity * lights[i].color_;
    }

    return color;
  }

 private:
  Vector3d position_;
  double radius_;
};

int main() {
  Mat image(1000, 1000, CV_8UC3, Scalar(255, 255, 255));

  double camera_distance = 1000;
  Vector3d camera_pos = Vector3d(0.5 * double(image.cols),
                                 0.5 * double(image.rows), -camera_distance);
  std::cout << __cplusplus << std::endl;

  std::vector<std::unique_ptr<Object>> objects;

  objects.push_back(
      std::make_unique<Sphere>(Sphere(Vector3d(100, 100, 100), 100)));
  objects.push_back(
      std::make_unique<Sphere>(Sphere(Vector3d(200, 200, 1000), 100)));

  std::vector<Light> lights;
  lights.push_back(Light(Vector3d(0, 0, 0), Vec3b(255, 0, 0)));
  lights.push_back(Light(Vector3d(1000, 1000, 0), Vec3b(0, 255, 0)));

  for (int x = 0; x < image.cols; x++) {
    for (int y = 0; y < image.rows; y++) {
      Vec3b pixel_color = Vec3b(0, 0, 0);

      Vector3d screen_pos = Vector3d(x, y, 0);
      Vector3d direction = (screen_pos - camera_pos).normalized();
      Ray ray = Ray(camera_pos, direction);

      for (uint32_t i = 0; i < objects.size(); i++) {
        if (objects[i]->CheckIntersection(&ray)) {
          pixel_color = objects[i]->CalculateLight(ray, lights);
        }
      }

      image.at<Vec3b>(y, x) = pixel_color;
    }
  }
  imshow("post_image", image);
  waitKey();
}
