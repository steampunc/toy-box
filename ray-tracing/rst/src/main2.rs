use image::{ImageBuffer, Rgb};
use std::cmp::{min};
mod vector;

struct Light {
    position: vector::Vector,
    color: Rgb<u8>,
}

enum ObjectType {
    SphereType(Sphere),
    PlaneType(Plane),
}

struct Sphere {
    position: vector::Vector,
    radius: f32,
}

fn CheckIntersection(object: &Object, ray: &Ray) -> Option<vector::Vector> {
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

fn GetNormalVector(object: &Object, position: &vector::Vector) -> vector::Vector {
    match &object.obj_type {
        ObjectType::SphereType(sphere) => {
            (position - &sphere.position).normalize()
        }
        ObjectType::PlaneType(plane) => {
            plane.normal.clone()
        }
    }
}

struct Plane {
    position: vector::Vector,
    normal: vector::Vector,
}

struct Object {
    obj_type: ObjectType,
    reflectivity: f32,
}

fn main() {
    let (width, height) = (1000, 1000);
    println!("Width: {}, Height: {}", width, height);

    let resolution = 1000.0;

    let mut image_data = ImageBuffer::<Rgb<u8>, Vec<u8>>::new(width, height);

    let emitter = vector::Vector {
        x: -1.0,
        y: 1.0,
        z: 0.0,
    };

    let screen_pos = vector::Vector {
        x: 1.0,
        y: 1.0,
        z: 0.0,
    };

    let reflection_depth: u8 = 4;
    let ambient_coefficient: f32 = 0.05;

    let y_hat = screen_pos.cross(&emitter).normalize();
    let x_hat = y_hat.cross(&(&emitter - &screen_pos)).normalize();

    println!("y_hat: {:?}", &y_hat);
    println!("x_hat: {:?}", &x_hat);
    println!("emitter: {:?}", &emitter);
    println!("screen_pos: {:?}", &screen_pos);

    let light1 = Light {
        position: vector::Vector {
            x: 0.0,
            y: 1.0,
            z: 15.0,
        },
        color: Rgb([255, 0, 0]),
    };

    let light2 = Light {
        position: vector::Vector {
            x: 1.0,
            y: 12.0,
            z: 11.0,
        },
        color: Rgb([0, 255, 0 ]),
    };

    let sphere1 = Object {
        obj_type: ObjectType::SphereType(Sphere {
            position: vector::Vector {
                x: 3.0,
                y: 1.0,
                z: 0.0,
            },
            radius: 0.5,
        }),
        reflectivity: 0.0,
    };

    let plane1 = Object {
        obj_type: ObjectType::PlaneType(Plane {
            position: vector::Vector {
                x: 10.0,
                y: 1.0,
                z: 0.0,
            },
            normal: vector::Vector {
                x: 1.0,
                y: 0.0,
                z: 0.0,
            },
        }),
        reflectivity: 0.0,
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

            let mut color = vector::Vector {
                x: 255.0,
                y: 255.0,
                z: 255.0,
            };

            let mut closest_intersection: Option<vector::Vector> = None;

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

                        // Setting up the ray of light that we want to check intersections for.
                        let light_ray = Ray {
                            position: ci.clone(),
                            direction: (ci - &light.position).normalize(),
                        };

                        // Iterate through each object to see if the ray intersects
                        for object in objects.iter() {
                            let light_color = vector::Vector {
                                x: light.color[0] as f32,
                                y: light.color[1] as f32,
                                z: light.color[2] as f32,
                            };

                            let intersected = CheckIntersection(object, &light_ray);
                            let mut should_color = false;
                            match &intersected {
                                None => should_color = true,
                                Some(i_point) => {
                                    if (i_point - &light_ray.position).len().powf(2.0) < 0.0001 {
                                        should_color = true;
                                    }
                                },
                            }
                            
                            let mut shade = 0.0; 

                            if should_color {
                                let normal_vec = GetNormalVector(&object, &ci);


                                let n_vec = normal_vec.dot(&light_ray.direction);
                                shade = if n_vec > 0.0 {0.0} else {-n_vec}; 


                            }
                            color = &color - &(light_color * (ambient_coefficient + (1.0 - ambient_coefficient) * shade));


                        }
                    }
                }
                None => color = vector::Vector {
                    x: 255.0,
                    y: 255.0,
                    z: 255.0,
                },
            }

            let rgb_color = Rgb([min(color.x as u8, 255), min(color.y as u8, 255), min(color.z as u8, 255)]);
            image_data.put_pixel(x, y, rgb_color);
        }
    }

    image_data.save("here.png").unwrap();
}
