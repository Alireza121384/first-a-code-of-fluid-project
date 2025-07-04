#properties
import math
pi=math.pi
N=float(1100*pi/30)    #rad/s
T=float(25+273)     #K
A_s=(0.15**2)*pi/4    #m^2
A_d=float(A_s)           #m^2
P_in=480             #W
P_d=float(0.18*100000)     #Pa
P_s=float(-0.05*100000)   #Pa
Q=float(197/1000/60)    #m^3/s
Torque=1.9         #N.m
z_s=0      #m
z_d=0      #m
rho=float(997.05)           #Kg/m^3
#result
P_mec=Torque*N       #W
V_s=Q/A_s        #m/s
V_d=Q/A_d        #m/s
h_pump=(((P_d)-(P_s))/(rho*9.81))+((((V_d)**2)-((V_s)**2))/(2*9.81))+z_d-z_s #m
P_hyd=rho*9.81*Q*h_pump       #W
N_s=N*(Q**0.5)/(h_pump**0.75)   #rad/s
eta_T=P_hyd/P_in
eta_hyd=P_hyd/P_mec
print(f'h_pump:{h_pump:.3f}     m\nP_hyd;{P_hyd:.3f}   W\
\neta_T:{eta_T*100:.3f}      %\neta_hyd:{eta_hyd*100:.3f}    %\
\nN_s:{N_s:.3f}        rad/s')
