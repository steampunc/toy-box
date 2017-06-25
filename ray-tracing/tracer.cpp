#include <iostream>
#include <fstream>
#include <cmath>
#include <limits>
#include <memory>
#include <cstdint>
#include <vector>

struct Vector3d {
  double x, y, z;
  Vector3d(double x, double y, double z) : x(x), y(y), z(z) {}
  Vector3d operator+(const Vector3d& v) const {
    return Vector3d(x + v.x, y + v.y, z + v.z);
  }
  void operator+=(const Vector3d& v) {
    x += v.x;
    y += v.y;
    z += v.z;
  }
  Vector3d operator-(const Vector3d& v) const {
    return Vector3d(x - v.x, y - v.y, z - v.z);
  }
  Vector3d operator*(double d) const { return Vector3d(x * d, y * d, z * d); }
  Vector3d operator/(double d) const { return Vector3d(x / d, y / d, z / d); }
  Vector3d normalized() const {
    double mg = sqrt(x * x + y * y + z * z);
    return Vector3d(x / mg, y / mg, z / mg);
  }
  double dot(Vector3d v) const { return x * v.x + y * v.y + z * v.z; }
  double norm() const { return sqrt(x * x + y * y + z * z); }
};

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
  Light(Vector3d position, Vector3d color)
      : position_(position), color_(color) {}
  Vector3d position_;
  Vector3d color_;
};

class Object {
 public:
  virtual bool CheckIntersection(Ray* ray) { return false; }
  virtual Vector3d CalculateLight(
      Ray ray, std::vector<Light> lights,
      std::vector<std::shared_ptr<Object>> objects) {
    return Vector3d(0, 0, 0);
  }
};

class Plane : public Object {
 public:
  Plane(Vector3d position, Vector3d normal_face, bool disk = false,
        double radius = 0)
      : position_(position),
        normal_face_(normal_face.normalized()),
        disk_(disk),
        radius_(radius) {}

  bool CheckIntersection(Ray* ray) override {
    double dot_prod = (ray->direction_).dot(normal_face_);
    if (dot_prod > 1e-6) {
      Vector3d intersection_vector = position_ - ray->position_;
      double t = intersection_vector.dot(normal_face_) / dot_prod;
      if (ray->nearest_intersection > t && t >= 0) {
        if (disk_) {
          Vector3d intersection_point = ray->position_ + ray->direction_ * t;
          Vector3d v = intersection_point - position_;
          double d_squared = v.dot(v);
          if (d_squared <= radius_ * radius_) {
            ray->nearest_intersection = t;
            return true;
          }
        } else {
          ray->nearest_intersection = t;
          return true;
        }
      }
    }
    return false;
  }

  Vector3d CalculateLight(
      Ray ray, std::vector<Light> lights,
      std::vector<std::shared_ptr<Object>> objects) override {
    Vector3d intersect =
        ray.position_ + ray.direction_ * ray.nearest_intersection;

    Vector3d color = Vector3d(0, 0, 0);
    for (uint32_t i = 0; i < lights.size(); i++) {
      Vector3d light_source = (intersect - lights[i].position_).normalized();
      double intensity = normal_face_.dot(light_source);
      intensity = std::max(intensity, 0.0);

      Ray shadow_ray = Ray(intersect - light_source.normalized(),
                           Vector3d(0, 0, 0) - light_source);
      bool should_be_lit = true;
      for (uint32_t j = 0; j < objects.size(); j++) {
        if (objects[j]->CheckIntersection(&shadow_ray)) {
          should_be_lit = false;
        }
      }

      color += lights[i].color_ * intensity * should_be_lit;
    }

    return color;
  }

  Vector3d position_, normal_face_;
  bool disk_;
  double radius_;
};

class Sphere : public Object {
 public:
  Sphere(Vector3d position, double radius)
      : position_(position), radius_(radius) {}

  bool CheckIntersection(Ray* ray) override {
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

  Vector3d CalculateLight(
      Ray ray, std::vector<Light> lights,
      std::vector<std::shared_ptr<Object>> objects) override {
    Vector3d intersect =
        ray.position_ + ray.direction_ * ray.nearest_intersection;

    Vector3d normal = (intersect - position_).normalized();

    Vector3d color = Vector3d(0, 0, 0);
    for (uint32_t i = 0; i < lights.size(); i++) {
      Vector3d light_source = (lights[i].position_ - intersect).normalized();
      double intensity = normal.dot(light_source);
      intensity = std::max(intensity, 0.0);

      Ray shadow_ray = Ray(intersect - light_source.normalized(),
                           Vector3d(0, 0, 0) + light_source);
      bool should_be_lit = true;

      for (uint32_t j = 0; j < objects.size(); j++) {
        if (objects[j]->CheckIntersection(&shadow_ray)) {
          should_be_lit = false;
        }
      }

      color += lights[i].color_ * intensity * should_be_lit;
    }

    return color;
  }

 private:
  Vector3d position_;
  double radius_;
};

int main() {
  uint32_t width = 1000;
  uint32_t height = 1000;

  std::ofstream image("image.ppm");
  image << "P3\n" << width << " " << height << " "
        << "255\n";

  double camera_distance = 1000;
  Vector3d camera_pos =
      Vector3d(0.5 * double(width), 0.5 * double(height), -camera_distance);

  std::vector<std::shared_ptr<Object>> objects;

  objects.push_back(
      std::make_shared<Sphere>(Sphere(Vector3d(170, 700, 200), 50)));
  objects.push_back(
      std::make_shared<Sphere>(Sphere(Vector3d(500, 500, 500), 200)));
  objects.push_back(std::make_shared<Plane>(Plane(
      Vector3d(700, 700, 400), Vector3d(0, 1, 1).normalized(), false, 50)));

  std::vector<Light> lights;
  lights.push_back(Light(Vector3d(0, 0, 0), Vector3d(255, 0, 0)));
  lights.push_back(Light(Vector3d(0, 500, 0), Vector3d(0, 255, 0)));
  lights.push_back(Light(Vector3d(0, 1000, 0), Vector3d(0, 0, 255)));

  for (int x = 0; x < width; x++) {
    for (int y = 0; y < height; y++) {
      Vector3d pixel_color = Vector3d(0, 0, 0);

      Vector3d screen_pos = Vector3d(x, y, 0);
      Vector3d direction = (screen_pos - camera_pos).normalized();
      Ray ray = Ray(camera_pos, direction);

      for (uint32_t i = 0; i < objects.size(); i++) {
        if (objects[i]->CheckIntersection(&ray)) {
          pixel_color = objects[i]->CalculateLight(ray, lights, objects);
        }
      }

      image << int(pixel_color.x) << " " << int(pixel_color.y) << " "
            << int(pixel_color.z) << "\n";
    }
  }
}
