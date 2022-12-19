"""
Auxiliary functions
 Convex hull based on: https://scipy-cookbook.readthedocs.io/items/Finding_Convex_Hull.html


 JCA
"""

import numpy as np

def read_file(filepath):
    """Read file and return a list of arrays. Each row is a product with
    6 values corresponding to each NIR channel"""
    with open(filepath, 'r') as f:
        lines = f.readlines()

    lines = [l.strip().split(';')[1:] for l in lines]
    data = []
    for l in lines:
        data.append(np.array([float(i) for i in l]))
    return data

def pca_reduction(data, ax=3):
    """Principal Component Analysis. return data reduced to ax dimensions"""
    x = (data-np.mean(data, axis=0)) / np.std(data, axis=0)
    z = np.dot(x.T, x) # Covariance matrix
    eigenvalues, eigenvectors = np.linalg.eig(z)

    variance_explained = []
    for i in eigenvalues:
        variance_explained.append((i/sum(eigenvalues))*100)
            
    print(f'Variance Explained: {variance_explained}')

    projection_matrix = (eigenvectors.T[:][:ax]).T

    return np.dot(x, projection_matrix)



def area_of_triangle(p1, p2, p3):
    '''calculate area of any triangle given co-ordinates of the corners'''
    return np.linalg.norm(np.cross((p2 - p1), (p3 - p1)))/2.

def _angle_to_point(point, centre):
    '''calculate angle in 2-D between points and x axis'''
    delta = point - centre
    res = np.arctan(delta[1] / delta[0])
    if delta[0] < 0:
        res += np.pi
    return res


def convex_hull(points, smidgen=0.0075):
    '''Calculate subset of points that make a convex hull around points

Recursively eliminates points that lie inside two neighbouring points until only convex hull is remaining.

:Parameters:
    points : ndarray (2 x m)
        array of points for which to find hull
    graphic : bool
        use pylab to show progress?
    smidgen : float
        offset for graphic number labels - useful values depend on your data range

:Returns:
    hull_points : ndarray (2 x n)
        convex hull surrounding points
'''

    n_pts = points.shape[1]
    assert(n_pts > 5)
    centre = points.mean(1)
  
    angles = np.apply_along_axis(_angle_to_point, 0, points, centre)
    pts_ord = points[:,angles.argsort()]

    pts = [x[0] for x in zip(pts_ord.transpose())]
    prev_pts = len(pts) + 1
    k = 0
    while prev_pts > n_pts:
        prev_pts = n_pts
        n_pts = len(pts)
        i = -2
        while i < (n_pts - 2):
            Aij = area_of_triangle(centre, pts[i],     pts[(i + 1) % n_pts])
            Ajk = area_of_triangle(centre, pts[(i + 1) % n_pts], \
                                   pts[(i + 2) % n_pts])
            Aik = area_of_triangle(centre, pts[i],     pts[(i + 2) % n_pts])
            if Aij + Ajk < Aik:
                del pts[i+1]
            i += 1
            n_pts = len(pts)
        k += 1
    return np.asarray(pts)