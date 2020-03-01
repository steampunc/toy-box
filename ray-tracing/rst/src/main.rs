mod vector;
mod camera;
mod image;
mod object;

use vector::{Vector, Ray};
use object::{Object, ObjectType, Sphere};

fn main() {

    let camera = camera::Camera {
        ul_position: Vector {
            x:1.0,
            y:1.0,
            z:0.5,
        },
        normal_vector: Vector {
            x:1.0,
            y:0.0,
            z:0.0,
        }.normalize(),
        screen_dimensions: (2.0, 1.0),
        emitter_distance: 1.0,    
        rotation: 0.0,
        resolution: 150.0,
    };

    let sphere = Object {
        obj_type: ObjectType::SphereType(Sphere {
            position: vector::Vector {
                x: 3.0,
                y: 0.0,
                z: 0.0,
            },
            radius: 0.5,
        }),
        reflectivity: 0.0,
    };

    let floor = Object {
        obj_type: ObjectType::SphereType(Sphere {
            position: vector::Vector {
                x: 3.0,
                y: 0.0,
                z: -100.0,
            },
            radius: 99.5,
        }),
        reflectivity: 0.0,
    };

    let objects: [Object; 2] = [sphere, floor];

    let (width, height) = camera.get_x_y_pixels();
    let mut image = image::PPM::new(height, width);

    for x in 0..width {
        for y in 0..height {
            let color = camera.trace(x, y, &objects);
            image.set_pixel(x, y, color);
        }
    }

        
    image.write_file("text_img.ppm");


	// Wanr to make a better camera.
	// screen position, screen dimensions, emitter distance, resolution (conversion from float to
	// integer camera resolution)
	//
    // Ways to preserve aspect ratio - i.e. place constraint on dimensions and it creates an image
    // object that 
    
}

