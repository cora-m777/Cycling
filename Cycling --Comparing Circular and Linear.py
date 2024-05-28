'''
Imports
'''

import numpy as np
import matplotlib.pyplot as plt

'''
Time and Fatigue Functions
'''

def Time_Linear(L, P,gamma, beta, v_w, Omega):
    velocity = (P/gamma)**(1/3)+2/3*v_w*np.cos(Omega) +(gamma/P)**(1/3)*((v_w*np.cos(Omega))**2-beta/(3*gamma))
    return L/velocity

def Fatigue_Linear(L, P,gamma, beta, v_w, Omega):
    return P*Time_Linear(L, P, gamma, beta, v_w, Omega)*(1+5/60*5.5)/4184

def Time_Circular(L, P,gamma, beta, v_w, Omega, n=1000, dist=None):
    velocity = lambda j,n: (P/gamma)**(1/3)+2/3*v_w*np.cos(2*np.pi*j/n) +(gamma/P)**(1/3)*((v_w*np.cos(2*np.pi*j/n))**2-beta/(3*gamma))
    Sum = 0
    #print("DIST:", dist)
    if dist is None:
    	end_point = n+1
    else:
    	end_point = int(n*dist/L + 1)
    #print("END POINT:", end_point)
    velocities = []
    for i in range(1, end_point):
        velocities.append(velocity(i,n))
        Sum += 1/velocities[-1]        
    return L*Sum/(n+1), velocities

def Fatigue_Circular(L, P,gamma, beta, v_w, n=1000):
    return P*Time_Circular(L, P, gamma, beta, v_w, n)[0]*(1+5/60*5.5)/4184
    
'''    
def Find_Numerical_Derivative(indep_list, dep_list):
    n_points = len(indep_list)
    deriv = [(dep_list[i+1]-dep_list[i])/(indep_list[i+1]-indep_list[i]) for i in range(n_points-1)]
    return np.array(deriv)
'''

'''
Graphing Total Time and Fatigue for a 45km flat course --both circular and linear
'''

# Course and athlete parameters
phi =0.0
mu = 0.0032
l,p,gam,v_wind, Beta = 45000, 500, 0.2, 7.5/3.6, 75*9.81*(np.sin(phi)+mu*np.cos(phi))

# All possible wind angles
angles = np.linspace(0, 2*np.pi, 1000)

# Linear time and fatigue
linear_times = [Time_Linear(l, p, gam, Beta, v_wind, omega) for omega in angles]
linear_times = np.array(linear_times)

linear_fatigue = [Fatigue_Linear(l, p, gam, Beta, v_wind, omega) for omega in angles]
linear_fatigue = np.array(linear_fatigue)

# Constructing circular time and fatigue
circular_times = []
circular_velocities = []
circular_fatigue = []

for omega in angles:
	temp = Time_Circular(l, p, gam, Beta, v_wind, omega)
	circular_times.append(temp[0])
	circular_fatigue .append(Fatigue_Circular(l, p, gam, Beta, v_wind, omega))
circular_times = np.array(circular_times)


# Graphing these results
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
plt.plot(angles*180/np.pi, linear_fatigue, label="Linear Fatigue")
plt.plot(angles*180/np.pi, circular_fatigue, label="Circular Fatigue")
plt.legend()
plt.xlabel("Wind to Cyclist Angle (deg)")
plt.ylabel("Fatigue (Calories Used)")
plt.xlim([0,360])
plt.title("Energy vs. Wind Angle  (P=500W; wind speed = 7.5kph)")
plt.show()

'''
Plotting each race and the velocity at each point in the course as the wind angle changes
'''
distance = np.linspace(0,l,1000)

for i in range(9):
	# Varying wind angles
	Angle = 2*np.pi/9*i
	
	# Grabbing the time and velocity from the linear course
	temp = Time_Circular(l, p, gam, Beta, v_wind, Angle)
	circular_time = temp[0]
	circular_velocities = np.array(temp[1])
	linear_time = Time_Linear(l, p, gam, Beta, v_wind, Angle)
	linear_velocities = l/linear_time * np.ones(len(circular_velocities))
	ave_circ_vel = np.mean(circular_velocities)*np.ones(len(linear_velocities))
	
	# Titles for stuff
	Title = "Angle = "+str(round(Angle,2))+" rad"
	lin_label = "Lin. Time: "+str(round(linear_time/60,1)) + " min."
	circ_label = "Circ. Time: "+str(round(circular_time/60,1)) + " min."
	ave_circ_label = "Mean circ. vel. = "+str(round(3.6*np.mean(circular_velocities),1)) + " kph"
	
	# Plotting
	plt.subplot(3, 3, i+1)
	plt.grid(True)
	plt.plot(1/1000*distance, 3.6*linear_velocities, label=lin_label,color='blue')
	plt.plot(1/1000*distance, 3.6*circular_velocities, label=circ_label,color='orange')
	plt.plot(1/1000*distance, 3.6*ave_circ_vel, "--", label=ave_circ_label, color='orange')
	plt.xlabel("Distance (km)")
	plt.ylabel("Velocity (kph)")
	plt.legend()
	plt.title(Title)
fig = plt.gcf()
fig.set_size_inches(14, 14)
plt.savefig("Test.png")
plt.show()

'''
Graphing the time and fatigue as it relates to the angles of elevation. Trying to find where asymptotes occur.
'''
Ground_Angles = np.linspace(0, np.pi/30,1000)

# Course and athlete parameters
phi =0.0
mu = 0.0032
m = 75
g = 9.81
l,p,gam,v_wind = 45000, 500, 0.2, 7.5/3.6

# Beta from the ground angle
Betas = [m*g*(np.sin(phi)+mu*np.cos(phi)) for phi in Ground_Angles]

# Linear times and fatigue
linear_times = [Time_Linear(l, p, gam, Beta, v_wind, 0) for Beta in Betas]
linear_times = np.array(linear_times)

linear_fatigue = [Fatigue_Linear(l, p, gam, Beta, v_wind, omega) for omega in angles]
linear_fatigue = np.array(linear_fatigue)

# Circular times and fatigue
circular_times = []
circular_velocities = []
circular_fatigue = []

for Beta in Betas:
	temp = Time_Circular(l, p, gam, Beta, v_wind, 0)
	circular_times.append(temp[0])
	circular_fatigue.append(Fatigue_Circular(l, p, gam, Beta, v_wind, 0))
circular_times = np.array(circular_times)

# Graphing this stuff
plt.grid(True)
plt.plot(180/np.pi*Ground_Angles, 1/60**2 * linear_times, label="Linear Times")
plt.plot(180/np.pi*Ground_Angles, 1/60**2 * circular_times, label="Circular Times")
plt.legend()
plt.xlabel("Elevation Angle (deg)")
plt.ylabel("Time (hours)")
plt.title("Time vs. Elevation Angle (P=500W; wind speed = 7.5kph)")
plt.show()

plt.grid(True)
plt.plot(180/np.pi*Ground_Angles, linear_fatigue, label="Linear Fatigue")
plt.plot(180/np.pi*Ground_Angles, circular_fatigue, label="Circular Fatigue")
plt.legend()
plt.xlabel("Elevation Angle (deg)")
plt.ylabel("Fatigue (Calories Used)")
plt.title("Energy vs. Elevation Angle  (P=500W; wind speed = 7.5kph)")
plt.show()
