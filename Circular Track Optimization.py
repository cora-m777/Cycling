import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize

def T_P (gamma, v_w, beta, L, P, n=1e5, delta=0):
    sum = 0
    for i in range(int(n)):
        numerator = 3*P**(2/3) - gamma**(4/3)*((v_w*np.cos(2*np.pi*i/n+delta))**2 -3*beta/gamma)
        sqrt_denominator = 3*P**(5/3) + 2*P**(4/3)*gamma**(1/3)*v_w*np.cos(2*np.pi*i/n+delta) + P*gamma**(2/3)*((v_w*np.cos(2*np.pi*i/n+delta))**2 -3*beta/gamma)
        sum += numerator/(sqrt_denominator)**2
    return -1*L/n*sum

phi =0.0
mu = 0.0032
l,gam,v_wind, Beta = 45000, 0.2, 7.5/3.6, 75*9.81*(np.sin(phi)+mu*np.cos(phi))

T_P_P = lambda P: T_P(gam, v_wind, Beta, l, P)

Ps = np.linspace(100, 5000, 1000)
T_Ps = T_P_P(Ps)

plt.semilogy(Ps, np.abs(T_Ps))
plt.show()