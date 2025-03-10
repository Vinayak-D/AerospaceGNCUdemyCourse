#include "controller.h"

Controller::Controller():_calculatedInput(0), _error(0), _prev_error(0), _reading(0){
    //initialize setpoint
    _setpoint = 0;
    _sat_lower = -100;
    _sat_upper = 100;
  }

void Controller::updateReading(const float val){
    _reading = val;
}

void Controller::performInference(){
    //input
    float _input[2][1]{{_error}, {_prev_error}};
    //forward propagation to layer 1
    float _layer1[5][1];
    NXM_Matmul(_layer1, weights_1, _input);
    //apply bias
    NX1_Add(_layer1, _layer1, bias_1);
    //ReLU activation
    applyReLU(_layer1);
    //forward propagation to layer 2
    float _layer2[5][1];
    NXM_Matmul(_layer2, weights_2, _layer1);
    //apply bias
    NX1_Add(_layer2, _layer2, bias_2);
    //ReLU activation
    applyReLU(_layer2);
    //forward propagation to output (no activation)
    float _output[1][1];
    NXM_Matmul(_output, weights_3, _layer2);
    //apply bias
    _output[0][0] += bias_3[0];
    _calculatedInput = _output[0][0];
}

void Controller::calculateInput(){
    performInference();
    //update previous error
    _prev_error = _error;
    //saturation check
    _calculatedInput = (_calculatedInput > _sat_upper) ? _sat_upper : _calculatedInput;
    _calculatedInput = (_calculatedInput < _sat_lower) ? _sat_lower : _calculatedInput;
}

void Controller::updateSetpoint(const float& val){
    _setpoint = val;
}

float Controller::returnSetpoint(){
    return _setpoint;
  }

void Controller::updateError(){
    _error = _setpoint - _reading;
}

float& Controller::returnInput(){
    return _calculatedInput;
}

void Controller::setLimits(const float lower, const float upper){
    _sat_lower = lower;
    _sat_upper = upper;
}
