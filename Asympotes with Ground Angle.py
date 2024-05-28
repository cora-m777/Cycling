'''
Imports
'''
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

'''
Track and Athlete Parameters
'''
phi =0.0
mu = 0.0032
m = 75
g = 9.81
#l,p,gam,v_wind = 45000, 500, 0.2, 7.5/3.6
l,p,gam = 45000, 500, 0.2

'''
Angles at which the velocity is 0 --implying infinite time. 
'''
def Asymptote(P, vw, ang):
	Omega = vw*np.cos(ang)
	return np.arcsin(1/(m*g*np.sqrt(1+mu**2))*(3*gam*(P/gam)**(2/3)+2*gam*(P/gam)**(1/3)*Omega + Omega**2))-np.arcsin(mu/np.sqrt(1+mu**2))

'''
Domain over which the asymptotes are found.
'''	
# Powers exerted by the athlete
Powers = np.linspace(0, 2000, 6)
# Different wind angles
Wind_Angles = np.linspace(0,2*np.pi,1000)
# Wind velocities in m/s
Wind_Velocities = 1/3.6*np.linspace(0,30,1000)


'''
Making a meshgrid of the different angles and velocities at which the asymptotes are found.
'''
Ang, Vel = np.meshgrid(Wind_Angles, Wind_Velocities)
'''
temp = 180/np.pi*Asymptote(Pow, Vel, Ang)

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot_surface(Vel*3.6, 180/np.pi*Ang, temp, cmap='viridis')
ax.set_xlabel('Wind Velocity (kph)')
ax.set_ylabel('Wind Angle (deg)')
ax.set_zlabel('φ Asymptote (deg)')
plt.show()
'''

'''
Graphing
'''
fig = plt.figure()
#ax = plt.axes(projection='3d')
for i in range(6):
	# Sampling the power at which the hill in question is attempted.
	Pow = Powers[i]
	
	# Converting the angle of elevation to road grade (a Global Cycling Network metric from the roadgrade of 36% video)
	Asymptotes = np.tan(Asymptote(Pow, Vel, Ang))
	
	Title = "Power = "+str(Pow)+"W."
	
	ax = fig.add_subplot(3, 2, i+1, projection='3d')
	ax.plot_surface(Vel*3.6, 180/np.pi*Ang, 100*Asymptotes, cmap='viridis')
	ax.set_xlabel('Wind Velocity (kph)')
	ax.set_ylabel('Wind Angle (deg)')
	ax.set_zlabel('Road Grade (%)')
	ax.view_init(15, 205)
	plt.title(Title)
fig = plt.gcf()
fig.set_size_inches(15, 12)
plt.savefig("Asymptotes.png")
plt.show()

'''
for i in range(6):
	Pow = Powers[i]
	Wind_Angles = np.linspace(0,2*np.pi,1000)
	omega = v_wind*np.cos(Wind_Angles)
	
	Title = "Power = "+str(Pow)+"W."

	Asymptote_Wind = Asymptote(Pow, omega)
	
	plt.subplot(2,3,i+1)
	plt.grid()
	plt.plot(180/np.pi*Wind_Angles, 180/np.pi*Asymptote_Wind)
	plt.xlabel("Wind Angle (deg)")
	plt.ylabel("φ Asymptote (deg)")
	#plt.ylim([0,10])
	plt.title(Title)
fig = plt.gcf()
fig.set_size_inches(20, 15)
plt.savefig("Asymptotes.png")
plt.show()
'''

