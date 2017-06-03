from Classes.Boid import Boid
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from random import random
from math import sqrt, pow

width = height = 700


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(450, 0)
    glutCreateWindow("Boids")
    glutDisplayFunc(drawBoids)
    # glutKeyboardFunc(keyboardEvent)
    # glutMouseFunc(mouseEvent)
    initialize()
    createMenu()
    glutIdleFunc(animate)
    glutMainLoop()


def drawBoids():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if not boidsList:
        for i in range(10):
            randomX = random() * 15
            randomY = random() * 15
            boidsList.append(Boid(i + 1, randomX, randomY))
            stepX.append(0)
            stepY.append(0)
    center = defineCenter(boidsList)

    gluLookAt(0.0, 0.0, 70.0,
              center[0], center[1], center[2],
              0.0, 1.0, 0.0)
    desenhaEixos()

    for b in boidsList:
        glPushMatrix()
        glTranslate(stepX[b.id-1], stepY[b.id-1], 0.0)
        b.drawBoid()
        glPopMatrix()

    glutSwapBuffers()


def defineCenter(boidsList):
    center = [0, 0, 0]
    for b in boidsList:
        center[0] += b.position[0]
        center[1] += b.position[1]
        center[2] += b.position[2]

    center[0] /= len(boidsList)
    center[1] /= len(boidsList)
    center[2] /= len(boidsList)

    glColor3d(1.0, 0.0, 0.0)
    glPointSize(4)
    glBegin(GL_POINTS)
    glVertex3d(center[0], center[1], center[2])
    glEnd()

    return center


def desenhaEixos():
    # Desenha Eixo +Y
    glBegin(GL_LINES)  # RED
    glVertex3d(0.0, 0.0, 0.0)
    glVertex3d(0.0, height/2, 0.0)
    glEnd()

    # Desenha Eixo -Y
    glColor3d(1.0, 0.8, 0.8)  # RED claro
    glBegin(GL_LINES)
    glVertex3d(0.0, 0.0, 0.0)
    glVertex3d(0.0, -height/2, 0.0)
    glEnd()

    # Desenha Eixo +X
    glColor3d(0.0, 0.0, 1.0)  # BLUE
    glBegin(GL_LINES)
    glVertex3d(0.0, 0.0, 0.0)
    glVertex3d(width/2, 0.0, 0.0)
    glEnd()

    # Desenha Eixo -X
    glColor3d(0.8, 0.8, 1.0)  # BLUE claro
    glBegin(GL_LINES)
    glVertex3d(0.0, 0.0, 0.0)
    glVertex3d(-width/2, 0.0, 0.0)
    glEnd()

    # Desenha Eixo +Z
    glColor3d(0.0, 1.0, 0.0)  # GREEN
    glBegin(GL_LINES)
    glVertex3d(0.0, 0.0, 0.0)
    glVertex3d(0.0, 0.0, width/2)
    glEnd()

    # Desenha Eixo -Z
    glColor3d(0.8, 1.0, 0.8)  # GREEN claro
    glBegin(GL_LINES)
    glVertex3d(0.0, 0.0, 0.0)
    glVertex3d(0.0, 0.0, -width/2)
    glEnd()


def keyboardEvent():
    pass


def mouseEvent():
    pass


def initialize():
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(40.0, width / height, 1, 100.0)


def createMenu():
    pass


def animate():
    def rule1(self):
        '''Boids try to fly towards the centre of mass of neighbouring boids'''
        pc = [0.0, 0.0]
        for b in boidsList:
            if b == self:
                continue
            pc[0] += b.position[0] + stepX[b.id-1]
            pc[1] += b.position[1] + stepY[b.id-1]
        pc[0] /= len(boidsList) - 1
        pc[1] /= len(boidsList) - 1

        pc[0] -= self.position[0] + stepX[self.id-1]
        pc[1] -= self.position[1] + stepY[self.id-1]

        return pc

    def rule2(self):
        '''Boids try to keep a small distance away from other objects (including other boids)'''
        c = [0.0, 0.0]
        for b in boidsList:
            if b == self:
                continue
            t1 = (b.position[0] - self.position[0])**2
            t2 = (b.position[1] - self.position[1])**2
            distance = sqrt(t1+t2)
            if distance < 3:
                c[0] -= self.position[0] - b.position[0]
                c[1] -= self.position[1] - b.position[1]
        return c

    def rule3(self):
        '''Boids try to match velocity with near boids'''
        pv = [0.0, 0.0]
        for b in boidsList:
            if b == self:
                continue
            pv[0] += b.velocity[0]
            pv[1] += b.velocity[1]
        pv[0] /= len(boidsList) - 1
        pv[1] /= len(boidsList) - 1

        pv[0] -= self.velocity[0]
        pv[1] -= self.velocity[1]

        pv[0] /= 8
        pv[1] /= 8

        return pv

    global stepX, stepY

    for b in boidsList:
        v1 = rule1(b)
        v2 = [0.0, 0.0] #rule2(b)
        v3 = rule3(b)

        b.velocity[0] += v1[0] + v2[0] + v3[0]
        b.velocity[1] += v1[1] + v2[1] + v3[1]

        if 0 <= stepX[b.id -1] < b.velocity[0]:
            stepX[b.id -1] += 0.1
        elif b.velocity[0] < stepX[b.id -1] <= 0:
            stepX[b.id -1] -= 0.1
        if 0 <= stepY[b.id -1] < b.velocity[1]:
            stepY[b.id -1] += 0.1
        elif b.velocity[1] < stepY[b.id -1] <= 0:
            stepY[b.id -1] -= 0.1

    glutPostRedisplay()


if __name__ == '__main__':
    boidsList = []
    stepX = []
    stepY = []
    main()
