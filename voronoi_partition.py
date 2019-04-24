import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt
from samplers.regular import regular_sampler_rect
from samplers.blue_noise import poisson_disc_sampler
from utils.tongue import insert_tongue_in_line
from shapely.geometry import Point

l = 20
w = 10
o_x, o_y = 10, 20
xx,yy = regular_sampler_rect(1.5,l,w,offset_x=o_x, offset_y=o_y)
#xx,yy = poisson_disc_sampler(1.2,l,w, num_pts=None, offset_x=o_x, offset_y=o_y)
points = np.array(list(zip(xx,yy))).squeeze()
print(points.shape)
#points = np.array([[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2],[2, 0], [2, 1], [2, 2]])
vor = Voronoi(points)

for vpair in vor.ridge_vertices:
    if vpair[0] >= 0 and vpair[1] >= 0:
        v0 = vor.vertices[vpair[0]]
        v1 = vor.vertices[vpair[1]]
        # Draw a line from v0 to v1.

        # sort the parts such that start point < end point
        if v0[0] < v1[0]:
            a = Point(v0)
            b = Point(v1)
        elif v0[0] > v1[0]:
            a = Point(v1)
            b = Point(v0)
        elif v0[0] == v1[0]:
            if v0[1] < v1[1]:
                a = Point(v1)
                b = Point(v0)
            elif v0[1] > v1[1]:
                a = Point(v0)
                b = Point(v1)

        print(v0,v1)
        curve_points = insert_tongue_in_line(a, b, id=2)
        plt.plot(curve_points[:, 0], curve_points[:, 1], 'r', lw=2)

        # plt.plot([v0[0], v1[0]], [v0[1], v1[1]], linewidth=2)
voronoi_plot_2d(vor)
plt.show()