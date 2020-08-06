import numpy as np

from matplotlib import animation
from matplotlib import pyplot as plt
from matplotlib.patches import ConnectionPatch

class Plot(object):
    def __init__(self, period, tup_circles_rad, tup_circles_loc, speed=8):
        self.fig = plt.figure()
        self.period = period
        self.tup_circles_loc = tup_circles_loc[0] #since the tuple is nested
        self.speed = speed

                   
        self.axes = self.fig.add_subplot(111)
        # Point that draws the images
        self.final_points = (self.get_final_point(self.axes),)
        
        X = (np.amin(tup_circles_loc[-1].real)-10), np.amax(tup_circles_loc[-1].real)+10
        Y = np.amax(tup_circles_loc[-1].imag)+10, np.amin(tup_circles_loc[-1].imag)-10

        self.x_lim = tuple(X)
        self.y_lim = tuple(Y)



        circle_lst = list()
        line_lst = list()
        for n, circle_rad_lst in enumerate(tup_circles_rad):
            for radius in circle_rad_lst:
                circle = self.get_circle((0,0), radius)
                line, = plt.plot([], [], "-", lw=1, color="black")
                
                self.axes.add_patch(circle)
                self.axes.add_patch(line)
                
                circle_lst.append(circle)
                line_lst.append(line)
            # Center circle doesn't move, so remove it!
            circle_lst.pop(0)
        self.tup_circles_lst = tuple(circle_lst)
        self.tup_lines_lst = tuple(line_lst)
            
        
    def get_circle(self, loc, radius):
        return plt.Circle(loc, np.absolute(radius), alpha = 1, fill = False)
    
    
    
  

    def get_final_point(self, axis):
        return axis.plot(0,0, color='#000000')[0]
    
    
    def plot(self, save = False, ani_name = None, ImageMagickLoc = None, close_after_animation = True):
        
        update, time = self.get_draw(close_after_animation=close_after_animation, save=save)
            
        #for ax in self.axes:
           
        self.axes.set_xlim(self.x_lim)
        self.axes.set_ylim(self.y_lim)
            
        ani = animation.FuncAnimation(self.fig, update, time, interval=1, blit=True, repeat=close_after_animation,repeat_delay=3000)
        if save is True and ImageMagickLoc is not None:
            #plt.rcParams['savefig.bbox'] = "tight"
            #plt.rcParams['savefig.orientation'] = "landscape"
            #plt.rcParams['figure.autolayout'] = True
            
            plt.rcParams['animation.convert_path'] = ImageMagickLoc
            writer = animation.ImageMagickFileWriter(fps = 30,bitrate=1800)
            ani.save(ani_name if ani_name else 'gif_1.gif', writer=writer,dpi=300)
        else:
            # TODO(Darius): Figure out a way to get Matplotlib to close the figure nicely after animation is done
            try:
                plt.show()
            except e as Exception: # _tkinter.TclError: invalid command name "pyimage10"
                pass

        plt.clf()
        plt.cla()
        plt.close()
        
    def get_draw(self, close_after_animation, save):
        time = np.arange(0, self.period, self.speed)
        def update(i):
            if close_after_animation and not save and i == time[-1]:
                plt.close()
            else:
                prev_real=0
                prev_img=0
                for index,obj_art in enumerate(zip(self.tup_circles_lst, self.tup_lines_lst)):
                    obj_art[0].center = self.get_circle_loc_point(circle_idx=index, time_idx = i)
                    real,img = self.get_line_point(circle_idx=index, time_idx = i)
                    X = [prev_real,real]
                    Y = [prev_img,img]
                    obj_art[1].set_data(X,Y)
                    prev_real = real
                    prev_img = img
                       
                
                    self.final_points[0].set_data(self.get_circle_loc_slice(-1, i))
            return ([])
        return update, time
        
    def get_circle_loc_point(self,circle_idx, time_idx):
        return (self.tup_circles_loc[circle_idx, time_idx].real, self.tup_circles_loc[circle_idx, time_idx].imag)
    
    def get_line_point(self, circle_idx, time_idx):
        return (self.tup_circles_loc[circle_idx, time_idx].real, self.tup_circles_loc[circle_idx, time_idx].imag)
    
    def get_circle_loc_slice(self,circle_idx, time_idx):
        return (self.tup_circles_loc[circle_idx, :time_idx].real, self.tup_circles_loc[circle_idx, :time_idx].imag)

   


