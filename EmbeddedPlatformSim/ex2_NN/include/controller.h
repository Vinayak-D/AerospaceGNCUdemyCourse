#ifndef CONTROLLER_H
#define CONTROLLER_H
#include "math.h"
#include "neuralMath.h"

class Controller{
    public:
        Controller();
        void updateReading(const float val);
        void calculateInput();
        void updateSetpoint(const float& val);
        void updateError();
        float& returnInput();
        void setLimits(const float lower, const float upper);
        float returnSetpoint();
        void performInference();
  
    private:
        float _calculatedInput;
        float _error;
        float _prev_error;
        float _reading;
        float _setpoint;
        float _sat_lower;
        float _sat_upper;
        float weights_1[5][2]{{2.3471, 0.1698}, {-2.3217, 1.8525}, {-0.2723, 0.1896}, {2.2098, -0.0192}, {-0.0628,  0.1871}};
        float bias_1[5][1]{{0.6904}, {-0.1043}, {-0.6755}, {-0.3744}, {-0.2915}};
        float weights_2[5][5]{{1.5146,  2.6609,  0.2683, -1.6473, -0.1947},
                              {0.5825,  0.0684, -0.0920,  1.5807, -0.0721},
                              {0.4981, -0.2335, -0.4149,  1.3201, -0.1132},
                              {-1.5919,  2.9905, -0.2899, -0.2059, -0.3124},
                              {-0.4188, -0.2611,  0.3844,  0.1996,  0.2168}};
        float bias_2[5][1]{{0.0006061}, {0.17643}, {1.26308}, {0.55131}, {-0.32314}};
        float weights_3[1][5]{-2.7409, 0.8454, 0.8959, -2.7602, -0.0161};
        float bias_3[1]{0.60661};
  };


#endif