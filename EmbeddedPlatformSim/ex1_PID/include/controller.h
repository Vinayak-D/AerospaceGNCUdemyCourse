#ifndef CONTROLLER_H
#define CONTROLLER_H
#include "math.h"

class Controller{
    public:
        Controller();
        void updateReading(const float& val);
        void calculateInput();
        void updateSetpoint(const float& val);
        void updateSetpoint(const float& dist, const float& height);
        void updateError();
        float& returnInput();
        void setPIDParameters(const float _kp, const float _ki, const float _kd);
        void setLimits(const float lower, const float upper);
        void overrideError();

    private:
        const float h;
        float _calculatedInput;
        float _error;
        float _prev_error;
        float _reading;
        float _tot_error;
        float _setpoint;
        float KP;
        float KI;
        float KD;
        float _sat_lower;
        float _sat_upper;
        bool initTrigger;
};


#endif