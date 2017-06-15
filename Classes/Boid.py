from OpenGL.GLUT import *
from OpenGL.GL import *
from random import uniform


class Boid:
    def __init__(self, _id, _x, _y):
        self.id = _id
        self.initialPosition = [_x, _y, 1.0]
        self.position = self.initialPosition[:]
        self.velocity = [0.0, 0.0, 0.0]
        self.colorX = uniform(0.0, 0.8)
        self.colorY = uniform(0.0, 0.8)
        self.colorZ = uniform(0.0, 0.8)

    def __str__(self):
        return "ID: {} X: {} Y: {} Z: {}".format(self.id, self.position[0], self.position[1], self.position[2])

    def drawBoid(self):
        glColor3f(self.colorX, self.colorY, self.colorZ)
        glTranslate(self.initialPosition[0], self.initialPosition[1], self.initialPosition[2])
        glutWireSphere(1, 10, 10)
