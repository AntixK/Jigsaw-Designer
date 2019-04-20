import numpy as np

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


if __name__ =="__main__":
    import matplotlib.pyplot as plt
    import seaborn as sns
    sns.set_style('darkgrid')
    l = 20
    w = 10
    o_x, o_y = 10, 20
    xx,yy = uniform_sampler_rect(1000,l,w, offset_x=o_x, offset_y=o_y)
    plt.hlines(o_y, o_x, o_x+l, 'k', lw=2)
    plt.hlines(o_y+w,o_x, o_x+l, 'k', lw=2)
    plt.vlines(o_x, o_y, o_y+w, 'k', lw=2)
    plt.vlines(o_x+l, o_y, o_y+w, 'k', lw=2)
    plt.scatter(xx, yy,marker='.', color='r', alpha= 0.6)
    plt.grid(True)
    plt.show()


