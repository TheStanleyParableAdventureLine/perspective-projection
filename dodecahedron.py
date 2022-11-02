#Sam Bowles 31/10/2022
#3D -> 2D projection

import turtle
import math

#constants
Phi = (1 + math.sqrt(5)) / 2

#classes for camera, point, edge and projection

class camera:

    xCor = 0
    yCor = 0
    zCor = 0
    fLength = 0
    proj = 0

    def __init__(self, x, y, z, f):
        self.xCor = x
        self.yCor = y
        self.zCor = z
        self.fLength = f

class point:

    xCor = 0
    yCor = 0
    zCor = 0
    proj = 0

    def __init__(self, x, y, z, p):
        self.xCor = x
        self.yCor = y
        self.zCor = z
        self.proj = p

class edge:

    startP = 0
    endP = 0
    proj = 0

    def __init__(self, start, end, p):
        self.startP = start
        self.endP = end
        self.proj = p

class projection:

    points = []
    edges = []
    camera = 0

    drawPen = 0

    def __init__(self, c):
        self.camera = c
        self.camera.proj = self

        self.drawPen = turtle.Turtle()
        self.drawPen.hideturtle()
        self.drawPen.color("black")
        self.drawPen.penup()
        self.drawPen.speed(0)

        #print("projection init")

    def projectPoint(self, point):

        #print("projecting point")
        
        #note: projection does not take rotation into account yet

        pView = [point.xCor - self.camera.xCor, point.yCor - self.camera.yCor, point.zCor - self.camera.zCor]
        #print(pView)

        # x projected = (focal length * x) / (focal length + z)
        # y projected = (focal length * y) / (focal length + z)

        viewProjected = [
            (self.camera.fLength * pView[0]) / (self.camera.fLength + pView[2]),
            (self.camera.fLength * pView[1]) / (self.camera.fLength + pView[2])
            ]
        #print("(" + str(camera.fLength) + " * " + str(pView[0]) + ") / (" + str(camera.fLength) + " + " + str(pView[2]) + ")" + str((camera.fLength * pView[0]) / (camera.fLength + pView[2])))
        #print("(" + str(camera.fLength) + " * " + str(pView[1]) + ") / (" + str(camera.fLength) + " + " + str(pView[2]) + ")" + str((camera.fLength * pView[1]) / (camera.fLength + pView[2])))
        
        #print("viewProjected: " + str(viewProjected))

        return viewProjected

    def draw(self):

            #print("drawing")

            self.drawPen.clear()
            
            for edge in self.edges:

                #project the start and end points to the camera plane
                start = self.projectPoint(edge.startP)
                end = self.projectPoint(edge.endP)

                #use the pen to draw the line
                self.drawPen.goto(start)
                self.drawPen.pendown()
                self.drawPen.goto(end)
                self.drawPen.penup()

            turtle.update()

#method to rotate projections
def rotateY(proj, angle, maxAngle):
    
    radToDegree = math.pi / 720
    angle *= radToDegree
        
    for i in range(0, 4 * maxAngle):
        
        for point in proj.points:
            newX = (point.xCor * math.cos(angle)) - (point.zCor * math.sin(angle))
            newZ = (point.xCor * math.sin(angle)) + (point.zCor * math.cos(angle))
            
            point.xCor = newX
            point.zCor = newZ
        
        proj.draw()

#setup shape projection
#camera and projection must be defined first
shapeCam = camera(0, 200, -600, 300)
shape = projection(shapeCam)


#vertex table for a dodecahedron
shapeVertexTable = [
    #cube                                           index and number of lines connected
    point(-200, 200, 200, shape),                   #left   top     front   0   *
    point(200, 200, 200, shape),                    #right  top     front   1   *
    point(200, 200, -200, shape),                   #right  top     back    2
    point(-200, 200, -200, shape),                  #left   top     back    3
    point(-200, -200, 200, shape),                  #left   bottom  front   4
    point(200, -200, 200, shape),                   #right  bottom  front   5
    point(200, -200, -200, shape),                  #right  bottom  back    6
    point(-200, -200, -200, shape),                 #left   bottom  back    7

    
    #pairs of two
    point(0, 200 * (1 /  Phi),  200 * Phi, shape),  #front  top             8   ***
    point(0, 200 * (-1 / Phi),  200 * Phi, shape),  #front  bottom          9   *
    
    point(0, 200 * (1 /  Phi), 200 * -Phi, shape),  #back   top             10
    point(0, 200 * (-1 / Phi), 200 * -Phi, shape),  #back   bottom          11
    
    
    
    point(200 * Phi,  0, 200 * (1 /  Phi),shape),   #right  front           12
    point(200 * Phi,  0, 200 * (-1 / Phi), shape),  #right  back            13
    
    point(200 * -Phi, 0, 200 * (1 /  Phi), shape),  #left   front           14
    point(200 * -Phi, 0, 200 * (-1 / Phi), shape),  #left   back            15
    
    
    
    point(200 * (1 /  Phi), 200 * Phi,  0, shape),  #top    right           16
    point(200 * (-1 / Phi), 200 * Phi,  0, shape),  #top    left            17
    
    point(200 * (1 /  Phi), 200 * -Phi, 0, shape),  #bottom right           18
    point(200 * (-1 / Phi), 200 * -Phi, 0, shape)   #bottom left            19
    ]

shape.points = shapeVertexTable

#edge table for a dodecahedron
#five edges per pair of two points
shapeEdgeTable = [
    #front pair
    edge(shape.points[8], shape.points[9], shape),
    edge(shape.points[8], shape.points[0], shape),
    edge(shape.points[8], shape.points[1], shape),
    edge(shape.points[9], shape.points[4], shape),
    edge(shape.points[9], shape.points[5], shape),

    #back pair
    edge(shape.points[10], shape.points[11], shape),
    edge(shape.points[10], shape.points[2],  shape),
    edge(shape.points[10], shape.points[3],  shape),
    edge(shape.points[11], shape.points[6],  shape),
    edge(shape.points[11], shape.points[7],  shape),

    #top pair
    edge(shape.points[16], shape.points[17],  shape),
    edge(shape.points[16], shape.points[1],  shape),
    edge(shape.points[16], shape.points[2],  shape),
    edge(shape.points[17], shape.points[0],  shape),
    edge(shape.points[17], shape.points[3],  shape),

    #bottom pair
    edge(shape.points[18], shape.points[19],  shape),
    edge(shape.points[18], shape.points[5],  shape),
    edge(shape.points[18], shape.points[6],  shape),
    edge(shape.points[19], shape.points[4],  shape),
    edge(shape.points[19], shape.points[7],  shape),

    #right pair
    edge(shape.points[12], shape.points[13],  shape),
    edge(shape.points[12], shape.points[1],  shape),
    edge(shape.points[12], shape.points[5],  shape),
    edge(shape.points[13], shape.points[6],  shape),
    edge(shape.points[13], shape.points[2],  shape),

    #left pair
    edge(shape.points[14], shape.points[15],  shape),
    edge(shape.points[14], shape.points[4],  shape),
    edge(shape.points[14], shape.points[0],  shape),
    edge(shape.points[15], shape.points[3],  shape),
    edge(shape.points[15], shape.points[7],  shape)
    ]

shape.edges = shapeEdgeTable

#setup turtle screen for drawing

window = turtle.Screen()
window.title("projection")
window.tracer(0, 0)

shape.draw()
turtle.update()


#counter to use for shape rotation
counter = 0

while True:
    counter += 1
    rotateY(shape, 1, 2)
    shapeCam.yCor = 400 * math.sin((math.pi / 720) * 4 * counter)

