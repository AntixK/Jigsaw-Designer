import numpy as np
import json
import matplotlib.pyplot as plt
from geomdl import NURBS
from utils.macros import *
from shapely.geometry import Point
"""
All the tongue styles were designed using this amazing tool - http://nurbscalculator.in.

"""
def get_tongue(id = 1, theta = 0, scale = 1.0):
    """
    Get the tongue vector from the list of tongue styles in the assets
    :param id: Id indicating the tongue style
    :param theta: Rotation angle for the tongue
    :param scale: Scaling of the tongue
    :return: Tongue array
    """
    with open(TONGUE_STYLE_PATH+'tongue_style_{}.json'.format(id)) as f:
        data = json.load(f)
    knots = data['knots']
    m = len(knots)
    d = data['degree']
    p = m - d - 1
    control_points = np.array(data['controlPoints']).reshape(-1,4)

    # Sanity check
    assert p == control_points.shape[0]

    #discard z and w vectors
    control_points = [[x,y] for x,y in control_points[:,:2]]

    # Set up curve
    curve = NURBS.Curve()
    curve.degree = d
    curve.ctrlpts = control_points

    # Use a specialized knot vector
    curve.knotvector = knots
    # Set evaluation delta
    curve.delta = 1/data['discretization']
    # Evaluate curve
    curve.evaluate()
    curve_points = np.array(curve.evalpts)
    # scale the curve to be at zero
    curve_points[:,0] -= min(curve_points[:,0])
    #theta = theta*np.pi/180
    rot_matrix = scale*np.array([[np.cos(theta), -np.sin(theta)],[np.sin(theta), np.cos(theta)]])
    curve_points = curve_points@rot_matrix
    return curve_points

def insert_tongue_in_line(start_pt, end_pt, **kwargs):

    a = 0.333
    x = start_pt.x*(1-a) + a*end_pt.x
    y = start_pt.y*(1-a) + a*end_pt.y
    pt_1 = Point([x,y])

    x = start_pt.x*(1-(2*a)) + (2*a)*end_pt.x
    y = start_pt.y*(1-(2*a)) + (2*a)*end_pt.y
    pt_2 = Point([x, y])

    if abs(end_pt.x-start_pt.x) <= 1e-5:
        angle = 90
        angle = angle*np.pi/180
    else:
        m = (end_pt.y - start_pt.y)/(end_pt.x-start_pt.x)
        angle = 2*np.pi - np.arctan(m)

    s = np.sqrt((pt_2.x-pt_1.x)**2+(pt_2.y - pt_1.y)**2)/4.6
    curve_points = get_tongue(scale=s,theta=angle, **kwargs)

    curve_points[:,0] += pt_1.x
    curve_points[:,1] += pt_1.y
    #
    # plt.plot((start_pt.x, pt_1.x), (start_pt.y, pt_1.y), 'r',lw=2)
    # plt.plot((pt_1.x, pt_2.x), (pt_1.y, pt_2.y),lw=2)
    # plt.plot((pt_2.x, end_pt.x), (pt_2.y, end_pt.y),lw=2)
    # plt.plot(curve_points[:,0], curve_points[:,1],'r',lw=2)
    # # plt.plot((curve_points[-1,0], end_pt.x), (curve_points[-1,1], end_pt.y),'r',lw=2)
    #
    # plt.grid(True)

    curve_points = np.insert(curve_points, 0, [pt_1.x, pt_1.y], axis=0)
    curve_points = np.insert(curve_points, 0, [start_pt.x, start_pt.y], axis=0)
    curve_points = np.insert(curve_points, -1, [pt_2.x, pt_2.y], axis=0)
    curve_points = np.insert(curve_points, -1, [end_pt.x, end_pt.y], axis=0)

    # plt.plot(curve_points[:, 0], curve_points[:, 1], 'r', lw=2)
    # plt.show()
    return curve_points


if __name__ == "__main__":
    # curve_points = get_tongue(2,scale=0.2)
    # plt.plot(curve_points[:,0], curve_points[:,1])
    # plt.grid(True)
    # plt.show()
    a = Point([13,27])
    b = Point([13,25])
    insert_tongue_in_line(a,b)

    # dis = []
    # S = np.arange(0.01,2.5,0.01)
    # for s in S:
    #     curve_points = get_tongue(2, scale=s)
    #     d = np.sqrt((curve_points[0, 0] - curve_points[-1, 0]) ** 2 + (curve_points[0, 1] - curve_points[-1, 1]) ** 2)
    #     dis.append(d)
    #
    # m = (dis[-1] - dis[0])/(S[-1]-S[0])
    # print(m)
    # plt.plot(S, dis)
    # plt.show()