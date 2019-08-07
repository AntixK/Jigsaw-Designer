import numpy as np
from shapely.geometry import Polygon, Point
from shapely.affinity import scale, rotate


def polyfy_rect(length, width):
    return Polygon([(0,0),(0,width),(length,width),(length,0)])

def polyfy_cir(origin, radius, resolution = 100):
    """
    Create an polygon representing circle
    :param origin: Tuple containing the origin of the circle
    :param radius: Radius of the circle
    :param resolution:Number of points to approximate the ellipse
    :return: Shapely polygon
    """
    circle = Point(origin).buffer(radius, resolution=resolution)
    return Polygon(list(circle.exterior_coords))

def polyfy(points):
    """
    Convert a list of points to a shapely polygon
    :param points:List of tuples of points or array of shape Nx2
    :return: Shapely polygon
    """
    if isinstance(points, list):
        points = np.array(points)
    assert points.shape[1] ==2
    return Polygon(points)

def polyfy_ell(origin, major_ax, minor_ax, angle = 0, resolution =100):
    """
    Create an polygon representing an ellipse
    :param origin: Tuple containing the origin of the ellipse
    :param major_ax: Major axis length (int)
    :param minor_ax: Minor axis length (int)
    :param angle: angle between major axis and x-axis (clockwise)
    :param resolution: Number of points to approximate the ellipse
    :return: Shapely polygon
    """
    cir = Point(origin).buffer(1, resolution=resolution)
    ell = scale(cir, int(major_ax), int(minor_ax))
    ell = rotate(ell, angle)
    return ell






