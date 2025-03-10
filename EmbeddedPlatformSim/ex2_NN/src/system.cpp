#include "system.h"

System::System():h(0.005){
    initialize();
}

void System::initialize(){
    //States X and inputs U at t = 0
    X[0] = 0;
    X[1] = 0;
    X[2] = 0;
    U[0] = 0.0;
}

void System::simStep(){
    //A*X
    NX1_Matmul(_prodAX, _A, X);
    //B*U
    NX1_Matmul(_prodBU, B, U);
    //dXdT = A*X+BU
    NX1_Add(_dXdT, _prodAX, _prodBU);
    //dXdT = h*dXdT;
    scaleArray(_dXdT, h);
    //X = X + dXdT
    NX1_Add(X, X, _dXdT);
    //Y = X[2]
    _Y = X[2];
}

void System::updateControllerCommand(const float& val){
    U[0] = val;
}

float& System::returnOutput(){
    return _Y;
}


