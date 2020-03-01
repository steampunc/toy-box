
use crate::vector;
use crate::image::RGB;

pub enum ObjectType {
    SphereType(Sphere),
}

pub struct Object {
    pub obj_type: ObjectType,
    pub reflectivity: f32,
    pub diffuse: bool,
}

pub struct Sphere {
    pub position: vector::Vector,
    pub radius: f32,
}

pub fn CheckIntersection(object: &Object, ray: &vector::Ray) -> Option<RGB> {
    match &object.obj_type {
        ObjectType::SphereType(sphere) => {
            let pos = &sphere.position - &ray.position;
            let b = ray.direction.dot(&pos);
            let c = pos.dot(&pos) - sphere.radius.powf(2.0);
            let t = (b * b - c);
            if t > 0.0 {
                let pos_count = (b + t.sqrt());
                if pos_count > 0.0 {
                    let coll_pos = &ray.position + &(&ray.direction * pos_count);  
                    let normal = (&sphere.position - &coll_pos).normalize();
                    return Some(RGB {
                        r: ((-normal.y + 1.0) * 0.5 * 255.0) as u8,
                        g: ((-normal.z + 1.0) * 0.5 * 255.0) as u8,
                        b: ((-normal.x + 1.0) * 0.5 * 255.0) as u8,
                    });
                }
            }
            None
        }
    }
}
