#ifndef MATRIXMATH_H
#define MATRIXMATH_H
#include <stddef.h>

template <size_t r1, size_t c1>
void NX1_Matmul(float (&result)[r1], float (&matrixOne)[r1][c1], float (&arrayTwo)[c1]){
    for (int i = 0; i < r1; ++i){
        result[i] = 0;
        int count = 0;
        for (int j = 0; j < c1; ++j){
            result[i] += matrixOne[i][j]*arrayTwo[count];
            count+=1;
        }
    }    
}

template <size_t r1>
void NX1_Add(float (&result)[r1], float (&arrayOne)[r1], float (&arrayTwo)[r1]){
    for (int i = 0; i < r1; ++i){
        result[i] = arrayOne[i] + arrayTwo[i];
    }    
}

template <size_t r1>
void NX1_Assign(float (&out)[r1], float (&in)[r1]){
    for (int i = 0; i < r1; ++i){
        out[i] = in[i];
    }    
}

template<size_t r1>
void scaleArray(float (&in)[r1], const float h){
    for (int i = 0; i < r1; ++i){
        in[i] = in[i]*h;
    }
}

#endif //MATRIXMATH_H