#Assignment 3 - The MPC Framework (TODO)
import numpy as np
from scipy import linalg

class MPCDesign:
    def __init__(self, Np, n, m, p):
        #Student section-----------------------------------------------------------------------------------------
        #Assign self.N_p to Np, create zero matrices using n, m, p variables
        #Example: a zero matrix of x,y is np.zeros([x, y])
        self.N_p = 0 #replace '0'
        self.F = 0 #replace '0'
        self.G = 0 #replace '0'
        self.H = 0 #replace '0'
        #End student section-------------------------------------------------------------------------------------
        
class eMPC(MPCDesign):
    def __init__(self, Np, n, m, p):
        super().__init__(Np,n,m,p)
        
    def calculateFGMatrices(self, A, B, C, Np, n):
        [S,D] = linalg.eig(A) #find eigenvalues
        #Eigenvalues for diagonal matrix (np.diag(MID)), n = # of states
        MID = np.zeros(n, dtype=complex) 
        for y in range(n):
            MID[y] = np.exp(S[y]*Np) #exponential
        phi = D @ np.diag(MID) @ linalg.inv(D) #get inverse of D, create diagonal matrix from vector MID
        F = np.real(C @ phi)
        G = np.real(C @ linalg.inv(A) @ (phi-np.identity(n)) @ B)   
        return F, G
    
    def calculateGain(self, Q, R):
        #Student section-----------------------------------------------------------------------------------------
        self.H = 0 #replace '0' , use X.transpose() to transpose a matrix X
        self.Hinv = 0 #replace '0'
        self.K_eMPC = 0 #replace '0', what is the formula for the optimal gain?
        #End student section-------------------------------------------------------------------------------------
    
    def setConstraints(self,M_con,g_con):
        self.M_con = M_con
        self.g_con = g_con     
        
    def assignFGMatrices(self, F, G):
        self.F = F
        self.G = G
    
    def constraintsSatisfied(self, U, M, g):
        result = True
        #Student section-----------------------------------------------------------------------------------------
        LHS = M @ U
        for i in range (0): #replace '0', how much should i iterate, hint: length of vector is len(vector)
            if (True): #replace, what should the condition be - to find out if constraint is not satisfied
                result = 0 #replace with.......
                break
        return result
        #End student section-------------------------------------------------------------------------------------