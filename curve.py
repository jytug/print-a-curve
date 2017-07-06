import numpy as np
from sympy import lambdify, symbols, sympify

# returns a list of faces and vertices, interpolated on a
# square [umin, umax] x [vmin, vmax] in unum * vnum points
def lambda_to_mesh(f1, f2, f3, umin, umax, vmin, vmax,
                   unum=50, vnum=50):
    vertices = []
    repeated_vertices = {}
    vertex_index = np.zeros([vnum + 1, unum + 1], dtype=np.int16)
    du = (umax - umin) / unum
    dv = (vmax - vmin) / vnum
    for iv in range(vnum + 1):
        for iu in range(unum + 1):
            vertex = evaluate_point(f1, f2, f3,
                [umin + iu * du, vmin + iv * dv])
            try:
                index = vertices.index(vertex)
                repeated_vertices[vertex] = index
            except:
                index = len(vertices)
                vertices.append(vertex)
            vertex_index[iv, iu] = index

    faces = []
    for iv in range(vnum):
        for iu in range(unum):
            faces.append([
                vertex_index[iv    , iu],
                vertex_index[iv + 1, iu],
                vertex_index[iv + 1, iu + 1]
                ])
            faces.append([
                vertex_index[iv    , iu],
                vertex_index[iv    , iu + 1],
                vertex_index[iv + 1, iu + 1]
                ])
    return np.array(vertices), np.array(faces)

def evaluate_point(f1, f2, f3, p):
    u, v = tuple(p)
    return [f1(u, v), f2(u, v), f3(u, v)]

from stl import mesh
# saves a mesh given as a set of vertices and faces, where
# faces are triples of indices in the vertices list
def save_mesh(vertices, faces, filename):
    graph = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            graph.vectors[i][j] = vertices[f[j],:]
    graph.save(filename)

def create_mesh_from_parametrization(variables, s1, s2, s3,
                     normal, umin, umax, vmin, vmax,
                     unum=50, vnum=50, filename="graph.stl"):
    u, v = symbols(variables)
    f1 = lambdify((u, v), sympify(s1), np)
    f2 = lambdify((u, v), sympify(s2), np)
    f3 = lambdify((u, v), sympify(s3), np)
    print(f1(1,1))
    print(f2(1,1))
    print(f3(1,1))
    faces, vertices = lambda_to_mesh(f1, f2, f3, umin, umax, vmin, vmax, unum, vnum)
    save_mesh(faces, vertices, filename)
