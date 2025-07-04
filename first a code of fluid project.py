#properties
import math
pi=math.pi
N=float(1750*pi/30)    #rad/s
T=float(((80-32)/1.8)+273)     #K
A_s=float((6**2)*pi/4*0.00064516)    #m^2
A_d=float(A_s)           #m^2
power_factor=float(0.875)
voltage=float(460)     #V
eta=float(0.9)
P_d=float(42.3/0.000145)     #Pa
P_s=float(-0.35/0.000145)    #Pa
Q=float(800*3.78541/1000/60)    #m^3/s
I=float(31)      #A
z_s=float(1*12*0.0254)      #m
z_d=float(3*12*0.0254)      #m
rho=float(996.69)           #Kg/m^3
#result
P_in=float((3**0.5)*power_factor*voltage*I)      #W
P_mec=eta*(3**0.5)*power_factor*voltage*I      #W
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
