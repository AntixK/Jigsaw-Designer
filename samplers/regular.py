import numpy as np

def regular_sampler_rect(min_dist, length, width):
    """
    Returns the x,y coordinates for the points on a regular grid
    inside the given rectangle.
    :param min_dist: Minimum distance between any two points
    :param length: Length of the rectangle
    :param width: Width of the rectangle
    :return: x,y coordinates
    """

    x,d_x = np.linspace(0, length, length//min_dist,retstep =True, endpoint=False)
    y,d_y = np.linspace(0, width, width//min_dist,retstep=True, endpoint=False)

    # sanity check
    try:
        assert d_x >= min_dist and d_y >= min_dist
    except AssertionError:
        raise RuntimeError("min_dist param too large for the given ploygon")

    xx, yy = np.meshgrid(x, y)
    return xx[1:,1:].reshape(-1,1), yy[1:,1:].reshape(-1,1)


if __name__ =="__main__":
    import matplotlib.pyplot as plt
    import seaborn as sns
    sns.set_style('darkgrid')
    l = 20
    w = 10

    xx,yy = regular_sampler_rect(0.9,l,w)
    plt.hlines(0,0, l,'k',lw=2)
    plt.hlines(w,0, l,'k',lw=2)
    plt.vlines(0,0, w,'k',lw=2)
    plt.vlines(l,0, w,'k',lw=2)
    plt.plot(xx, yy, marker='.', color='k', linestyle='none')
    plt.grid(True)
    plt.show()


