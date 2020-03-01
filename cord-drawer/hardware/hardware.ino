#include <Stepper.h>

// initialize the stepper library on pins 8 through 11:
Stepper LStepper(200, 4,5,6,7);            
Stepper RStepper(200, 42,44,46,48);            

double board_width = 1.03;
double steps_per_m = 200 / 0.145;

void setup() {
  LStepper.setSpeed(50);
  RStepper.setSpeed(50);  // initialize the serial port:
  Serial.begin(9600);

}



void move(int dl, int dr) {
  int prev_int = -1;
  if (abs(dl) >= abs(dr)) {
    for (int i = 0; i < abs(dl); i++) {
      if (dl > 0) {
        LStepper.step(1);
      } else if (dl < 0) {
        LStepper.step(-1);
      }
    
      if (int(abs(i * dr/dl)) != prev_int) {
        if (dr > 0) {
          RStepper.step(1);        
        } else if (dr < 0) {
          RStepper.step(-1);
        }
        prev_int = int(abs(i * dr/dl));
      }
    }
  } else if (abs(dr) >= abs(dl)) {
   for (int i = 0; i < abs(dr); i++) {
      if (dr > 0) {
        RStepper.step(1);
      } else if (dr < 0) {
        RStepper.step(-1);
      }
    
      if (int(abs(i * dl/dr)) != prev_int) {
        if (dl > 0) {
          LStepper.step(1);        
        } else if (dl < 0) {
          LStepper.step(-1);
        }
        prev_int = int(abs(i * dl/dr));
      }
    }
  }
  Serial.write("A");
}

const byte numChars = 32;
char receivedChars[numChars]; // an array to store the received data

boolean newData = false;
int delta_l = 0;
int delta_r = 0;

int incomingByte = 0;
void loop() {
  recvWithEndMarker();
  if (newData) {
    move(delta_l, delta_r);
    newData = false;
  }
}

void recvWithEndMarker() {
  static byte ndx = 0;
  char endMarker = '\n';
  char rc;
  while (Serial.available() > 0 && newData == false) {
    rc = Serial.read();

    if (rc != endMarker) {
      receivedChars[ndx] = rc;
      ndx++;
      if (ndx >= numChars) {
        ndx = numChars - 1;
      }
    }
    else {
      receivedChars[ndx] = '\0'; // terminate the string
      ndx = 0;
      parseData();
      newData = true;
    }
  }
}

void parseData() {
  // split the data into its parts
  char * strtokIndx; // this is used by strtok() as an index

  strtokIndx = strtok(receivedChars,",");      // get the left length
  delta_l = atoi(strtokIndx);
  
  strtokIndx = strtok(NULL, ","); // Find second length
  delta_r = atoi(strtokIndx);
}


/* Demo
 
 
 if (counter % 400 <= 100) {
 LStepper.step(2);
 RStepper.step(1);
 } else if (counter % 400 <= 200) {
 LStepper.step(2);
 RStepper.step(-1);
 } else if (counter % 400 <= 300) {
 LStepper.step(-2);
 RStepper.step(-1);  
 } else {
 LStepper.step(-2);
 RStepper.step(1);
 }
 counter += 1; */
