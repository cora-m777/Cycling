import numpy as np
import matplotlib.pyplot as plt

def Time_Linear(L, P,gamma, beta, v_w, Omega):
    velocity = (P/gamma)**(1/3)+2/3*v_w*np.cos(Omega) +(gamma/P)**(1/3)*((v_w*np.cos(Omega))**2-beta/(3*gamma))
    return L/velocity

def Fatigue_Linear(L, P,gamma, beta, v_w, Omega):
    return P*Time_Linear(P, gamma, beta, v_w, Omega)

def Time_Circular(L, P,gamma, beta, v_w, n=100000):
    velocity = lambda j,n: (P/gamma)**(1/3)+2/3*v_w*np.cos(2*np.pi*j/n) +(gamma/P)**(1/3)*((v_w*np.cos(2*np.pi*j/n))**2-beta/(3*gamma))
    Sum = 0
    for i in range(n+1):
        Sum += 1/velocity(i,n)
    return L*Sum/(n+1)

def Fatigue_Circular(L, P,gamma, beta, v_w, n=100000):
    return P*Time_Circular(L, P, gamma, beta, v_w, n)

l,p,gam,v_wind, Beta = 45000, 500, 0.2, 7.5/3.6,0

angles = np.linspace(0, 2*np.pi, 1000)
linear_times = [Time_Linear(l, p, gam, Beta, v_wind, omega) for omega in angles]
linear_times = np.array(linear_times)

linear_fatigue = p*linear_times

circular_times = Time_Circular(l, p, gam, Beta, v_wind, n=30)*np.ones(1000)
circular_fatigue = p*circular_times

plt.grid(True)
plt.plot(angles*180/np.pi, 1/60**2 * linear_times, label="Linear Times")
plt.plot(angles*180/np.pi, 1/60**2 * circular_times, label="Circular Times")
plt.legend()
plt.xlabel("Wind to Cyclist Angle (deg)")
plt.ylabel("Time (hours)")
plt.xlim([0,360])
plt.title("Time vs. Wind Angle (P=500W; wind speed = 7.5kph)")
plt.show()

plt.grid(True)
plt.plot(angles*180/np.pi, 1/4184 * linear_fatigue, label="Linear Fatigue")
plt.plot(angles*180/np.pi, 1/4184 * circular_fatigue, label="Circular Fatigue")
plt.legend()
plt.xlabel("Wind to Cyclist Angle (deg)")
plt.ylabel("Fatigue (Calories Used)")
plt.xlim([0,360])
plt.title("Energy vs. Wind Angle  (P=500W; wind speed = 7.5kph)")
plt.show()

