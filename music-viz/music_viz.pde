import processing.sound.*;
import processing.serial.*;

AudioIn mic;
Serial serial;
Amplitude amp;

int pageSize = 800;
int fr = 15;

float time = 0;
float tempo = 80.0;
float time_sig = 4; //Beats per measure
float rpm = 1 * TWO_PI; // radians per 
float fpm = fr * 60;

float angular_velocity = (tempo / time_sig) * (rpm / fpm);

SoundFile soundfile;

void setup(){
  mic = new AudioIn(this, 0);
  mic.start();
  frameRate(fr);
  
  serial = new Serial(this, "/dev/ttyUSB0", 9600);
  serial.write("IN;SP1;PA4150,3825;PD;");
  
  
  amp = new Amplitude(this);
  
  ellipseMode(CENTER);
  size(700, 700);
  background(255);
 
  soundfile = new SoundFile(this, "m80.mp3");
  
  delay(500);
  
  
  amp.input(soundfile);
  
  soundfile.play();
}

void draw() {
  
  time += 1.0;
  
  float micLevel = amp.analyze();
  
  print(micLevel);
  float theta = angular_velocity * time;
  float radius = 10 + map(micLevel, 0.0, 1.0, 10, float(pageSize));
  int x = int(radius * cos(theta)) + 5150;
  int y = int(radius * sin(theta)) + 3825;
  serial.write("PA" + x + "," + y + ";");
  
  
  
  ellipse(x, y, 2, 2);
}
