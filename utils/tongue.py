import numpy as np
import json
import matplotlib.pyplot as plt
from geomdl import NURBS
from macros import *
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
    # scale the curve to be above zero
    #curve_points[:,1] -= min(curve_points[:,1])
    theta = theta*np.pi/180
    rot_matrix = scale*np.array([[np.cos(theta), -np.sin(theta)],[np.sin(theta), np.cos(theta)]])
    curve_points = curve_points@rot_matrix
    return curve_points

def insert_tongue_in_line(start_pt, end_pt):
    pass

if __name__ == "__main__":
    curve_points = get_tongue(2,scale=0.2)
    plt.plot(curve_points[:,0], curve_points[:,1])
    plt.grid(True)
    plt.show()
