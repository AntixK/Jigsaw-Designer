import numpy as np
from shapely.geometry import Polygon,Point

def uniform_sampler_rect(num_points, length, width, offset_x = 0, offset_y=0):
    """
    Returns the x,y coordinates for the points on an uniformly sampled grid
    inside the given rectangle. Uses rejection sampling
    NEVER USE THIS!
    :param num_points: Number of points to be sampled
    :param length: Length of the rectangle
    :param width: Width of the rectangle
    :param offset_x: x Offset of the rectangle from the origin
    :param offset_y: y offset of the rectangle from the origin
    :return: x,y coordinates of the sampled points
    """

    x = np.random.uniform(0, length, num_points)
    y = np.random.uniform(0,width,num_points)
    return x+offset_x,y+offset_y

def uniform_sampler_poly(num_points, polygon):
    min_x,min_y,max_x,max_y = polygon.bounds
    xx,yy = uniform_sampler_rect(num_points, max_x-min_x, max_y-min_y, offset_x=min_x,offset_y=min_y)

    points = [Point(x,y) for x,y in zip(xx,yy)]
    check = [xy.within(polygon) for xy in points]
    xx = xx[check]
    yy =yy[check]
    return xx, yy

if __name__ =="__main__":
    import matplotlib.pyplot as plt
    import seaborn as sns
    sns.set_style('darkgrid')
    l = 20
    w = 10
    # o_x, o_y = 10, 20
    # xx,yy = uniform_sampler_rect(1000,l,w, offset_x=o_x, offset_y=o_y)
    # plt.hlines(o_y, o_x, o_x+l, 'k', lw=2)
    # plt.hlines(o_y+w,o_x, o_x+l, 'k', lw=2)
    # plt.vlines(o_x, o_y, o_y+w, 'k', lw=2)
    # plt.vlines(o_x+l, o_y, o_y+w, 'k', lw=2)
    # plt.scatter(xx, yy,marker='.', color='r', alpha= 0.6)
    # plt.grid(True)
    # plt.show()

    a = [(141.4378366,-25.95915986), (165.4279876,-29.43400298), (163.1382942,-47.65345814), (133.1675418,-42.99807751)]
    arr = np.array(a)
    arr = np.row_stack((arr,arr[0]))
    p = Polygon(a)
    xx,yy = uniform_sampler_poly(200, p)

    plt.plot(arr[:,0],arr[:,1])
    plt.plot(xx,yy,'r.',alpha=0.6)
    plt.show()
