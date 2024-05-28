import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def Time_Circular(L, P,gamma, beta, v_w, n=100):
    velocity = lambda j,n: (P/gamma)**(1/3)+2/3*v_w*np.cos(2*np.pi*j/n) +(gamma/P)**(1/3)*((v_w*np.cos(2*np.pi*j/n))**2-beta/(3*gamma))
    Sum = 0
    for i in range(n+1):
        Sum += 1/velocity(i,n)
    return L*Sum/(n+1)

def Fatigue_Circular(L, P,gamma, beta, v_w, n=100):
    return P*Time_Circular(L, P, gamma, beta, v_w, n)*(1+5/60*5.5)/4184

def Beta(mu, M, G, phi):
    return M*G*(np.sin(phi)+mu*np.cos(phi))

Phis = np.linspace(0, np.pi/22, 2000) # Change to 18 for the solution curve
Ps = np.linspace(600, 1600, 2000)

l, gamm, V_w, omega, Mu, m, g = 45000, 0.2, 10/3.6, np.pi/6, 0.0032, 75, 9.81

#print(Time_Linear(l, 500, gamm, Beta(Mu, m, g, 0), V_w, omega))

#T_over_Ps = Time_Linear(l, Ps, gamm, Beta(Mu, m, g, 0), V_w, omega)

P_Phi_Phi, P_Phi_P = np.meshgrid(Phis, Ps)


T_Circular = Time_Circular(l, P_Phi_P, gamm, Beta(Mu, m, g, P_Phi_Phi), V_w)

F_Circular = Fatigue_Circular(l, P_Phi_P, gamm, Beta(Mu, m, g, P_Phi_Phi), V_w)
F_Circular = F_Circular
 
T_highlight = np.where(F_Circular >= 2000.0, T_Circular, np.nan)  # Use np.nan to not plot points below 1000
F_highlight = np.where(F_Circular >= 2000.0, F_Circular, np.nan)  # Use np.nan to not plot points below 1000

fig = plt.figure(figsize=(10, 10))
ax = plt.axes(projection='3d')
 
ax.plot_surface(P_Phi_P, 180/np.pi*P_Phi_Phi, T_Circular/3600, cmap='cool', alpha=0.5)
ax.plot_wireframe(P_Phi_P, 180/np.pi*P_Phi_Phi, T_Circular/3600, color ='purple', rstride=50, cstride=50)
ax.plot_surface(P_Phi_P, 180/np.pi*P_Phi_Phi, T_highlight/3600, color='red', alpha=0.7)

ax.set_xlabel('Max Power (W)', fontsize=12)
ax.set_ylabel('Angle of Elevation (deg)', fontsize=12)
ax.set_zlabel('Time (Hours)', fontsize=12)
ax.set_title('Time as a Function of P_max (Circular)', fontsize=20)
#fig.savefig("Time vs P_max (Circular).png")
 
plt.show()

fig = plt.figure(figsize=(10, 10))
ax = plt.axes(projection='3d')
 
#ax.plot_wireframe(P_Phi_P, 180/np.pi*P_Phi_Phi, Max_Fatigue, color='black', rstride=2, cstride=2, alpha=0.5)
ax.plot_surface(P_Phi_P, 180/np.pi*P_Phi_Phi, F_Circular, cmap='cool', alpha=0.5)
ax.plot_wireframe(P_Phi_P, 180/np.pi*P_Phi_Phi, F_Circular, color ='purple', rstride=50, cstride=50)
ax.plot_surface(P_Phi_P, 180/np.pi*P_Phi_Phi, F_highlight, color='red', alpha=0.7)


ax.set_xlabel('Max Power (W)', fontsize=12)
ax.set_ylabel('Angle of Elevation (deg)', fontsize=12)
ax.set_zlabel('Energy Expenditure (cal)', fontsize=12)
ax.set_title('Fatigue as a Function of P_max (Circular)', fontsize=20)
#fig.savefig("Fatigue vs P_max (Circular).png")
plt.show()

'''
Here for Case 3
'''

Epsilon = 2e0

F_highlight = np.where(np.abs(F_Circular-2000)<=Epsilon, np.zeros((2000,2000)),255* np.ones((2000,2000)))  # Use np.nan to not plot points below 1000
im = Image.fromarray(F_highlight)
im.show()

#plt.imshow(F_highlight)
#plt.show()
