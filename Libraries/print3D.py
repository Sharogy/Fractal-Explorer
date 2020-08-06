import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def P3D():
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    xcoord = []
    ycoord = []

    with open ("Docs\quivercoord.txt", "r") as fp:
        coordlist = fp.readlines()
    for i in range (0, len(coordlist)):
        coord = coordlist[i]
        newcoord = coord.split(", ")
            
        xcoord.append(float(newcoord[0]))
        ycoord.append(float(newcoord[1]))

    ax.set_xlim3d(min(xcoord)-25, max(xcoord)+25)
    ax.set_ylim3d(min(ycoord)-25, max(ycoord)+25)
    ax.set_zlim3d(0, 100)

    for i in range (0,len(xcoord)-1):
        zincrement = 100/len(xcoord)
        ax.quiver3D(xcoord[i],ycoord[i],zincrement*i, xcoord[i+1]-xcoord[i] , ycoord[i+1]-ycoord[i] , zincrement, length=12, normalize = True)
        #ax.quiver3D(xcoord[i],ycoord[i],0, xcoord[i+1]-xcoord[i] , ycoord[i+1]-ycoord[i] , 0, length=12, normalize = True)
    plt.show()

