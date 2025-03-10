#include "controller.h"

Controller::Controller():h(0.005), _calculatedInput(0), _error(0), _prev_error(0), _reading(0), _tot_error(0), initTrigger(true){
    _setpoint = 0;
    KP = 1;
    KI = 0;
    KD = 0;
    _sat_lower = -1000;
    _sat_upper = 1000;
}

void Controller::updateReading(const float& val){
    _reading = val;  
}

void Controller::calculateInput(){
    //de/dt
    float error_derivative = (initTrigger) ? 0.0 : (_error - _prev_error)/h; 
    initTrigger = false;
    //integral
    _tot_error += _error*h;      
    //update previous error
    _prev_error = _error;
    //PID controller
    _calculatedInput = KP*_error + KI*_tot_error + KD*error_derivative;    
    //saturation check
    _calculatedInput = (_calculatedInput > _sat_upper) ? _sat_upper : _calculatedInput;
    _calculatedInput = (_calculatedInput < _sat_lower) ? _sat_lower : _calculatedInput;
}

void Controller::updateSetpoint(const float& val){
    _setpoint = val;
}

void Controller::updateSetpoint(const float& dist, const float& height){
    _setpoint = atan(height/dist);
}

void Controller::updateError(){
    _error = _setpoint - _reading;
}

float& Controller::returnInput(){
    return _calculatedInput;
}

void Controller::setPIDParameters(const float _kp, const float _ki, const float _kd){
    KP = _kp;
    KI = _ki;
    KD = _kd;
}

void Controller::setLimits(const float lower, const float upper){
    _sat_lower = lower;
    _sat_upper = upper;
}

void Controller::overrideError(){
    _error = 0.0;
}
