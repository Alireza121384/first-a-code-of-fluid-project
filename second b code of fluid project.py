#properties                                                                     
import math
pi=math.pi
N=1100*pi/30    #rad/s
T=25+273     #K
A_s=(0.15**2)*pi/4    #m^2
A_d=A_s           #m^2
P_in=[520,500,480,470,460,450,420,420,400,380,360,330,310]     #W
P_d=[0.06,0.11,0.18,0.21,0.25,0.25,0.29,0.29,0.32,0.34,0.35,0.36,\
     0.36]        #bar
P_da=[x*100000 for x in P_d]     #Pa
P_s=[-0.08,-0.07,-0.05,-0.04,-0.05,-0.04,-0.03,-0.03,-0.02,-0.02,-0.02,-0.01,\
     -0.01]          #bar         
P_sa=[y*100000 for y in P_s]           #Pa
Q=[254,228,197,177,163,155,129,127,99,75,50,27,2]    #L/min
Q_a=[x/1000/60 for x in Q]      #m^3/s
Torque=[2.1,2,1.9,1.8,1.7,1.7,1.5,1.5,1.4,1.2,1.1,1,0.9]      #N.m
z_s=0      #m
z_d=0      #m
rho=997.05           #Kg/m^3
#result
def P_mec(Torque,N):
    return(Torque*N)      #W
def V_s(Q_a,A_s):
    return(Q_a/A_s)        #m/s
def V_d(Q_a,A_d):
    return(Q_a/A_d)        #m/s
def h_pump(P_da,P_sa,rho,V_d,V_s,z_s,z_d):
    return((((P_da)-(P_sa))/(rho*9.81))+((((V_d)**2)-((V_s)**2))/(2*9.81))\
        +z_d-z_s)         #m
def P_hyd (rho,Q_a,h_pump):
    return(rho*9.81*Q_a*h_pump)       #W
def N_s (N,Q_a,h_pump):
    return(N*(Q_a**0.5)/(h_pump**0.75))   #rad/s
def eta_T (P_hyd,P_in):
    return(P_hyd/P_in)
def eta_hyd (P_hyd,P_mec):
    return(P_hyd/P_mec)
print (f"Q (L/min) | Q (m^3/s) | h_pump (m) | P_hyd (W)     | P_mec (W) |\
 eta_T (%)  | eta_hyd (%) | N_s (rad/s)")
print('-'*104)
#parameters
for P_db , P_sb , Q_b , Torque_a , P_a_in in zip(P_da , P_sa , Q_a , Torque ,\
                                                 P_in):
    V_sa=V_s(Q_b,A_s)   #m/s
    V_da=V_d(Q_b,A_d)   #m/s
    h_a_pump=h_pump(P_db,P_sb,rho,V_da,V_sa,z_s,z_d)    #m
    P_a_mec=P_mec(Torque_a,N)   #W
    P_a_hyd=P_hyd (rho,Q_b,h_a_pump)    #W
    eta_T_a=eta_T (P_a_hyd,P_a_in)    #W
    eta_hyd_a=eta_hyd (P_a_hyd,P_a_mec)      #W
    N_a_s=N_s (N,Q_b,h_a_pump)
    Q_c=Q_b*1000*60    #L/min
    print(f"{Q_c:<8.0f}  | {Q_b:<9.4f} | {h_a_pump:<9.3f}  | {P_a_hyd:<10.3f}\
    | {P_a_mec:<10.3f} | {eta_T_a*100:<10.3f} | {eta_hyd_a*100:<11.3f}\
    | {N_a_s:<6.3f}")
