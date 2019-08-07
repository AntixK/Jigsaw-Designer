from macros import *
import numpy as np
import matplotlib.pyplot as plt
import cv2

def func():
    img = cv2.imread(TEMPLATE_STYLE_PATH + 'dolphin.jpg',-1)
    thresh = 240
    img = cv2.threshold(img, thresh, 255, cv2.THRESH_BINARY)[1]

    edges = cv2.Canny(img,10,250)
    #
    # # print(edges.shape)
    kernel = np.ones((5, 5), np.uint8)
    edges = cv2.dilate(edges,kernel,iterations = 2)
    kernel = np.ones((3, 3), np.uint8)
    edges = cv2.erode(edges, kernel, iterations=2)
    # print(edges.shape)

    plt.imshow(img,cmap='gray')
    plt.show()
    x,y = np.where(edges > 0)
    pts = np.array(list(zip(x,y)))

    """
    The indexing in the above array starts from the top left.
    To make it start from the bottom left, we perfrom the following
    transformations.
     - Rotate the image by 90 degrees so that it is upright (transpose)
     - Shift the image upwards so that it starts from 0
    """
    theta = 90 * np.pi / 180
    rot_matrix = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    pts = pts @ rot_matrix
    pts[:,1] -= min(pts[:,1])
    print(pts.shape)
    return pts,edges

if __name__=="__main__":
    a,b = func()
    #plt.imshow(b)
    plt.plot(a[:,0],a[:,1], 'k.',ms=1)
    plt.show()