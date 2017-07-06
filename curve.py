import numpy as np
import sympy as sp

# returns a list of faces and vertices, interpolated on a
# square [umin, umax] x [vmin, vmax] in unum * vnum points
def lambda_to_mesh(f1, f2, f3, o1, o2, o3,
                   umin, umax, vmin, vmax,
                   unum=50, vnum=50, width=0.5):
    vertices = []           # a list of vertices on the surface
    shifted_vertices = []     # a list of shifted vertices - for width
    repeated_vertices = {}

    vertex_index = np.zeros([vnum + 1, unum + 1], dtype=np.int16)
    du = (umax - umin) / unum
    dv = (vmax - vmin) / vnum
    for iv in range(vnum + 1):
        for iu in range(unum + 1):
            vertex = evaluate_point(f1, f2, f3,
                (umin + iu * du, vmin + iv * dv))
            offset = width * evaluate_point(o1, o2, o3,
                (umin + iu * du, vmin + iv * dv))
            shifted_vertex = vertex + offset
            try:
                index = vertices.index(vertex)
                repeated_vertices[vertex] = index
            except:
                index = len(vertices)
                vertices.append(vertex)
                shifted_vertices.append(shifted_vertex)
            vertex_index[iv, iu] = index
    
    vertices_flat = len(vertices)

    all_vertices = vertices + shifted_vertices

    faces = []
    for iv in range(vnum):
        for iu in range(unum):
            add_flat_triangles(iv, iu, vertex_index, vertices_flat,
                    faces, shifted=False)
            add_flat_triangles(iv, iu, vertex_index, vertices_flat,
                    faces, shifted=True)
    for iv in range(vnum + 1):
        for iu in range(unum + 1):
            add_connecting_triangles(iv, iu, vertex_index, vertices_flat,
                    faces, iv < vnum, iu < unum)

    return np.array(all_vertices), np.array(faces)

def evaluate_point(f1, f2, f3, p):
    u, v = tuple(p)
    return np.array([f1(u, v), f2(u, v), f3(u, v)])

# add all the triangles on the surface, probably shifted
def add_flat_triangles(iv, iu, vertex_index, vertices_flat_count, faces, shifted):
    faces.append(np.array([
        vertex_index[iv    , iu],
        vertex_index[iv + 1, iu],
        vertex_index[iv + 1, iu + 1]
        ]) + shifted * vertices_flat_count)
    faces.append(np.array([
        vertex_index[iv    , iu],
        vertex_index[iv    , iu + 1],
        vertex_index[iv + 1, iu + 1]
        ]) + shifted * vertices_flat_count)

# add all the triangles connecting the two surfaces
def add_connecting_triangles(iv, iu, vertex_index,
        vertices_flat_count, faces, add_up, add_right):
    if add_up:
        faces.append(np.array([
            vertex_index[iv    , iu],
            vertex_index[iv + 1, iu],
            vertex_index[iv + 1, iu] + vertices_flat_count
            ]))
        faces.append(np.array([
            vertex_index[iv    , iu],
            vertex_index[iv    , iu] + vertices_flat_count,
            vertex_index[iv + 1, iu] + vertices_flat_count
            ]))
    if add_right:
        faces.append(np.array([
            vertex_index[iv, iu],
            vertex_index[iv, iu + 1],
            vertex_index[iv, iu + 1] + vertices_flat_count
            ]))
        faces.append(np.array([
            vertex_index[iv, iu    ],
            vertex_index[iv, iu    ] + vertices_flat_count,
            vertex_index[iv, iu + 1] + vertices_flat_count
            ]))
    

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
                     umin, umax, vmin, vmax,
                     unum=50, vnum=50, width=0.5,
                     filename="graph.stl"):
    u, v = sp.symbols(variables)
    sf1, sf2, sf3 = map(sp.sympify, (s1, s2, s3))
    f1, f2, f3 = (sp.lambdify((u, v), sfi) for sfi in (sf1, sf2, sf3))
    o1, o2, o3 = normal(sf1, sf2, sf3, u, v)
    faces, vertices = lambda_to_mesh(f1, f2, f3, o1, o2, o3,
            umin, umax, vmin, vmax, unum, vnum, width=width)
    save_mesh(faces, vertices, filename)

# a symbolic normal to the surface
def normal(symf1, symf2, symf3, u, v):
    der_u = sp.Matrix([[sp.diff(symfi, u) for symfi in [symf1, symf2, symf3]]])
    der_v = sp.Matrix([[sp.diff(symfi, v) for symfi in [symf1, symf2, symf3]]])
    orthogonal = der_u.cross(der_v)
    normal = orthogonal / orthogonal.norm()
    return tuple([sp.lambdify((u, v), n_i) for n_i in normal])
