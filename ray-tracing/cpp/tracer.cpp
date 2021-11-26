#include <cmath>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <memory>
#include <random>
#include <vector>

/* A Barebones C++ Ray Tracer */

// My nice little vector class.
// Supports adding, subtracting, scaling, normalizing, and dot
// products. That's all the necessary operations for a ray tracer,
// and I rely on it frequently.
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

// The fundamental building block of the ray tracer, which encapsulates
// a "pointing vector", direction_, and the position of the ray.
// Finally, it maintains a value for the closest point of intersection,
// which allows us to determine which object to render on that pixel.
class Ray {
 public:
  Ray(Vector3d position, Vector3d direction)
      : position_(position), direction_(direction) {
    nearest_intersection = std::numeric_limits<double>::infinity();
  }

  Vector3d position_, direction_;
  double nearest_intersection;
};

// Lights are another fundemental part of the ray tracer, and are what
// determine the color values of the objects which the rays intersect.
// You can see their use within the CalculateLight functions of
// objects.
class Light {
 public:
  Light(Vector3d position, Vector3d color)
      : position_(position), color_(color) {}
  Vector3d position_;
  Vector3d color_;
};

// This parent class makes the process of using a variety of
// different objects within the scene very simple. They all inherit
// the Object class and override the default functions to
// modify the functionality depending on the object.
class Object {
 public:
  virtual bool CheckIntersection(Ray* ray) { return false; }
  virtual Vector3d CalculateLight(
      Ray ray, std::vector<Light> lights,
      std::vector<std::shared_ptr<Object>> objects) {
    return Vector3d(0, 0, 0);
  }
};

// The Plane class is one such instance of an inherited object.
class Plane : public Object {
 public:
  // We define an infinite plane with a normal vector and a point through which 
  // the plane intersects. Optionally, we can also define a radius and
  // make the plane a finite disk.
  Plane(Vector3d position, Vector3d normal_face, bool disk = false,
	double radius = 0)
      : position_(position),
	normal_face_(normal_face.normalized()),
	disk_(disk),
	radius_(radius) {}

  bool CheckIntersection(Ray* ray) override {
    double dot_prod = (ray->direction_).dot(normal_face_);
	// To see if a ray intersects a plane, the ray must not be parallel to the plane.
	// This means the dot product between a ray and the plane's normal vector
	// must be nonzero.
    if (dot_prod > 1e-6) {
	  // If it intersects the plane, we then determine the point of intersection by
	  // projecting the ray onto the plane.
      Vector3d intersection_vector = position_ - ray->position_;
      double t = intersection_vector.dot(normal_face_) / dot_prod;
      if (ray->nearest_intersection > t && t >= 0) {
		// Handling the disk logic.
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
	  // We determine the lighting of the plane at the point of intersection by again
   	  // casting rays from the point of intersection to all of the lights which are
	  // in the scene. If they are obscured (i.e. another object intersects this ray),
	  // we do not involve that light in computing the color of that pixel.
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

	  // Optionally adding noise to create a fuzzier image. This isn't really
	  // fundamental to the raytracing itself.
      double k_noise = 0;
      double a = (drand48() - 0.5) / 0.5 * k_noise;
      double b = (drand48() - 0.5) / 0.5 * k_noise;
      double c = (drand48() - 0.5) / 0.5 * k_noise;

      lights[i].color_ =
	  Vector3d(lights[i].color_.x + a, lights[i].color_.y + b,
		   lights[i].color_.z + c);

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
	// Spheres have slightly more complex ray intersection calculations, but they
	// more or less break down to some geometry and linear algebra. A good
	// handling of this math is at the following link:
	// https://facultyweb.cs.wwu.edu/~wehrwes/courses/csci480_21w/lectures/L07/L07_notes.pdf
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
	// Similar logic to the Plane object, we iterate through all the lights and
	// figure out which are unobscured when coming from the point of intersection.
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
      double k_noise = 0;
      double a = (drand48() - 0.5) / 0.5 * k_noise;
      double b = (drand48() - 0.5) / 0.5 * k_noise;
      double c = (drand48() - 0.5) / 0.5 * k_noise;

      lights[i].color_ =
	  Vector3d(lights[i].color_.x + a, lights[i].color_.y + b,
		   lights[i].color_.z + c);

      color += lights[i].color_ * intensity * should_be_lit;
    }

    return color;
  }

 private:
  Vector3d position_;
  double radius_;
};

int main() {
  // Defining the image dimensions and initializing the image as a
  // ppm, which is really easy to create and modify, but is definitely
  // not an efficient image in terms of compression.
  uint32_t width = 1000;
  uint32_t height = 1000;

  std::ofstream image("image.ppm");
  image << "P3\n"
	<< width << " " << height << " "
	<< "255\n";

  // Establishing the camera's position and field of view within the scene.
  double camera_distance = 1000;
  Vector3d camera_pos =
      Vector3d(0.5 * double(width), 0.5 * double(height), -camera_distance);

  // Populating the scene with a variety of objects. Since
  // all the types of geometries inherit from the Object class,
  // we can store them within the object vector in a relatively
  // clean manner.
  std::vector<std::shared_ptr<Object>> objects;

  // You can append any objects to the scene. In this case, we have two spheres
  // and a plane.
  objects.push_back(
      std::make_shared<Sphere>(Sphere(Vector3d(170, 700, 200), 50)));
  objects.push_back(
      std::make_shared<Sphere>(Sphere(Vector3d(500, 500, 500), 200)));
  objects.push_back(std::make_shared<Plane>(Plane(
      Vector3d(700, 700, 400), Vector3d(0, 1, 1).normalized(), false, 50)));

  // We handle the light separately - they do not play the same role
  // as objects, and are used to calculate the color value of each pixel.
  std::vector<Light> lights;
  lights.push_back(Light(Vector3d(0, 0, 0), Vector3d(255, 0, 0)));
  lights.push_back(Light(Vector3d(0, 500, 0), Vector3d(0, 255, 0)));
  lights.push_back(Light(Vector3d(0, 1000, 0), Vector3d(0, 0, 255)));

  // Now, iterating through every pixel in the image, we create a
  // ray for that pixel in the correct direction.
  for (int x = 0; x < width; x++) {
    for (int y = 0; y < height; y++) {
      Vector3d pixel_color = Vector3d(0, 0, 0);

      Vector3d screen_pos = Vector3d(x, y, 0);

      Vector3d direction = (screen_pos - camera_pos).normalized();
      Ray ray = Ray(camera_pos, direction);

	  // After creating the ray, we iterate through all the objects and find
	  // which one has the nearest intersection. This point of intersection
	  // is updated and stored internally within the ray.
      for (uint32_t i = 0; i < objects.size(); i++) {
		 if (objects[i]->CheckIntersection(&ray)) {
		   pixel_color = objects[i]->CalculateLight(ray, lights, objects);
		 }
      }

	  // After using the lights to determine the pixel color, we write
	  // it to the image file.
      image << int(int(pixel_color.x) > 255
		       ? 255
		       : (int(pixel_color.x) < 0 ? 0 : int(pixel_color.x)))
	    << " "
	    << int(int(pixel_color.y) > 255
		       ? 255
		       : (int(pixel_color.y) < 0 ? 0 : int(pixel_color.y)))
	    << " "
	    << int(int(pixel_color.z) > 255
		       ? 255
		       : (int(pixel_color.z) < 0 ? 0 : int(pixel_color.z)))
	    << "\n";
    }
  }
}
