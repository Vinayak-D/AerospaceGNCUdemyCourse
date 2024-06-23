#Assignment 2 - The QP Framework (TODO)

import numpy as np
import copy
import matplotlib.pyplot as plt

class QuadProg:
    def __init__(self,M_con,Hinv,g_con,f):
        self.W = (M_con @ Hinv @ M_con.T)*0.5
        self.Z = np.squeeze(M_con @ Hinv @ f + g_con.transpose())
        self.r = np.shape(self.Z)[0]
        self.i_t = 0
        self.err = np.empty(1)
        self.err[self.i_t] = 1
        self.lam = np.zeros(self.r)
    
    def plotResult(self,U):
        print('\nConstrained Inputs:',U[0],U[1], 'after num iterations:', self.i_t)
        x = list(range(0, self.i_t))
        y = self.err[:-1]     
        plt.plot(x,y)

class PQP(QuadProg):
    def __init__(self,M_con,Hinv,g_con,f):
        super().__init__(M_con,Hinv,g_con,f)
        self.lam = np.ones(self.r)  
        self.Zm = np.maximum(-self.Z,0)
        self.Zp = np.maximum(self.Z,0)
        r_vec = np.maximum(-self.W,0) @ np.zeros(self.r)
        self.Wm = np.maximum(-self.W,0) + np.diag(r_vec)
        self.Wp = np.maximum(self.W,0) + np.diag(r_vec)

    def Optimize(self):
        #Student section - Use Algorithm 5 in previous lecture, to complete--------------------------------------
        while False: #update this condition (hint: latest err)
            old = copy.deepcopy(self.lam)
            for i in range(0): #update this condition
                Km = 0 #replace with Wm x lam (use @ to multiply)
                Kp = 0 #replace with Wp x lam (use @ to multiply)  
                self.lam[i] = self.lam[i]*((self.Zm[i]+Km[i])/(self.Zp[i]+Kp[i]))
            err = np.dot((self.lam-old).T,(self.lam-old)) 
            self.i_t = 0 #increment self.i_t by 1
            self.err = np.append(self.err,err) 
        #End student section---------------------------------------------------------------------------------------