#Assignment 4 - Longitudinal Control (TODO)

from assignment3_mpc import eMPC
from assignment2_quadprog import PQP
from assignment3_system import System
from conversions import ned2lla
import numpy as np
d2r = np.deg2rad
import copy
from flightgear_python.fg_if import FDMConnection
import time

#-------------------------FlightGear Callback-------------------------#
i = 0
def fdm_callback(fdm_data, event_pipe):
    global i
    global latValues, lonValues, altValues, thetaValues, elevatorValies, alphaValues, psi, thetadotValues
    #position and orientation
    fdm_data.lat_rad = latValues[i]
    fdm_data.lon_rad = lonValues[i]
    fdm_data.alt_m = altValues[i]
    fdm_data.phi_rad = 0
    fdm_data.theta_rad = thetaValues[i]
    fdm_data.psi_rad = psi
    fdm_data.elevator = elevatorValues[i]
    fdm_data.alpha_rad = alphaValues[i]
    fdm_data.thetadot_rad_per_s = thetadotValues[i]
    i += 1
    print(float(i/limit)*100)
    if i >= limit - 1:
        i = 0    
    return fdm_data  # return the whole structure

if __name__ == '__main__':

    #-------------------------System Design-------------------------#
    system = System()
    A_c = np.array([[0, 500.0000, 0, -500.0000, 0, 0, 0],
                    [0, 0, 0, 0, 1, 0, 0],
                    [0.0001, -32.1700, -0.0130, -2.9483, -1.0283, 0.0016, 0.1018],
                    [0, 0, -0.0003, -0.7506, 0.9281, -0.0000, -0.0016],
                    [0, 0, 0, -1.8365, -1.0271, 0, -0.1335],
                    [0, 0, 0, 0, 0, -1, 0],
                    [0, 0, 0, 0, 0, 0, -20.2]])
    B_c = np.array([[0,0],
                    [0,0],
                    [0,0],
                    [0,0],
                    [0,0],
                    [1,0],
                    [0,20.2]])
    C_c = np.array([[1, 0, 0, 0, 0, 0, 0],
                    [0, 1, 0, 0, 0, 0, 0],
                    [0, 0, -7, 0, 0, 0, 0],
                    [0, 0, 0, 1, 0, 0, 0],
                    [0, 0, 0, 0, 1, 0, 0]])
    C_1 = C_c[:2]
    C_2 = C_c[2:]
    XO = np.array([10000, 0.0638, 500, 0.0638, 0, 0.06, -0.0393])
    system.updateContinuousStateModel(A_c,B_c,C_c,XO)
    
    #Time Setting
    dT = 0.01
    system.discretize(dT)
    U = np.zeros(system.m)
    system.updateInitialConditions(U)
    
    #Design parameters for MPC
    Q = np.diag([1,1,49,1,1]) 
    R = np.diag([20,50])
    system.updateMPCParameters(Q, R)
    
    #-------------------------Controller Design-------------------------#
    N_p = [3.5, 3.5]
    controller = eMPC(N_p, system.n, system.m, system.p)
    
    #The F,G matrices (for C_1 - use Np1 horizon) 
    F_1,G_1 = controller.calculateFGMatrices(system.Ac, system.Bc, C_1, N_p[0], system.n)
    #The F,G matrices (for C_2 - use Np2 horizon)
    F_2,G_2 = controller.calculateFGMatrices(system.Ac, system.Bc, C_2, N_p[1], system.n)
    F = np.asarray(np.concatenate((F_1, F_2)))
    G = np.asarray(np.concatenate((G_1, G_2)))
    controller.assignFGMatrices(F, G)
    
    #Student Section--------------------------------------------------------------------------------

    #Constraints
    Mconstraints = 0 #complete
    gconstraints = 0 #complete
    #call controller set constraints method and pass M, g appropriately (uncommand / fix next line)
    #controller..

    #calculate optimal feedback gain (uncomment / fix next line) - pass in appropriate arguments
    #controller...

    #End student section-----------------------------------------------------------------------------
    
    
    #-------------------------Time Settings-------------------------#
    
    k = 0   
    Time = 60
    k_f = int(Time/dT)
    dk_1 = int(N_p[0]/dT)
    dk_2 = int(N_p[1]/dT)
    limit = int(k_f-max(dk_1,dk_2))
    
    system.prepareLogger(k_f)
    
    #Setpoint
    R_bar = system.Setpoint_Assignment4(k, k_f, system.p)
    
    #Values to pass to FlightGear callback
    lat0_target = d2r(34.44417) 
    lon0_target = d2r(126.44125)
    alt0 = 7
    psi = d2r(340)
    latValues = [lat0_target]
    lonValues = [lon0_target]
    altValues = [XO[0]]
    thetaValues = [XO[1]]
    alphaValues = [XO[3]]
    thetadotValues = [XO[4]]
    elevatorValues = [XO[6]]
    x = 0
    y = 0
    #------------------System and Controller Simulation-----------------#
    
    for k in range(limit):
        #copy old inputs
        U_old = copy.deepcopy(system.U)
        #one timestep
        system.stepsim()
        #The PREDICTED system Outputs Yp(k) = nx1 
        Y_pred = np.squeeze(controller.F @ system.X) #
        #Calculate the error and find the optimal U
        #error vector E = R - Y, this is future error (at prediction point)
        system.E[0] = R_bar[0][k+dk_1] - Y_pred[0].item()
        system.E[2] = R_bar[1][k+dk_2] - Y_pred[2].item()
        #Unconstrained input
        system.U = controller.K_eMPC @ system.E

        #Student Section--------------------------------------------------------------------------------
        
        #Get constrained input if unconstrained is not satisfactory
        if not controller.constraintsSatisfied(system.U, controller.M_con, controller.g_con):
            system.f = -controller.G.transpose() @ system.Q @ system.E
            qp = 0 #update (initialize PQP class - pass in correct arguments - hint, look at the constructor)
            qp.Optimize()
            #Find constrained input
            system.U = -controller.Hinv @ (system.f + 0.5*controller.M_con.transpose() @ qp.lam)
        
        #End student section-----------------------------------------------------------------------------

        #Log states and inputs
        dU = U_old - system.U
        system.logStatesAndInputs(k, dU)
        
        #Get LLA position, and append other values to pass to FlightGear callback
        curr_speed = system.Xlogged[2,k].item()
        curr_theta = system.Xlogged[1,k].item()
        curr_D = alt0 - system.Xlogged[0,k].item()
        x = x + dT*(curr_speed*np.cos(psi)*np.cos(curr_theta))
        y = y + dT*(curr_speed*np.sin(psi)*np.cos(curr_theta))
        P_LLA = ned2lla(x, y, curr_D, lat0_target, lon0_target, alt0)
        latValues.append(P_LLA[0])
        lonValues.append(P_LLA[1])
        altValues.append(system.Xlogged[0,k].item())
        thetaValues.append(system.Xlogged[1,k].item())
        alphaValues.append(system.Xlogged[3,k].item())
        thetadotValues.append(system.Xlogged[4,k].item())
        elevatorValues.append(system.Ulogged[1,k].item())
    
    #Plot results
    TIME = np.linspace(0,k*dT,k)
    Rbar0 = R_bar[0]
    Rbar1 = R_bar[1]
    system.plotResults(TIME, Rbar0, Rbar1)

    #FG callback
    fdm_conn = FDMConnection(fdm_version=24)  # May need to change version from 24
    fdm_event_pipe = fdm_conn.connect_rx('localhost', 5501, fdm_callback)
    fdm_conn.connect_tx('localhost', 5502)
    fdm_conn.start()# Start the FDM RX/TX loop    
    while(True):
        time.sleep(0.020)






