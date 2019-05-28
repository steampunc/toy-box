mod vector;
mod camera;

use vector::{Vector, Ray};
use image::{ImageBuffer, Rgb};

fn main() {
    
    let camera = camera::Camera {
    ul_position: Vector {
        x:1.0,
        y:1.0,
        z:1.0,
    },
    normal_vector: Vector {
        x:1.0,
        y:0.0,
        z:0.0,
    }.normalize(),
    screen_dimensions: (2.0, 2.0),
    emitter_distance: 1.0,    
    rotation: 0.0,
    resolution: 100.0,

};

    let (width, height) = (100, 100);
    let mut image_data = ImageBuffer::<Rgb<u8>, Vec<u8>>::new(width, height);
    camera.trace();

    // Want to make a better camera.
    // screen position, screen dimensions, emitter distance, resolution (conversion from float to
    // integer camera resolution)
    //
    // Ways to preserve aspect ratio - i.e. place constraint on dimensions and it creates an image
    // object that 
    
}

