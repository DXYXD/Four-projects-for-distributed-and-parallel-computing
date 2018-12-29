from numpy import *
from random import random,seed
import tkinter
from PIL import Image, ImageTk, ImageDraw
from time import time
import threading

seed(323)

G = 1.0 # Gravitational Constant
THRESHOLD = 1 # Number of bodies after which to subdivide Quad
MAXDEPTH = 10
THETA = 0.5 # Barnes-Hut ratio of accuracy
ETA = 0.5 # Softening factor

NUM_CHECKS = 0 # Counter

###################################################
###################################################

class QuadTree:
    """ Class container for for N points stored as a 2D Quadtree """
    root = None
    def __init__(self, bbox, N, theta = THETA):
        self.bbox = bbox
        self.N = N
        self.theta = theta
        self.reset()
    def reset(self):
        self.root = Quad(self.bbox)
    def generate(self):
        # Build up nodes of tree fresh for bodies
        self.reset()
        for x in range(self.N):
            # For each body, add to root
            self.root.addBody(x,0)

    def updateSys(self, dt, n):
        self.calculateBodyAccelsT(n)
        global VEL,POS
        # midpoint method
        VEL += ACC * dt / 2
        POS += VEL * dt
        # print(POS)
    def calculateBodyAccelsT(self, n):
        # Update ACC table based on current POS
        threadi = []
        for i in range(n):
            if i != n - 1:
                amount = N // n
            else:
                amount = N - (n - 1) * (N // n)
            t = threading.Thread(target = self.calculateBodyAccels, args = (i, amount, n, ))
            threadi.append(t)
            t.start()
        for thread_ in threadi:
            t.join()

    def calculateBodyAccels(self, indx, amount, n):
        dis = N // n
        for k in range(indx * dis, indx * dis + amount):
            ACC[k] = self.calculateBodyAccel(k)
    def calculateBodyAccel(self, bodI):
        return self.calculateBodyAccelR(bodI, self.root)

    def calculateBodyAccelR(self, bodI, node):
        # Calculate acceleration on body I
        # key difference is that body is ignored in calculations
        acc = zeros(2,dtype=float)
        if (node.leaf):
            # print "Leaf"
            # Leaf node, no children
            for k in node.bods:
                if k != bodI: # Skip same body
                    acc += getForce( POS[bodI] ,1.0,POS[k],MASS[k])
        else:
            s = max( node.bbox.sideLength )
            d = node.center - POS[bodI]
            r = sqrt(d.dot(d))
            if (r > 0 and s/r < self.theta):
                # Far enough to do approximation
                acc += getForce( POS[bodI] ,1.0, node.com, node.mass)
            else:
                # Too close to approximate, recurse down tree
                for k in range(4):
                    if node.children[k] != None:
                        acc += self.calculateBodyAccelR(bodI, node.children[k])
        return acc

    def calculateAccel(self, p):
        return self.calculateAccelR(p, self.root)
    def calculateAccelR(self, p, node):
        # Calculate acceleration on point p = [x,y]
        acc = zeros(2,dtype=float)
        if (node.leaf):
            # print "Leaf"
            # Leaf node, no children
            for k in node.bods:
                acc += getForce(p,1.0,POS[k],MASS[k])
        else:
            s = max( node.bbox.sideLength )
            d = node.center - p
            r = sqrt(d.dot(d))
            if (r > 0 and s/r < self.theta):
                # Far enough to do approximation
                acc += getForce(p,1.0, node.com, node.mass)
            else:
                # Too close to approximate, recurse down tree
                for k in range(4):
                    if node.children[k] != None:
                        acc += self.calculateAccelR(p, node.children[k])
        return acc

    def __repr__(self):
        return self.__str__()
    def __str__(self):
        return self.root.__str__()
        

def getForce(p1,m1,p2,m2):
    # need to d
    global NUM_CHECKS
    d = p2-p1
    r = sqrt(d.dot(d)) + ETA
    f = array( d * G*m1*m2 / r**3 )
    NUM_CHECKS += 1
    return f


class Quad:
    """ A rectangle of space, contains point bodies """
    def __init__(self,bbox,bod = None,depth=0):
        self.bbox = bbox
        self.center = bbox.center
        self.leaf = True # Whether is a parent or not
        self.depth = depth
        if bod != None: # want to capture 0 int also
            self.setToBody(bod)
            self.N = 1
        else:
            self.bods = []
            self.mass = 0.
            self.com = array([0,0], dtype=float)
            self.N = 0
            
        self.children = [None]*4 # top-left,top-right,bot-left,bot-right

    def addBody(self, idx, depth):
        # Recurse if you have a body or you have children
        if len(self.bods) > 0 or not self.leaf:
            # Not empty
            if (depth >= MAXDEPTH):
                self.bods.append(idx)
            else:
                # Subdivide tree
                subBods = [idx] # bodies to add to children
                if len(self.bods) > 0:
                    # if node has no children yet, move own body down to child
                    subBods.append(self.bods[0])
                    self.bods = []

                for bod in subBods:
                    quadIdx = self.getQuadIndex(bod)
                    if self.children[quadIdx]:
                        # child exists, recursively call 
                        self.children[quadIdx].addBody(bod,depth+1)
                    else:
                        # create child
                        subBBox = self.bbox.getSubQuad(quadIdx)
                        self.children[quadIdx] = Quad(subBBox, bod,depth+1)

                self.leaf = False

            # Update CoM
            bodyMass = MASS[idx]
            self.com   = (self.com * self.mass + POS[idx] * bodyMass) / (self.mass + bodyMass)
            self.mass += bodyMass
        else:
            # Empty Quad, add body directly
            self.setToBody(idx)

        self.N += 1 # Number of bodies incremented
    
    def updateCOM(self):
        if self.leaf:
            self.mass = array(map(lambda x: MASS[x], self.bods)).sum()
            self.com = array(map(lambda x: POS[x]*MASS[x], self.bods)).sum(0) / self.mass
        else:
            self.mass = array(map(lambda child: child.mass if child else 0, self.children)).sum()
            self.com   = array(map(lambda child: child.mass*child.com if child else zeros(2), self.children)).sum(0) / self.mass
        
    def setToBody(self,idx):
        self.bods = [idx]
        self.mass = float( MASS[idx].copy() )
        self.com  = POS[idx].copy()

    def getQuadIndex(self,idx):
        return self.bbox.getQuadIdx(POS[idx])
        
    def __repr__(self):
        return self.__str__()
    def __str__(self):        
        if len(self.bods) > 0:
            bodstring = str(self.bods)
        else:
            bodstring = "PARENT"
        if any(self.children):
            childCount = "C:%g," % sum(map(lambda x: 1 if x else 0, self.children))
            childStr = "\n"
            for x in range(4):
                childStr += ("-"*(self.depth+1))+str(x+1)+" "
                if self.children[x]:
                    childStr += str(self.children[x])
                if x < 3: 
                    childStr += "\n"
        else:
            childCount = ""
            childStr = ""
        return "D%g{N:%g,M:%g,%sCOM:%s,B:%s}%s" % (self.depth,self.N,round(self.mass,2),childCount,self.com.round(2),bodstring,childStr)


class BoundingBox:
    def __init__(self,box,dim=2):
        assert(dim*2 == len(box))
        self.box = array(box,dtype=float)
        self.center = array( [(self.box[2]+self.box[0])/2, (self.box[3]+self.box[1])/2] , dtype=float)
        self.dim = dim
        self.sideLength = self.max() - self.min()

    def max(self):
        return self.box[self.dim:]
    def min(self):
        return self.box[:self.dim]
    def inside(self,p):
        # p = [x,y]
        if any(p < self.min()) or any(p > self.max()):
            return False
        else:
            return True
    def getQuadIdx(self,p):
        # y goes up
        # 0 1
        # 2 3
        if p[0] > self.center[0]: # x > mid
            if p[1] > self.center[1]: # y > mid
                return 1
            else:
                return 3
        else:
            if p[1] > self.center[1]: # y > mid
                return 0
            else:
                return 2
    def getSubQuad(self,idx):
        b = array([None,None,None,None])
        if idx % 2 == 0:
            # Even #, left half
            b[::2] = [self.box[0], self.center[0]] # x - midx
        else:
            b[::2] = [self.center[0], self.box[2]] # midx - x2
        if idx < 2:
            # Upper half (0 1)
            b[1::2] = [self.center[1], self.box[3]] # midy - y2
        else:
            b[1::2] = [self.box[1], self.center[1]] # y - midy
        return BoundingBox(b,self.dim)

    def __repr__(self):
        return self.__str__()
    def __str__(self):
        return "<<%g,%g,%g,%g>>" % (self.box[0],self.box[1],self.box[2],self.box[3])


##############################################
##############################################

def drawAccelGrid(drawPtr, gridSize):
    # Draw accel grid
    MAX_ACC = 1
    boundmax = max(BOUNDS.max())
    for x in range(gridSize):
        for y in range(gridSize):
            p = array([x+0.5,y+0.5],dtype=float) * BOUNDS.sideLength / gridSize
            acc = sys.calculateAccel(p)
            mag = sqrt((acc*acc).sum())
            acc *= (boundmax/gridSize)/mag # Unit value
            drawLine(drawPtr, p, p+acc, (255,int(255*mag/MAX_ACC),0) )

def drawBodies(drawPtr):
    for x in range(N):
        if BOUNDS.inside(POS[x]):
            p = convertPos(POS[x])
            r = MASS[x]*5
            drawPtr.ellipse( join(p-r,p+r) , fill = (0,0,0) )

def drawVels(drawPtr):
    for x in range(N):
        if BOUNDS.inside(POS[x]):
            drawLine(drawPtr, POS[x], POS[x]+VEL[x], (0,0,255) )

def drawAccs(drawPtr):
    for x in range(N):
        if BOUNDS.inside(POS[x]):
            drawLine(drawPtr, POS[x], POS[x]+ACC[x], (255,0,0) )

def join(p1,p2):
    return ([p1[0],p1[1],p2[0],p2[1]])

def drawBBOX(drawPtr, node):
    if node.depth == 0:
        drawCross(drawPtr,node.com)
    p = join(convertPos(node.bbox.min()),
             convertPos(node.bbox.max()))
    drawPtr.rectangle( p , outline=(0,0,255) )

def drawLine(drawPtr, p1, p2, color):
    drawPtr.line( join( convertPos(p1) , convertPos(p2) ), fill=color )

CROSS_SIZE = 20 # pixels
def drawCross(drawPtr, p):
    p = convertPos(p)
    drawPtr.line( (p[0]-CROSS_SIZE,p[1],p[0]+CROSS_SIZE,p[1]), fill=(0,255,0) )
    drawPtr.line( (p[0],p[1]-CROSS_SIZE,p[0],p[1]+CROSS_SIZE), fill=(0,255,0) )

def drawQuadTree(drawPtr, qtree):
    drawQuadTreeR(drawPtr, qtree.root)
def drawQuadTreeR(drawPtr,node):
    drawBBOX(drawPtr,node)
    for child in node.children:
        if child != None:
            drawQuadTreeR(drawPtr,child)

def convertPos(p):
    # From BOUNDS to IMAGE_SIZE and list format [x,y]
    # p = (x,y) -> [ix, iy]
    c = trunc( ( p - BOUNDS.min()) / (BOUNDS.max()-BOUNDS.min()) * array(IMAGE_SIZE) ).tolist()
    c[1] = IMAGE_SIZE[1] - c[1] # flip y axis
    return c

##############################################
##############################################

def task_update():
    global T,boo
    print("Update t=%g-%g" % (T,T+DT))
    T += DT
    ts = time()
    sys.generate()
    print("QUADTREE: %gms" % ((time()-ts)*1000))


    im = Image.new('RGB', IMAGE_SIZE, (255,255,255))
    draw = ImageDraw.Draw(im)

    ts = time()
    drawQuadTree(draw,sys)
    drawBodies(draw)
    print("DRAW: %gms" % ((time()-ts)*1000))
    ts = time()
    sys.updateSys(DT, numthread)
    print("SYSUPD: %gms" % ((time()-ts)*1000))
    
    ts = time()
    boo = ImageTk.PhotoImage(im)
    label_image.config(image=boo)
    label_image.pack()
    print("SHOWING: %gms" % ((time()-ts)*1000))
    root.after(10,task_update)

    print()

def button_click_exit_mainloop (event):
    event.widget.quit() # this will cause mainloop to unblock.

##############################################
##############################################

N = 100
BOUNDS = BoundingBox([0,0,10,10])

IMAGE_SIZE = (600,400)
GRID_SIZE = 10
CIRCLE_RADIUS = 10 # radius in pixels
numthread = 4

# Global variables
# 2D Position
MASS = zeros(N,dtype=float)
POS = zeros((N,2),dtype=float)
VEL = zeros((N,2),dtype=float)
ACC = zeros((N,2),dtype=float)
for i in range(N):
    MASS[i] = 1 #random()*3
    POS[i] = BOUNDS.min() + array([random(),random()])*BOUNDS.sideLength

sys = QuadTree(BOUNDS, N)

DT = 0.1
T = 0

root = tkinter.Tk()
root.bind("<Button>", button_click_exit_mainloop)
label_image = tkinter.Label(root)


print("Update t=%d-%d" % (T,T+DT))
T += DT
print("Updating system by dt=%g" % DT)
sys.generate()
print("Finished generating quad tree")
sys.updateSys(DT, numthread)
print("Done updating System.")

im = Image.new('RGB', IMAGE_SIZE, (255,255,255))
draw = ImageDraw.Draw(im)

drawQuadTree(draw,sys)
drawBodies(draw)
drawVels(draw)
drawAccs(draw)

print("Number of force calcs: %g" % NUM_CHECKS)
boo = None

task_update()
print("Here")
root.mainloop()

print("Done.")
