#Sam Bowles 31/10/2022
#3D -> 2D projection

import turtle
import math


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

#setup cube projection
#camera and projection must be defined first
cubeCam = camera(0, 0, -400, 300)
cube = projection(cubeCam)

cubeVertexTable = [
        #points for top face
        point(-200, 200, -200, cube),   #left  top front        index 0
        point(-200, 200, 200, cube),   #left  top back         index 1
        point(200, 200, 200, cube),    #right top back         index 2
        point(200, 200, -200, cube),    #right top front        index 3

        #points for bottom face
        point(-200, -200, -200, cube),  #left  bottom front     index 4
        point(-200, -200, 200, cube),  #left  bottom back      index 5
        point(200, -200, 200, cube),   #right bottom back      index 6
        point(200, -200, -200, cube)    #right bottom front     index 7
    ]

cube.points = cubeVertexTable

cubeEdgeTable = [
    #edges for top face
    edge(cube.points[3], cube.points[0], cube), #right top front to left top front  3 -> 0
    edge(cube.points[0], cube.points[1], cube), #left top front to left top back    0 -> 1
    edge(cube.points[1], cube.points[2], cube), #left top back to right top back    1 -> 2
    edge(cube.points[2], cube.points[3], cube), #right top back to right top front  2 -> 3

    #edges for bottom face
    edge(cube.points[7], cube.points[4], cube), #right bottom front to left bottom front    7 -> 4
    edge(cube.points[4], cube.points[5], cube), #left bottom front to left bottom back      4 -> 5
    edge(cube.points[5], cube.points[6], cube), #left bottom back to right bottom back      5 -> 6
    edge(cube.points[6], cube.points[7], cube), #right bottom back to right bottom front    6 -> 7

    #'struts' to connect top and bottom
    edge(cube.points[3], cube.points[7], cube), #right top front to right bottom front      3 -> 7
    edge(cube.points[0], cube.points[4], cube), #left top front to left bottom front        0 -> 4
    edge(cube.points[1], cube.points[5], cube), #left top back to left bottom back          1 -> 5
    edge(cube.points[2], cube.points[6], cube)  #right top back to right bottom back        2 -> 6
    ]

cube.edges = cubeEdgeTable


#setup turtle screen for drawing

window = turtle.Screen()
window.title("projection")
window.tracer(0, 0)

cube.draw()
turtle.update()

#counter to use for cube rotation
counter = 0

while True:
    counter += 1
    rotateY(cube, 1, 2)
    cubeCam.yCor = 400 * math.sin((math.pi / 180) * 1 * counter)
