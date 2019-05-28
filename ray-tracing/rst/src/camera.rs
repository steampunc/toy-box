
use crate::vector::{Vector, Ray};


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
        
        println!("X_hat: {:?}, Y_hat: {:?}", x_hat, y_hat);
        (x_hat, y_hat)
    }

    fn get_x_y_pixels(&self) -> (u16, u16) {
        ((&self.screen_dimensions.0 * &self.resolution) as u16,
        (&self.screen_dimensions.1 * &self.resolution) as u16)
    }

    fn get_emitter_position(&self) -> Vector {
        let (x_hat, y_hat) = self.get_x_y_directions();
        &(&self.normal_vector * (-&self.emitter_distance)) + &(&self.ul_position + &(&(x_hat * self.screen_dimensions.0 * 0.5) + &(y_hat * self.screen_dimensions.1 * 0.5)))
    }

    pub fn trace(&self) -> () {

        let (x_hat, y_hat) = self.get_x_y_directions();

        let emitter_pos = self.get_emitter_position();

        let (x_pix_count, y_pix_count) = self.get_x_y_pixels();

        for x in 0..x_pix_count {
            for y in 0..y_pix_count {
                let screen_position = &self.ul_position + &(&(&x_hat * (x as f32 / self.resolution)) + &(&y_hat * (y as f32 / self.resolution)));
                let tracer_ray = Ray {
                    position: emitter_pos.clone(),
                    direction: &screen_position - &emitter_pos,
                }; 
            }
        }
        
        
    
    }
}
