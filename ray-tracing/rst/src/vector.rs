
#[derive(Debug, Clone)]
pub struct Vector {
    pub x: f32,
    pub y: f32,
    pub z: f32,
}

#[derive(Debug)]
pub struct Ray {
    pub position: Vector,
    pub direction: Vector,
}

impl Vector {
    pub fn len(&self) -> f32 {
        (self.x * self.x + self.y * self.y + self.z * self.z).sqrt()
    }

    pub fn cross(&self, v: &Vector) -> Vector {
        Vector {
            x: self.y * v.z - self.z * v.y,
            y: self.z * v.x - self.x * v.z,
            z: self.x * v.y - self.y * v.x,
        }
    }

    pub fn normalize(&self) -> Vector {
        self * (1.0 / self.len())
    }

    pub fn dot(&self, v: &Vector) -> f32 {
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
