#include "controller.h"
#include <Arduino.h>

#define USETESTSETPOINT 0

Controller ctrl;
float testSetpoint = 0.75;
float downrange = 2000;
float height = -500;
float reading = 0.0;

void setup() {
    //Set controller parameters
    ctrl.setPIDParameters(6,1,3);
    ctrl.setLimits(-1.57, 1.57);
    //Set initial setpoint
    if (USETESTSETPOINT){
        ctrl.updateSetpoint(testSetpoint);
    } else {
        ctrl.updateSetpoint(downrange, height);
    }
    // Start serial communication with system
    Serial.begin(9600);  
}

void loop() {

    // Check if data is available to read from system
    if (Serial.available() > 0) {
        reading = Serial.parseFloat();   
        ctrl.updateReading(reading);
        ctrl.updateError();
        // Controller
        ctrl.calculateInput();            
        Serial.print("U_CMD,");
        Serial.println(ctrl.returnInput(), 7); 
    }
}