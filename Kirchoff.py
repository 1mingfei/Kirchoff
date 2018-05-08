#!/usr/bin/python
import numpy as np


class Kirchoff(object):
    #get initial Neighbour list:
    def initial_NB_list_1D(self):
        Dmn=2 #dimension of 1D NNB list(left/right)
        self.NB=np.zeros((self.N,Dmn))
        #treat BC
        self.NB[N-1][0]=(self.N-1-1)
        self.NB[N-1][1]=(0)
        for i in range(1,self.N-1): #leave 0 and N as BC
            self.NB[i][0]=(i-1)
            self.NB[i][1]=(i+1)
        return
    def initial_NB_list_2D(self):
        return
    
    #update Voltage on node i:
    def update_Vi_1D(self,i):
        num=0.0
        denom=0.0
        if i==(self.N-1):
            return(self.V[i-1])
        else:
            for k in range(len(self.NB[i])):
                j=int(self.NB[i][k])
                num+=self.g[i][j]*self.V[j]
                denom+=self.g[i][j]
            return(num/denom)
    
    #get initial g_ij (conductances)
    def initial_sigma(self):
        if self.typ=="uniform":
            sigma=np.ones(N)
        elif self.typ=="broken":
            sigma=np.ones(N)
            sigma[N//2]=1e-20
            sigma[N//2+1]=1e-20
        elif self.typ=="fake-GB":
            sigma=np.ones(N)
            sigma[N//2]=1e-2
        return sigma
            
    def initial_g(self):
        for i in range(self.N_flat):
            for j in range(self.N_flat):
                self.g[i][j]=np.sqrt(self.sigma[i]*self.sigma[j])
        return
    #get initial Voltage on each node:
    def initial_V_1D(self):
        self.V[0]=self.V_A
        return
    
    def iteration_1D(self):
        for ep in range(self.max_epoch):
            for i in range(1,self.N):
                self.V[i]=self.update_Vi_1D(i)
            print(self.V)
        return

            



    def __init__(self,D,N,typ,V_A,max_epoch):
        self.D=D
        self.N=N
        self.typ=typ
        self.V_A=V_A
        self.max_epoch=max_epoch
        self.sigma=self.initial_sigma()
        self.N_flat=self.N
        self.g=np.zeros((self.N_flat,self.N_flat))
        if self.D==1:
            self.V=np.zeros(self.N)
            self.initial_V_1D()

            self.initial_NB_list_1D()
            self.initial_g()
            print(self.sigma)
            print(self.g)
            self.iteration_1D()
        elif self.D==2:
            self.N_flat=self.N #this line need to be changed for 2D case
            self.V=np.zeros((self.N_flat,self.N_flat))
            self.initial_V_2D()

            self.initial_NB_list_2D()
            self.initial_g()

        print(self.V)
        return

#define mesh density
N=5
#define Voltage on one lhs
V_A=100.0
#define maximum iterations
max_epoch=20

#test_1D=Kirchoff(1,N,'broken',V_A,max_epoch) #"broken","uniform"
#test_1D=Kirchoff(1,N,'uniform',V_A,max_epoch) #"broken","uniform"
test_1D=Kirchoff(1,N,'fake-GB',V_A,max_epoch) #"fake-GB"
