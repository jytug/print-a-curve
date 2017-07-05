import numpy as np

from triangle import *

# returns a set of 3d triangles, interpolated on a
# square [umin, umax] x [vmin, vmax] in unum * vnum points
def lambda_to_mesh(f1, f2, f3, orient, umin, umax, vmin, vmax,
                   unum=500, vnum=500):
    res = []
    du = (umax - umin) / unum
    dv = (vmax - vmin) / vnum
    def point_up_triangle(iu, iv, offset):
        top = np.array([umin + iu * du, vmin + iv * dv + offset * (dv / 2)])
        bottom_left = np.array([
            umin + (iu - 1) * du,
            min(vmin + iv * dv + offset * (dv / 2) - (dv / 2), vmin),
          ])
        bottom_right = np.array([
            umin + (iu - 1) * du,
            max(vmin + iv * dv + offset * (dv / 2) + (dv / 2), vmax)
          ])
        centroid = (top + bottom_left + bottom_right) / 3
        return np.array(top, bottom_left, bottom_right, orient(tuple(centroid)))

    def point_down_triangle(iu, iv, offset):
        top_right = np.array([
            umin + iu * du,
            max(vmin + iv * dv + offset * (dv / 2), vmax)
          ])
        top_left = np.array([
            umin + iu * du,
            min(vmin + (iv - 1) * dv + offset * (dv / 2), vmin),
          ])
        bottom = np.array([
            umin + (iu - 1) * du,
            vmin + iv * dv + offset * (dv / 2) - (dv / 2)
          ])
        centroid = (top_right + top_left + bottom) / 3
        return np.array(top_right, top_left, bottom, orient(tuple(centroid)))

    for iu in range(1, unum + 1):
        if iu % 2:
            res.append(point_down_triangle(iu, 0, True))
            res.append(point_up_triangle(iu, 0, True))
        else:
            res.append(point_up_triangle(iu, 0, False))
        for iv in range(1, vnum + 1):
            if iv != vnum and iv % 2 == 0:
                res.append(point_up_triangle, iu, iv, iu % 2)
            res.append(point_down_triangle, iu, iv, iu % 2)

def evaluate_point(f1, f2, f3, p):
    u, v = tuple(p)
    return np.array([f1(u, v), f2(u, v), f3(u, v)])

def triangle_centroid_2d(p1, p2, p3):
    return (p1 + p2 + p3) / 3

