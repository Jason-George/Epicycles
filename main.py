from Image import Image
from Fourier import Fourier
from Plot import Plot
import numpy as np
import cv2
import time

#If save 
save_animate = False
save_path = './Destination/im_1.gif'  #or mp4



#Preprocessing the Image

img = cv2.imread('./Images/HORSE.png',0)
img = cv2.resize(img,(300,200))
_,edges = cv2.threshold(img,127,255,cv2.THRESH_TRUNC)

edges = cv2.GaussianBlur(edges, (5,5), 0)
#edges = cv2.erode(edges, None, iterations=1)
edges = cv2.dilate(edges, None, iterations=1)
edges = cv2.Canny(edges,10,120)
#plt.imshow(edges,'gray')

contours, __ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#the above snippet of the code, copied from the jupyter notebook



im_1 = Image(contours)
path_1 = im_1.sort()

period_1, tup_circle_rads_1, tup_circle_locs_1= Fourier(n_approx = 1000, coord_1 = path_1).get_circles()


#Path to whereImageMagick is installed
loc = 'C:\Program Files\ImageMagick-7.0.10-Q16-HDRI\magick.exe'

if save_animate:
    Plot(period_1, tup_circle_rads_1, tup_circle_locs_1, speed = 45).plot(save = True,ani_name = save_path,
                                                                          ImageMagickLoc=loc)
else:
    Plot(period_1, tup_circle_rads_1, tup_circle_locs_1, speed = 80).plot(close_after_animation = False)

