import numpy as np

def uniform_sampler_rect(num_points, length, width):
    """
    Returns the x,y coordinates for the points on an uniformly sampled grid
    inside the given rectangle. Uses rejection sampling
    NEVER USE THIS!
    :param num_points: Number of points to be sampled
    :param length: Length of the rectangle
    :param width: Width of the rectangle
    :return: x,y coordinates of the sampled points
    """

    x = np.random.uniform(0, length, num_points)
    y = np.random.uniform(0,width,num_points)
    return x,y


if __name__ =="__main__":
    import matplotlib.pyplot as plt
    import seaborn as sns
    sns.set_style('darkgrid')
    l = 20
    w = 10

    xx,yy = uniform_sampler_rect(1000,l,w)
    plt.hlines(0,0, l,'k',lw=2)
    plt.hlines(w,0, l,'k',lw=2)
    plt.vlines(0,0, w,'k',lw=2)
    plt.vlines(l,0, w,'k',lw=2)
    plt.plot(xx, yy, marker='.', color='k', linestyle='none')
    plt.grid(True)
    plt.show()


