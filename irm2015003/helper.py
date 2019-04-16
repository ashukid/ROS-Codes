import math

def quaternion_to_euler(rot):

    quaternion=(rot[0],rot[1],rot[2],rot[3])
    rot = euler_from_quaternion(quaternion)

    return rot


def distance(x,y):

    temp= math.pow(y[0]-x[0],2)+math.pow(y[1]-x[1],2)
    return math.sqrt(temp)

def calForces(mine,others,goal):

    fxrep=0
    fxatt=0
    fyatt=0
    fyrep=0

    krep=10
    katt=1

    for agents in others:

        d=distance(mine,agents)
        fxrep += krep*(-agents[0]+mine[0])/(d*d)
        fyrep += krep*(-agents[1]+mine[1])/(d*d)

    fxatt += katt*(goal[0]-mine[0])
    fyatt += katt*(goal[1]-mine[1])

    return fxatt+fxrep,fyatt+fyrep


def getGoal(x):
    g=[[0,0],[5,0],[10,0],[10,-5],[5,-5],[0,-5],[0,-10],[5,-10],[10,-10]]
    return g[x]
