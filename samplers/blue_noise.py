import numpy as np
import warnings
from shapely.geometry import Polygon,Point

def poisson_disc_sampler(min_dist, length, width, num_pts = None, k=30, offset_x = 0, offset_y=0):
    """
    O(N) algorithm for generating blue0noise using the poisson disc algorithm.

    Resources -
     [1] https://www.jasondavies.com/poisson-disc/
     [2] http://www.cemyuksel.com/cyCodeBase/soln/poisson_disk_sampling.html

    :param min_dist: minimum distance between any two points
    :param length: Length of the rectangle
    :param width: Width of the rectangle
    :param num_pts: Maximum number of points to sample
    :param k: number of trials to look for neighbourhood samples
    :param offset_x: x Offset of the rectangle from the origin
    :param offset_y: y offset of the rectangle from the origin
    :return:
    """
    cell_size = min_dist/np.sqrt(2)
    num_cell_w = int(np.ceil(width/cell_size))
    num_cell_l = int(np.ceil(length/cell_size))

    coords = [(x,y) for x in range(num_cell_l) for y in range(num_cell_w)]
    grid = {coord:None for coord in coords}

    def get_coords(pt):
        return int(pt[0]//cell_size), int(pt[1]//cell_size)

    def is_point_valid(pt):
        """
        Search for points in the neighbourhood of the given point
        and check if they are atleast min_dist away.
        :param pt: given point in the plane
        :return: Boolean.
        """
        pt_x, pt_y = get_coords(pt)
        #print(pt_x, min(pt_x+3, width),, pt_y, min(pt_y+3, length),num_cell_w)
        for x in range(max(pt_x -2, 0 ), min(pt_x+3, num_cell_l)):
            for y in range(max(pt_y - 2,0), min(pt_y+3, num_cell_w)):
                if grid[(x,y)] is None:
                    continue
                near_pt = samples[grid[(x,y)]]
                dist = (near_pt[0] - pt[0])**2 + (near_pt[1] - pt[1])**2

                if dist < min_dist**2:
                    return False
        return True

    pt = (np.random.uniform(0,width), np.random.uniform(0,length))
    samples = [pt]
    grid[get_coords(pt)] = 0
    active_list = [0]
    num_samples = 1

    while active_list:
        ind = np.random.choice(active_list)
        pivot = samples[ind]

        for _ in range(k):
            r, theta = np.random.uniform(cell_size, 2 * cell_size), np.random.uniform(0, 2 * np.pi)
            pt = pivot[0] + r * np.cos(theta), pivot[1] + r * np.sin(theta)
            if not (0 <= pt[0] < length and 0 <= pt[1] < width):
                continue

            if is_point_valid(pt):
                samples.append(pt)
                num_samples += 1

                if num_pts is not None and (num_samples+1) > num_pts:
                    samples = np.array(samples)
                    return samples[:, 0]+offset_x, samples[:, 1]+offset_y

                active_list.append(num_samples - 1)
                grid[get_coords(pt)] = num_samples - 1

        active_list.remove(ind)

    if num_pts is not None and num_samples < num_pts:
        warnings.warn("Only {} samples could be generated".format(num_samples))

    samples = np.array(samples)
    return samples[:,0]+offset_x, samples[:,1]+offset_y

def poisson_disc_sampler_poly(min_dist, polygon):
    min_x,min_y,max_x,max_y = polygon.bounds
    xx,yy = poisson_disc_sampler(min_dist, max_x-min_x, max_y-min_y, offset_x=min_x,offset_y=min_y)

    points = [Point(x,y) for x,y in zip(xx,yy)]
    check = [xy.within(polygon) for xy in points]
    xx = xx[check]
    yy =yy[check]
    return xx, yy

def best_candidate_sampler():
    # Resources
    # [1] https://blog.demofox.org/2017/10/20/generating-blue-noise-sample-points-with-mitchells-best-candidate-algorithm/

    pass

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import seaborn as sns
    from time import time

    sns.set_style('darkgrid')

    # l,w = 60,45
    # r = 1.57
    # o_x,o_y = 10,20
    # st = time()
    # xx,yy = poisson_disc_sampler(r,l,w, num_pts=1000, offset_x=o_x, offset_y=o_y)
    # e = time() - st
    # print("Time:{}, Num samples {}".format(e, len(xx)))
    # print()
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
    xx,yy = poisson_disc_sampler_poly(1.2, p)

    plt.plot(arr[:,0],arr[:,1])
    plt.plot(xx,yy,'r.',alpha=0.6)
    plt.show()
