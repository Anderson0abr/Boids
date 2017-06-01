from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from random import uniform

class Boid:
    def __init__(self, _id, _x, _y):
        self.id = _id
        self.x = _x
        self.y = _y
        self.z = 50
        self.velocity = [0,0,0]
        self.colorX = uniform(0.0, 0.8)
        self.colorY = uniform(0.0, 0.8)
        self.colorZ = uniform(0.0, 0.8)

    def __str__(self):
        return "ID: {} X: {} Y: {} Z: {}".format(self.id, self.x, self.y, self.z)

    def drawBoid(self):

        if self.id == 1:
            print(self.colorX)
            print(self.colorY)
            print(self.colorZ)
        glColor3f(self.colorX, self.colorY, self.colorZ)
        glTranslate(self.x, self.y, self.z)
        glutWireSphere(2, 20, 20)

    def moveBoid(self, center):
        pass