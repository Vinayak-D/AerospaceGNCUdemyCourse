#Assignment 3 - The System Model Framework (completed)

import numpy as np
import control as ct
import matplotlib.pyplot as plt

class System:
    def __init__(self):
        
        #Default dimensions
        self.n = 0
        self.m = 0
        self.p = 0
        
        #Default state models (continuous and discrete)
        self.Ac = 1
        self.A = 1
        self.Bc = 1
        self.B = 1
        self.C = 1
        self.D = 1
        self.XO = 1
        self.Xlogged = 0
        self.Ulogged = 0
        
        #Default Initial Conditions
        self.U = 1
        self.R_set = 1
        #self.model = 1
        self.E = 1
        self.Ypr = 1
        
        #Default Sampling time and states
        self.dT = 0
        self.X = 1
        self.Y = 1
        
        #MPC Parameters
        #self.MPCType = 0
        self.Q = 0
        self.R = 0    
        self.f = 0
        
    #Methods to update the system           
    def updateContinuousStateModel(self,A,B,C,XO):
        self.Ac = A
        self.Bc = B
        self.C = C
        self.D = np.zeros((np.shape(self.C)[0],np.shape(self.Bc)[1]))
        self.XO = XO
        self.n = A.shape[0]
        self.m = B.shape[1]
        self.p = C.shape[0]
        self.X = np.zeros(self.n)
        
    def updateInitialConditions(self,U):
        self.U = U
        self.model = ct.ss(self.Ac,self.Bc,self.C,self.D)
        self.E = np.zeros(self.p)
        self.Ypr = np.zeros(self.p)

    def discretize(self,dT):
        self.dT = dT
        __cont = ct.ss(self.Ac,self.Bc,self.C,self.D)
        __disc = __cont.sample(dT,method = 'zoh')
        (self.A,self.B,self.C,self.D) = ct.ssdata(__disc)

    def stepsim(self):
        self.X = np.asarray(self.A @ np.reshape(self.X,(self.n,1)) + self.B @ np.reshape(self.U,(self.m,1)))
        self.Y = self.C @ np.reshape(self.X,(self.n,1))
        
    #Methods to update constraints, and MPC type
    def updateMPCParameters(self,Q,R):
        self.Q = Q
        self.R = R
        
    #Prepare logged states array
    def prepareLogger(self,length):
        self.Xlogged = np.zeros([self.n,length])
        self.Ulogged = np.zeros([2*self.m,length])
        
    #Log all states for plotting
    def logStatesAndInputs(self,idx,dU):
        for i in range(self.n):
            self.Xlogged[i][idx] = self.X[i].item() + self.XO[i].item()
        for i in range(self.m):
            self.Ulogged[i][idx] = self.U[i].item()
            self.Ulogged[i+self.m][idx] = dU[i].item()    

    #The setpoint calculator for Assignment 4
    def Setpoint_Assignment4(self,k,k_f,p):
        #How much to increment height
        d_hD = 108
        d_vD = 54
        #empty preallocation 
        R_bar = np.zeros([p, int(k_f)])
        while(k<k_f):
            if (k>=k_f/1.5):
                R_bar[0,k] = - d_hD
                R_bar[1,k] = - d_vD
            elif (k>=k_f/4):
                #setpoints are CHANGE in value
                R_bar[0,k] = 0 + d_hD*2
                R_bar[1,k] = 0 + d_vD*2
            elif (k>=k_f/6):
                R_bar[0,k] = 0 + d_hD/-1.25
                R_bar[1,k] = 0 + d_vD/-1.25
            elif (k>=k_f/10):
                R_bar[0,k] = 0 + d_hD/3 
                R_bar[1,k] = 0 + d_vD/3
            else:
                R_bar[0,k] = 0
                R_bar[1,k] = 0
            k+=1
        return R_bar        
        
    #Plot all results
    def plotResults(self, TIME, Rbar0, Rbar1):
        plt.figure()
        plt.subplot(3,2,1)
        height = self.Xlogged[0,:]
        plt.plot(TIME, height[1:len(TIME) + 1], linewidth=1.75)
        plt.plot(TIME, self.XO[0] + Rbar0[1:len(TIME) + 1],'k--',label='$\Delta h_{des}$', linewidth=1)
        plt.ticklabel_format(useOffset=False)
        plt.legend()
        plt.ylabel('$\Delta h$ (m)')
        plt.tight_layout(pad=2.0,h_pad=None, w_pad=None)

        plt.subplot(3,2,2)
        speed = self.Xlogged[2,:]
        plt.plot(TIME, speed[1:len(TIME) + 1], linewidth=1.75)
        plt.ticklabel_format(useOffset=False)
        plt.ylabel('$\Delta v$ (m/s)')
        plt.tight_layout(pad=2.0,h_pad=None, w_pad=None)

        plt.subplot(3,2,3)
        thrust = self.Ulogged[0,:]
        plt.plot(TIME, thrust[1:len(TIME)+1],label='$\delta t$')
        plt.axhline(max(thrust),color='k',linestyle='dashed')
        plt.axhline(min(thrust),color='k',linestyle='dashed')
        plt.ylabel('$\delta t$')
        plt.xlabel('Time (s) ')
        plt.tight_layout()

        plt.subplot(3,2,4)
        elevator = self.Ulogged[1,:]
        plt.plot(TIME, elevator[1:len(TIME)+1],label='$\delta e$')
        plt.axhline(max(elevator),color='k',linestyle='dashed')
        plt.axhline(min(elevator),color='k',linestyle='dashed')
        plt.xlabel('Time (s)')
        plt.ylabel('$\delta e (rad)$')
        plt.tight_layout()

        plt.subplot(3,2,5)
        del_thrust = self.Ulogged[2,:]
        plt.plot(TIME, del_thrust[1:len(TIME)+1],label='$\Delta(\delta t$)')
        plt.axhline(max(del_thrust),color='k',linestyle='dashed')
        plt.axhline(min(del_thrust),color='k',linestyle='dashed')
        plt.xlabel('Time (s)')
        plt.ylabel('$\Delta(\delta t)$')
        plt.tight_layout()

        plt.subplot(3,2,6)
        del_elevator = self.Ulogged[3,:]
        plt.plot(TIME, del_elevator[1:len(TIME)+1],label='$\Delta(\delta e)$')
        plt.axhline(max(del_elevator),color='k',linestyle='dashed')
        plt.axhline(min(del_elevator),color='k',linestyle='dashed')
        plt.xlabel('Time (s)')
        plt.ylabel('$\Delta(\delta e (rad))$')
        plt.tight_layout()
    