#include "controller.h"
#include <Arduino.h>

Controller ctrl;
float reading = 0.0;
float i;
float _setpt;

void setup() {
    //Set controller parameters
    ctrl.setLimits(-1.57, 1.57);
    //Set initial count
    i = 0;
    // Start serial communication with system
    Serial.begin(9600);  
}

void loop() {

    // Check if data is available to read from system
    if (Serial.available() > 0) {

        _setpt = i*0.0005 + 0.5;
        _setpt = (_setpt > 1.25) ? 1.25 : _setpt;

        ctrl.updateSetpoint(_setpt);

        reading = Serial.parseFloat();   
        ctrl.updateReading(reading);
        ctrl.updateError();
        // Controller
        ctrl.calculateInput();            
        Serial.print("U_CMD,");
        Serial.println(ctrl.returnInput(), 7); 

        i++;
    }
}