import numpy as np

def regular_sampler_rect(min_dist, length, width, offset_x =0, offset_y=0):
    """
    Returns the x,y coordinates for the points on a regular grid
    inside the given rectangle.
    :param min_dist: Minimum distance between any two points
    :param length: Length of the rectangle
    :param width: Width of the rectangle
    :param offset_x: x Offset of the rectangle from the origin
    :param offset_y: y offset of the rectangle from the origin
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
    return xx[1:,1:].reshape(-1,1)+offset_x, yy[1:,1:].reshape(-1,1)+offset_y


if __name__ =="__main__":
    import matplotlib.pyplot as plt
    import seaborn as sns
    sns.set_style('darkgrid')
    l = 20
    w = 10
    o_x, o_y = 10, 20
    xx,yy = regular_sampler_rect(0.9,l,w,offset_x=o_x, offset_y=o_y)
    plt.hlines(o_y, o_x, o_x+l, 'k', lw=2)
    plt.hlines(o_y+w,o_x, o_x+l, 'k', lw=2)
    plt.vlines(o_x, o_y, o_y+w, 'k', lw=2)
    plt.vlines(o_x+l, o_y, o_y+w, 'k', lw=2)
    plt.scatter(xx, yy,marker='.', color='r', alpha= 0.6)
    plt.grid(True)
    plt.show()


