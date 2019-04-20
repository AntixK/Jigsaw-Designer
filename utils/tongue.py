import numpy as np
import json
import matplotlib.pyplot as plt
from geomdl import NURBS

"""
All the tongue styles were designed using this amazing tool - http://nurbscalculator.in.

"""

with open('tongue_styles/'+'tongue_style_4.json') as f:
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

plt.plot(curve_points[:,0], curve_points[:,1])
plt.grid(True)
plt.show()
