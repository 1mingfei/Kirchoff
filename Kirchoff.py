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
        #leave 0 and N as BC
        for i in range(1,self.N-1): 
            self.NB[i][0]=(i-1)
            self.NB[i][1]=(i+1)
        return
    def initial_NB_list_2D_PBC(self):
        Dmn=4 #dimension of 1D NNB list(left/right)
        self.NB=np.zeros((self.N**2,Dmn))
        #treat row BC j=0 and j=N:
        j=0 #j is col 
        for i in range(self.N): #i is row
            if i==0: row_u=(self.N-1)
            else:
                row_u=i-1 
            if i==(self.N-1): row_d=0
            else:
                row_d=i+1
            self.NB[i*self.N+j][0]=0
            self.NB[i*self.N+j][1]=(i*self.N+j+1)
            self.NB[i*self.N+j][2]=((row_u)*self.N+j)
            self.NB[i*self.N+j][3]=((row_d)*self.N+j)
        j=(self.N-1)
        for i in range(self.N): #i is row
            if i==0: row_u=(self.N-1)
            else:
                row_u=i-1 
            if i==(self.N-1): row_d=0
            else:
                row_d=i+1
            self.NB[i*self.N+j][0]=(i*self.N+j-1)
            self.NB[i*self.N+j][1]=0
            self.NB[i*self.N+j][2]=((row_u)*self.N+j)
            self.NB[i*self.N+j][3]=((row_d)*self.N+j)

        #BC: perodic along col; not perodic along row
        for i in range(self.N):  # i is row
            if i==0: row_u=(self.N-1)
            else:
                row_u=i-1 
            if i==(self.N-1): row_d=0
            else:
                row_d=i+1
            for j in range(1,self.N-1):    # j is col
                self.NB[i*self.N+j][0]=(i*self.N+j-1)   #left
                self.NB[i*self.N+j][1]=(i*self.N+j+1)   #right
                self.NB[i*self.N+j][2]=((row_u)*self.N+j) #top
                self.NB[i*self.N+j][3]=((row_d)*self.N+j) #bot
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
    def update_Vi_2D(self,i):
        num=0.0
        denom=0.0
        if (i%(self.N)+1)==self.N:  #skip 2nd NB
            j=int(self.NB[i][0])
            num+=self.g[i][j]*self.V_flat[j]
            denom+=self.g[i][j]
            j=int(self.NB[i][2])
            num+=self.g[i][j]*self.V_flat[j]
            denom+=self.g[i][j]
            j=int(self.NB[i][3])
            num+=self.g[i][j]*self.V_flat[j]
            denom+=self.g[i][j]
            return(num/denom)
        else:
            for k in range(len(self.NB[i])):
                j=int(self.NB[i][k])
                num+=self.g[i][j]*self.V_flat[j]
                denom+=self.g[i][j]
            return(num/denom)

    #get initial g_ij (conductances)
    def initial_sigma_1D(self):
        if self.typ=="uniform":
            sigma=np.ones(self.N)
        elif self.typ=="broken":
            sigma=np.ones(self.N)
            sigma[self.N//2]=1e-20
            sigma[self.N//2+1]=1e-20
        elif self.typ=="fake-GB":
            sigma=np.ones(self.N)
            sigma[self.N//2]=1e-2
        return sigma

    def initial_sigma_2D(self):
        sigma=np.ones(self.N**2)
        if self.typ=="uniform":
            pass
        elif self.typ=="defects": #25% random defects
            rd_lst=np.arange((self.N-1)**2)
            np.random.shuffle(rd_lst)
            print(rd_lst)
            for i in rd_lst[:50]:
                sigma[i]=1e-10
        elif self.typ=="broken":
            for i in range(self.N):    # i is row
                sigma[i*self.N+self.N//2-1]  = 1e-2    
                sigma[i*self.N+self.N//2]    = 1e-3    
                sigma[i*self.N+self.N//2+1]  = 1e-2    
        return sigma
            
    def initial_g_1D(self):
        for i in range(self.N):
            for j in range(self.N):
                self.g[i][j]=np.sqrt(self.sigma[i]*self.sigma[j])
        return
            
    def initial_g_2D(self):
        for i in range(self.N**2):
            for j in range(self.N**2):
                self.g[i][j]=np.sqrt(self.sigma[i]*self.sigma[j])
        return

    #get initial Voltage on each node:
    def initial_V_1D(self):
        self.V[0]=self.V_A
        return

    def initial_V_2D(self):
        self.V_flat=self.V.flatten('C')
        for i in range(self.N):
            self.V_flat[i*self.N+0]=self.V_A
        return
   
    #iterative steps
    def iteration_1D(self):
        for ep in range(self.max_epoch):
            for i in range(1,self.N):
                self.V[i]=self.update_Vi_1D(i)
            print("step %2d"%(ep))
            print(self.V)
        return

    def iteration_2D(self):
        for ep in range(self.max_epoch):
            for i in range(1,self.N**2):
                self.V_flat[i]=self.update_Vi_2D(i)
            ##print("step %2d"%(ep))
            ###print(self.V_flat)
            ##self.flat_to_V_2D()
            ##print(self.V)
            ##print(np.mean(self.V[:,-1]))
        return

    def flat_to_V_2D(self):
        self.V=self.V_flat.reshape(self.N,self.N)
        return


 

    def __init__(self,D,N,typ,V_A,max_epoch):
        self.D=D
        self.N=N
        self.typ=typ
        self.V_A=V_A
        self.max_epoch=max_epoch
        if self.D==1:
            self.sigma=self.initial_sigma_1D()
            self.V=np.zeros(self.N)
            self.initial_V_1D()
            self.initial_NB_list_1D()
            self.g=np.zeros((self.N,self.N))
            self.initial_g_1D()
            self.iteration_1D()
        elif self.D==2:
            self.sigma=self.initial_sigma_2D()
            self.V=np.zeros((self.N,self.N))
            self.initial_V_2D()
            #print(self.V_flat)
            self.initial_NB_list_2D_PBC()
            #print(self.NB)
            self.g=np.zeros((self.N**2,self.N**2))
            self.initial_g_2D()
            self.iteration_2D()
            self.flat_to_V_2D()
        print("final Voltage")
        print(self.V)
        print(np.mean(self.V[:,-1]))
        return

#define mesh density
N=50
#define Voltage on one lhs
V_A=100.0
#define maximum iterations
max_epoch=1000

#test_1D=Kirchoff(1,N,'broken',V_A,max_epoch) #1D:"broken","uniform","fake-GB"
#test_1D=Kirchoff(1,N,'uniform',V_A,max_epoch) 
#test_1D=Kirchoff(1,N,'fake-GB',V_A,max_epoch) 
test_2D=Kirchoff(2,N,'uniform',V_A,max_epoch)  #2D:"uniform","broken"
test_2D=Kirchoff(2,N,'broken',V_A,max_epoch) 

