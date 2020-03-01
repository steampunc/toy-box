use crate::vector::{Vector, Ray};
use crate::image::RGB;
use crate::object;


pub struct Camera {
    pub ul_position: Vector,
    pub normal_vector: Vector,
    pub screen_dimensions: (f32, f32),
    pub resolution: f32, // number of pixels per unit on the screen
    pub emitter_distance: f32,    
    pub rotation: f32,

}

impl Camera { 
    fn get_x_y_directions(&self) -> (Vector, Vector) {
        let z_hat = Vector {
            x:0.0,
            y:0.0,
            z:1.0,
        };
        let ur_y_hat = &z_hat - &(&self.normal_vector * (z_hat.dot(&self.normal_vector)));
        let y_hat = (&(&ur_y_hat * -self.rotation.cos()) + &(self.normal_vector.cross(&ur_y_hat).normalize() * -self.rotation.sin())).normalize();
        let x_hat = y_hat.cross(&self.normal_vector).normalize(); 
        
        (x_hat, y_hat)
    }

    pub fn get_x_y_pixels(&self) -> (u32, u32) {
        ((&self.screen_dimensions.0 * &self.resolution) as u32,
        (&self.screen_dimensions.1 * &self.resolution) as u32)
    }

    fn get_emitter_position(&self) -> Vector {
        let (x_hat, y_hat) = self.get_x_y_directions();
        &(&self.normal_vector * (-&self.emitter_distance)) + &(&self.ul_position + &(&(x_hat * self.screen_dimensions.0 * 0.5) + &(y_hat * self.screen_dimensions.1 * 0.5)))
    }

    pub fn trace(&self, x: u32, y: u32, objects: &[object::Object]) -> RGB {

        let (x_hat, y_hat) = self.get_x_y_directions();

        let emitter_pos = self.get_emitter_position();

        dbg!(&x);
        dbg!(&y);
        let screen_position = &self.ul_position + &(&(&x_hat * (x as f32 / self.resolution)) + &(&y_hat * (y as f32 / self.resolution)));
        let tracer_ray = Ray {
            position: emitter_pos.clone(),
            direction: (&screen_position - &emitter_pos).normalize(),
        }; 

        for object in objects.iter() {
            let intersect = object::CheckIntersection(object, &tracer_ray);
            match intersect {
                Some(color) => { 
                    dbg!(&color);
                    return color;
                },
                None => (),
            }
            
        }

        // For ambient coloring of sky
        let t = 0.5 * (tracer_ray.direction.normalize().z + 1.0);
        RGB {
            r: (((1.0 - t) + t * 0.5) * 255.0) as u8,
            g: (((1.0 - t) + t * 0.7) * 255.0) as u8,
            b: (((1.0 - t) + t * 1.0) * 255.0) as u8,
        }
    }
}
