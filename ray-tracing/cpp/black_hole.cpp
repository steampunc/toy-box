#include <math.h>
#include <fstream>
#include <iostream>

struct vec3 {
  double x, y, z;
  vec3(double x, double y, double z) : x(x), y(y), z(z) {}
  vec3 operator+(const vec3& v) const {
    return vec3(x + v.x, y + v.y, z + v.z);
  }
  void operator+=(const vec3& v) {
    x += v.x;
    y += v.y;
    z += v.z;
  }
  vec3 operator-(const vec3& v) const {
    return vec3(x - v.x, y - v.y, z - v.z);
  }
  vec3 operator*(double d) const { return vec3(x * d, y * d, z * d); }
  vec3 operator/(double d) const { return vec3(x / d, y / d, z / d); }
  vec3 normalized() const {
    double mg = sqrt(x * x + y * y + z * z);
    return vec3(x / mg, y / mg, z / mg);
  }
  double dot(vec3 v) const { return x * v.x + y * v.y + z * v.z; }
  vec3 cross(vec3 v) const { return vec3(y * v.z - z * v.y, z * v.x - x * v.z, x * v.y - y * v.x); }
  double norm() const { return sqrt(x * x + y * y + z * z); }
};

class Ray {
 public:
  Ray(vec3 position_, vec3 direction_)
      : position(position_), direction(direction_) {
		  collided = false;
  }
  vec3 position, direction;
  bool collided;
};

void print(Ray r) {
	std::cout << "Pos: " << r.position.x << " " << r.position.y << " " << r.position.z << std::endl;
	std::cout << "Dir: " << r.direction.x << " " << r.direction.y << " " << r.direction.z << std::endl;
	std::cout << "Col: " << r.collided << std::endl;
}

void print(vec3 p) {
	std::cout << p.x << " " << p.y << " " << p.z << std::endl;
}

void print(float f) {
	std::cout << f << std::endl;
}

// Calculates velocity of light at a particular position in space.
float rs = 1.0;
float velocity(vec3 pos) {
    float lr = pos.norm();
    return sqrt(1.0 - rs/(4.0 * lr)) / pow(1.0 + rs / (4.0 * lr), 2.5);
}

// Integrates light through scene following Snell's law.
vec3 updateRay(Ray ray, float dl, float dt) {
	vec3 r_perp = ray.position.normalized();
	vec3 out_vec = ray.direction.cross(r_perp);
	vec3 dir_perp = out_vec.cross(ray.direction).normalized();

	float vi = velocity(ray.position - dir_perp * dl / 2.0);
	float vo = velocity(ray.position + dir_perp * dl / 2.0);

	float theta = atan((vi - vo) * dt / dl);

	vec3 dir = ray.direction * cos(theta) + dir_perp * sin(theta); 
	dir = dir.normalized();
	return dir;
}

bool checkCollision(Ray* ray, float step, vec3 position, vec3 normal_face, float radius) {
	if (ray->position.norm() < rs) {
		return true;
	}
	double dot_prod = (ray->direction).dot(normal_face);
	if (abs(dot_prod) < 1e-4) {
		return false;
	} else {
		return false;
	}
	return false;
}

vec3 get_color(vec3 direction) {
	float xdir = vec3(1.0, 0.0, 0.0).dot(direction);
	float ydir = vec3(0.0, 1.0, 0.0).dot(direction);
	float zdir = vec3(0.0, 0.0, 1.0).dot(direction);
	vec3 color = vec3(0.0, 0.0, 0.0);
	if (xdir > 0) {
		if (ydir > 0) {
			if (zdir > 0) {
				color = vec3(128, 0, 0);	
			} else {
				color = vec3(0, 128, 0);
			}
		} else {
			if (zdir > 0) {
				color = vec3(0, 0, 128);
			} else {
				color = vec3(128, 0, 128);
			}
		}
	} else {
		if (ydir > 0) {
			if (zdir > 0) {
				color = vec3(128, 128, 0);	
			} else {
				color = vec3(0, 128, 128);
			}
		} else {
			if (zdir > 0) {
				color = vec3(255, 128, 128);
			} else {
				color = vec3(128, 255, 128);
			}
		}
	}
	return color;
}

vec3 skybox(vec3 direction, int x) {
	vec3 pixel_color = vec3(255.0, 255.0, 255.0);
	if (direction.dot(vec3(0, 0, 1)) > 0.9995) {return vec3(255.0, 0.0, 0.0);}
	float theta = acos(vec3(0.0, 1.0, 0.0).dot(direction));
	float phi = acos(vec3(1.0, 0.0, 0.0).dot(direction));
	if (fmod(phi, acos(0.0) / 5.0) < acos(0.0) / 10.0) {
		if (fmod(theta, acos(0.0) / 5.0) < acos(0.0) / 10.0) {
			pixel_color = get_color(direction);
		}
	} else {
		if (fmod(theta, acos(0.0) / 5.0) > acos(0.0) / 10.0) {
			pixel_color = get_color(direction);
		}
	}
	return pixel_color;
}

int main() {
  // Defining image dims
  uint32_t width = 1000;
  uint32_t height = 1000;

  std::ofstream image("image.ppm");
  image << "P3\n"
	<< width << " " << height << " "
	<< "255\n";

  // Camera's position and field of view within the scene.
  double camera_distance = 10;
  vec3 camera_pos =
      vec3(0.0, 0.0, -camera_distance);
  float dt = 0.1;
  float dl = 0.01;

  // Now, iterating through every pixel in the image, we create a
  // ray for that pixel in the correct direction.
  for (int x = 0; x < width; x++) {
    for (int y = 0; y < height; y++) {
	  //std::cout << "xy:" << x << " " << y << std::endl;

      vec3 pixel_color = vec3(255.0, 255.0, 255.0);

	  float c = 1.0;
	  vec3 aspect = vec3(1.0/float(width), 1.0/float(height), 0.0);
	  vec3 screen_pos = vec3(aspect.x * (x - int(width / 2)), aspect.y * (y - int(height / 2)), -camera_distance + c);
      vec3 direction = (screen_pos - camera_pos).normalized();

      Ray ray = Ray(camera_pos + direction, direction);
	  float init_dist = ray.position.norm() + 1.0;
	  //print(ray);
	  while (ray.position.norm() < init_dist && !ray.collided) {
		  float step = velocity(ray.position) * dt;
		  ray.position += ray.direction * step;
		  ray.direction = updateRay(ray, dl, dt); 
		  ray.collided = checkCollision(&ray, step, vec3(0, 0, 0), vec3(1.0, 0.0, 0.1).normalized(), 2.0);
	  }

	  if (ray.collided) {
		  pixel_color = vec3(0.0, 0.0, 0.0);
	  } else { 
	  	pixel_color = skybox(ray.direction, x);
	  }

	  // Writing pixel to file
      image << int(abs(int(pixel_color.x)) > 255
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
