use image::{ImageBuffer, Rgb};
use std::cmp::{min};

#[derive(Debug, Clone)]
struct Vector {
    x: f32,
    y: f32,
    z: f32,
}

impl Vector {
    fn len(&self) -> f32 {
        (self.x * self.x + self.y * self.y + self.z * self.z).sqrt()
    }

    fn cross(&self, v: &Vector) -> Vector {
        Vector {
            x: self.y * v.z - self.z * v.y,
            y: self.z * v.x - self.x * v.z,
            z: self.x * v.y - self.y * v.x,
        }
    }

    fn normalize(&self) -> Vector {
        self * (1.0 / self.len())
    }

    fn dot(&self, v: &Vector) -> f32 {
        self.x * v.x + self.y * v.y + self.z * v.z
    }
}

impl std::ops::Add<&Vector> for &Vector {
    type Output = Vector;
    fn add(self, v: &Vector) -> Vector {
        Vector {
            x: self.x + v.x,
            y: self.y + v.y,
            z: self.z + v.z,
        }
    }
}

impl std::ops::Sub<&Vector> for &Vector {
    type Output = Vector;
    fn sub(self, v: &Vector) -> Vector {
        Vector {
            x: self.x - v.x,
            y: self.y - v.y,
            z: self.z - v.z,
        }
    }
}

impl std::ops::Mul<f32> for Vector {
    type Output = Vector;
    fn mul(self, n: f32) -> Vector {
        Vector {
            x: n * self.x,
            y: n * self.y,
            z: n * self.z,
        }
    }
}

impl std::ops::Mul<f32> for &Vector {
    type Output = Vector;
    fn mul(self, n: f32) -> Vector {
        Vector {
            x: n * self.x,
            y: n * self.y,
            z: n * self.z,
        }
    }
}

struct Light {
    position: Vector,
    color: Rgb<u8>,
}

enum ObjectType {
    SphereType(Sphere),
    PlaneType(Plane),
}

struct Sphere {
    position: Vector,
    radius: f32,
}

fn CheckIntersection(object: &Object, ray: &Ray) -> Option<Vector> {
    match &object.obj_type {
        ObjectType::SphereType(sphere) => {
            let pos = &sphere.position - &ray.position;
            let v = pos.dot(&ray.direction);

            let d = sphere.radius.powf(2.0) - (pos.dot(&pos) - v.powf(2.0));

            if d < 0.0 {
                return None
            }

            Some(&ray.position + &(&ray.direction * (v - d.sqrt())))
        }
        ObjectType::PlaneType(plane) => None,
    }
}

struct Plane {
    position: Vector,
    normal: Vector,
}

struct Object {
    obj_type: ObjectType,
}

#[derive(Debug)]
struct Ray {
    position: Vector,
    direction: Vector,
}

fn main() {
    let (width, height) = (1000, 1000);
    println!("Width: {}, Height: {}", width, height);

    let resolution = 1000.0;

    let mut image_data = ImageBuffer::<Rgb<u8>, Vec<u8>>::new(width, height);

    let emitter = Vector {
        x: -1.0,
        y: 1.0,
        z: 0.0,
    };

    let screen_pos = Vector {
        x: 1.0,
        y: 1.0,
        z: 0.0,
    };

    let y_hat = screen_pos.cross(&emitter).normalize();
    let x_hat = y_hat.cross(&(&emitter - &screen_pos)).normalize();

    println!("y_hat: {:?}", &y_hat);
    println!("x_hat: {:?}", &x_hat);
    println!("emitter: {:?}", &emitter);
    println!("screen_pos: {:?}", &screen_pos);

    let light1 = Light {
        position: Vector {
            x: 0.0,
            y: 1.0,
            z: 15.0,
        },
        color: Rgb([243, 0, 0]),
    };

    let light2 = Light {
        position: Vector {
            x: 1.0,
            y: 12.0,
            z: 11.0,
        },
        color: Rgb([0, 240, 255]),
    };

    let sphere1 = Object {
        obj_type: ObjectType::SphereType(Sphere {
            position: Vector {
                x: 3.0,
                y: 1.0,
                z: 0.0,
            },
            radius: 0.1,
        }),
    };

    let objects: [Object; 1] = [sphere1];
    let lights: [Light; 2] = [light1, light2];

    for x in 0..width {
        for y in 0..height {

            let x_pix = &x_hat * ((x as f32 - 0.5 * width as f32) / resolution);
            let y_pix = &y_hat * ((y as f32 - 0.5 * height as f32) / resolution);

            let pixel_pos = &screen_pos + &(&x_pix + &y_pix);
            let tracer_direction = (&pixel_pos - &emitter).normalize();

            let pixel_ray = Ray {
                position: emitter.clone(),
                direction: tracer_direction,
            };

            let mut color = Rgb([0, 0, 0]);
            let mut closest_intersection: Option<Vector> = None;

            for object in objects.iter() {
                let intersection_position = CheckIntersection(object, &pixel_ray);

                match (&intersection_position, &closest_intersection) {
                    (Some(ip), Some(ci)) => {
                        if ip.len() < ci.len() {
                            closest_intersection = Some(ip.clone());
                        }
                    },
                    (Some(ip), None) => {
                        closest_intersection = Some(ip.clone());
                    },
                    _ => (),
                }
            }

            match &closest_intersection {
                Some(ci) => {
                    for light in lights.iter() {
                        let light_ray = Ray {
                            position: ci.clone(),
                            direction: (ci - &light.position).normalize(),
                        };

                        for object in objects.iter() {
                            let intersected = CheckIntersection(object, &light_ray);
                            let mut should_color = false;
                            match &intersected {
                                None => should_color = true,
                                Some(i_point) => {
                                    if (i_point - &light_ray.position).len().powf(2.0) < 0.001 {
                                        should_color = true;
                                    }
                                },
                            }

                            if should_color {

                                let r = min(color[0] as u16 + light.color[0] as u16, 255) as u8;
                                let g = min(color[1] as u16 + light.color[1] as u16, 255) as u8;
                                let b = min(color[2] as u16 + light.color[2] as u16, 255) as u8;

                                color = Rgb([r,g,b]);
                            }


                        }
                    }
                }
                None => color = Rgb([0,0,0]),
            }

            image_data.put_pixel(x, y, color);
        }
    }

    image_data.save("here.png").unwrap();
}
