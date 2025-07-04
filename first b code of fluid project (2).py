#properties
import math
pi=math.pi
N=1750*pi/30    #rad/s
T=((80-32)/1.8)+273     #K
A_s=(6**2)*pi/4*0.00064516    #m^2
A_d=A_s           #m^2
power_factor=0.875
voltage=460     #V
eta=0.9
P_d=[53.3,48.3,42.3,36.9,33,27.8,15.3,7.3]        #Psi
P_da=[x/0.000145 for x in P_d]     #Pa
P_s=[0.65,0.25, -0.35, -0.92, -1.24, -1.62, -2.42, -2.89]          #Psi         
P_sa=[y/0.000145 for y in P_s]           #Pa
Q=[0,500,800,1000,1100,1200,1400,1500]    #gpm
Q_a=[x*3.78541/1000/60 for x in Q]      #m^3/s
I=[18,26.2,31,33.9,35.2,36.3,38,39]      #A
z_s=1*12*0.0254      #m
z_d=3*12*0.0254      #m
rho=996.69           #Kg/m^3
#result
def P_in (power_factor,voltage,I):
    return((3**0.5)*power_factor*voltage*I)      #W
def P_mec(power_factor,voltage,I,eta):
    return(eta*(3**0.5)*power_factor*voltage*I)      #W
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
print (f"Q (gpm) | Q (m^3/s) | h_pump (m) | P_hyd (W)     | eta_T (%)  | eta\
_hyd (%) | N_s (rad/s)")
print('-'*90)
#parameters
for P_db , P_sb , Q_b , I_a in zip(P_da , P_sa , Q_a , I):
    V_sa=V_s(Q_b,A_s)   #m/s
    V_da=V_d(Q_b,A_d)   #m/s
    h_a_pump=h_pump(P_db,P_sb,rho,V_da,V_sa,z_s,z_d)    #m
    P_a_in=P_in (power_factor,voltage,I_a)    #W
    P_a_mec=P_mec(power_factor,voltage,I_a,eta)   #W
    P_a_hyd=P_hyd (rho,Q_b,h_a_pump)    #W
    eta_T_a=eta_T (P_a_hyd,P_a_in)    #W
    eta_hyd_a=eta_hyd (P_a_hyd,P_a_mec)      #W
    N_a_s=N_s (N,Q_b,h_a_pump)
    Q_c=Q_b*1000*60/3.78541    #gpm
    print(f"{Q_c:<6.0f}  | {Q_b:<9.4f} | {h_a_pump:<9.3f}  | {P_a_hyd:<10.3f}\
    | {eta_T_a*100:<10.3f} | {eta_hyd_a*100:<11.3f} | {N_a_s:<6.3f}")
    
    
