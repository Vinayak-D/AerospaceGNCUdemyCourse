#ifndef NEURALMATH_H
#define NEURALMATH_H
#include <stddef.h>

template <size_t r1, size_t c1>
void NX1_Matmul(float (&result)[r1], float (&matrixOne)[r1][c1], float (&arrayTwo)[c1]){
    for (size_t i = 0; i < r1; ++i){
        result[i] = 0;
        size_t count = 0;
        for (size_t j = 0; j < c1; ++j){
            result[i] += matrixOne[i][j]*arrayTwo[count];
            count+=1;
        }
    }    
}

template<size_t a1, size_t b1, size_t c1>
void NXM_Matmul(float (&result)[a1][c1], float (&matrixOne)[a1][b1], float (&matrixTwo)[b1][c1]){
    for (size_t i = 0; i < a1; i++) {
        for (size_t j = 0; j < c1; j++) {
            result[i][j] = 0;
            for (size_t k = 0; k < b1; k++) {
                result[i][j] += matrixOne[i][k] * matrixTwo[k][j];
            }
        }
    }  
}

template <size_t r1>
void NX1_Add(float (&result)[r1], float (&arrayOne)[r1], float (&arrayTwo)[r1]){
    for (size_t i = 0; i < r1; ++i){
        result[i] = arrayOne[i] + arrayTwo[i];
    }    
}

template <size_t r1>
void NX1_Add(float (&result)[r1][1], float (&arrayOne)[r1][1], float (&arrayTwo)[r1][1]){
    for (size_t i = 0; i < r1; ++i){
        result[i][0] = arrayOne[i][0] + arrayTwo[i][0];
    }    
}

template <size_t r1>
void NX1_Assign(float (&out)[r1], float (&in)[r1]){
    for (size_t i = 0; i < r1; ++i){
        out[i] = in[i];
    }    
}

template<size_t r1>
void scaleArray(float (&in)[r1], const float h){
    for (size_t i = 0; i < r1; ++i){
        in[i] = in[i]*h;
    }
}

template<size_t r1>
void applyReLU(float (&in)[r1][1]){
    for (size_t i = 0; i < r1; ++i) {
        in[i][0] = (in[i][0] <= 0) ? 0 : in[i][0];  
    }
}

#endif //MATRIXMATH_H