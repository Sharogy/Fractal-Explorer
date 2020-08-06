import numpy as np
import scipy.spatial as spt
from matplotlib.path import Path
import Libraries.lineintersect  as li

def GetFirstPoint(dataset):
    imin = np.argmin(dataset[:,1])
    return dataset[imin]

def GetNearestNeighbors(dataset, point, k):
    mytree = spt.cKDTree(dataset,leafsize=10)
    distances, indices = mytree.query(point,k)
    return dataset[indices[:dataset.shape[0]]]

def SortByAngle(kNearestPoints, currentPoint, prevPoint):
    angles = np.zeros(kNearestPoints.shape[0])
    i = 0
    for NearestPoint in kNearestPoints:
        angle = np.arctan2(NearestPoint[1]-currentPoint[1],
                NearestPoint[0]-currentPoint[0]) - \
                np.arctan2(prevPoint[1]-currentPoint[1],
                prevPoint[0]-currentPoint[0])
        angle = np.rad2deg(angle)
        angle = np.mod(angle+360,360)
        angles[i] = angle
        i += 1
    return kNearestPoints[np.argsort(angles)]

def removePoint(dataset, point):
    delmask = [np.logical_or(dataset[:,0]!=point[0],dataset[:,1]!=point[1])]
    newdata = dataset[tuple(delmask)]
    return newdata


def concavehull(dataset, k):
    assert k >= 3, 'k has to be greater or equal to 3.'
    points = np.asarray(dataset)
    firstpoint = GetFirstPoint(points)
    hull = []
    hull.append(firstpoint)
    points = removePoint(points,firstpoint)
    currentPoint = firstpoint
    prevPoint = (currentPoint[0]+10, currentPoint[1])
    step = 2

    while not np.array_equal(firstpoint, currentPoint) or (step == 2) and points.size > 0 :
        if step == 5 :
            points = np.append(points, [firstpoint], axis=0)
        kNearestPoints = GetNearestNeighbors(points, currentPoint, k)
        cPoints = SortByAngle(kNearestPoints, currentPoint, prevPoint)
        its = True
        i = 0
        while its and (i<cPoints.shape[0]):
                i += 1
                if np.array_equal(cPoints[i-1], firstpoint) :
                    lastPoint = 1
                else:
                    lastPoint = 0
                j = 2
                its = False
                while not its and j<np.shape(hull)[0]-lastPoint:
                    its = li.doLinesIntersect(hull[step-1-1], cPoints[i-1],
                            hull[step-1-j-1], hull[step-j-1])
                    j += 1
        if its:
            return concavehull(dataset,k+1)
        prevPoint = currentPoint
        currentPoint = cPoints[i-1]
        hull.append(currentPoint)
        points = removePoint(points,currentPoint)
        step += 1
    p = Path(hull)
    pContained = p.contains_points(dataset, radius=0.0000000001)
    if not pContained.all():
        return concavehull(dataset, k+1)
    return hull

def points_concave(points):
    return np.asarray(points)
