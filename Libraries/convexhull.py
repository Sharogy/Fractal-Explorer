def orientation (p, q, r):
    ori = (q[1]-p[1]) * (r[0]-q[0]) - (q[0]-p[0]) * (r[1]-q[1])
    if ori == 0:
        return 0
    elif ori > 0:
        return 1
    elif ori < 0:
        return 2


def convexhull(points):
    n = len(points)
    if (n < 3):
        return None
    else: 
        i = 1
        k = 0
        while i < n:
            if (points[i][0]<points[k][0]):
                k = i
            i += 1
        p = k
        q = int()
        hull = list()
        running = True
        while running:      
            hull.append(points[p])
            q = (p+1)%n
            i = 0
            while i < n:
                if (orientation(points[p],points[q],points[i])==2):
                    q = i
                i += 1
            p = q
            if p == k:
                running = False
        return hull






        
    
        


