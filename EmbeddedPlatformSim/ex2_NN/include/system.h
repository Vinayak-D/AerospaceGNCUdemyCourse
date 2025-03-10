#ifndef SYSTEM_H
#define SYSTEM_H

#include "neuralMath.h"

class System{
    public:
        System();
        void initialize();
        void simStep();
        void updateControllerCommand(const float& val);
        float& returnOutput();

    private:
        float X[3];
        float _prodAX[3];
        float _prodBU[3];
        float _dXdT[3];
        float _Y;
        float U[1];
        float _A[3][3]{{-0.313, 56.7, 0},{-0.0139, -0.426, 0},{0, 56.7, 0}};
        float B[3][1]{{0.232},{0.0203},{0}};
        const float h;

};


#endif