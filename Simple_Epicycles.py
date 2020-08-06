# import necessary packages
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#an array of values between one whole rotation
x = np.linspace(0, 2*np.pi, 800)
frames = len(x)


# set up the figure and subplot
fig = plt.figure()
ax = fig.add_subplot(
    111, aspect="equal", autoscale_on=False, xlim=(-5,5), ylim=(-5, 5)
)
ax.grid()

line_colors = ['green','black','cyan','purple','blue']
circle_colors = ['orange', 'yellow', 'green', 'magenta','brown']
radii = [2.0,1.5,1.1,0.7,0.3]

lines= []
circles=[]

#Create a list of lines and object objects
for y in range(5):
    
        
        circle = plt.Circle((0.0,0.0),radii[y],color=circle_colors[y],fill=False)
        line, = plt.plot([],[],'-', lw=2, color=line_colors[y])
        
        
        ax.add_patch(circle)
        ax.add_patch(line)
        lines.append(line,)
        circles.append(circle)


# animation function
def animate(i):

    line_coord_x=[0.0]
    line_coord_y=[0.0]

    different_freq = [1.0,2.0,3.5,4.2,7.0]
    
    X=0
    Y=0

    #calculate the different points 
    for z in range(len(lines)):
        X += radii[z] * np.cos(x[i]*different_freq[z]*2*np.pi)
        Y += radii[z] * np.sin(x[i]*different_freq[z]*2*np.pi)
        line_coord_x.append(X)
        line_coord_y.append(Y)


    #update the list of lines and object
    for index, obj in enumerate(zip(lines,circles)):
        A = [line_coord_x[index],line_coord_x[index+1]]
        B = [line_coord_y[index],line_coord_y[index+1]]
        obj[0].set_data(A,B)
        obj[1].center= (line_coord_x[index], line_coord_y[index])
        
        
    return circles + lines


# call the animation
ani = animation.FuncAnimation(fig, animate,frames=frames, interval=20,blit=True, repeat=True)

# show the animation
plt.show()

