#!/usr/bin/env python

'''
Algoritmo Boids
Trabalho final da disciplina de Computação Gráfica - 2016.2
Universidade Estadual do Ceará (UECE)

Desenvolvido por: Anderson Bezerra Ribeiro
Data: 27/06/2017
'''

from math import sqrt
from random import random

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from Classes.Boid import Boid


def start():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(450, 0)
    glutCreateWindow("Boids")
    glutDisplayFunc(drawBoids)
    glutKeyboardFunc(keyboardEvent)
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
            randomX = random() * 50
            randomY = random() * 50
            boidsList.append(Boid(i + 1, randomX, randomY))
            stepX.append(0.0)
            stepY.append(0.0)
            stepZ.append(0.0)
    center = defineCenter(boidsList)

    gluLookAt(center[0], (center[1] - rotateCamera), (70.0 - rotateCamera),
              center[0], center[1], center[2],
              0.0, 1.0, 0.0)
    desenhaEixos()

    for b in boidsList:
        glPushMatrix()
        desenhaCentro(center)

        glTranslate(center[0], center[1], center[2])
        glScaled(scale, scale, scale)
        glRotated(rotate, 0.0, 0.0, 1.0)
        glTranslate(-center[0], -center[1], -center[2])

        glTranslate(stepX[b.id - 1], stepY[b.id - 1], stepZ[b.id - 1])
        b.drawBoid()
        glPopMatrix()

    glutSwapBuffers()


def defineCenter(boidsList):
    center = [0.0, 0.0, 0.0]
    for b in boidsList:
        center[0] += b.position[0]
        center[1] += b.position[1]
        center[2] += b.position[2]

    center[0] /= len(boidsList)
    center[1] /= len(boidsList)
    center[2] /= len(boidsList)
    return center


def desenhaCentro(center):
    glColor3d(1.0, 0.0, 0.0)
    glPointSize(4)
    glBegin(GL_POINTS)
    glVertex3d(center[0], center[1], center[2])
    glEnd()


def desenhaEixos():
    # Desenha Eixo +Y
    glBegin(GL_LINES)  # RED
    glVertex3d(0.0, 0.0, 0.0)
    glVertex3d(0.0, height / 2, 0.0)
    glEnd()

    # Desenha Eixo -Y
    glColor3d(1.0, 0.8, 0.8)  # RED claro
    glBegin(GL_LINES)
    glVertex3d(0.0, 0.0, 0.0)
    glVertex3d(0.0, -height / 2, 0.0)
    glEnd()

    # Desenha Eixo +X
    glColor3d(0.0, 0.0, 1.0)  # BLUE
    glBegin(GL_LINES)
    glVertex3d(0.0, 0.0, 0.0)
    glVertex3d(width / 2, 0.0, 0.0)
    glEnd()

    # Desenha Eixo -X
    glColor3d(0.8, 0.8, 1.0)  # BLUE claro
    glBegin(GL_LINES)
    glVertex3d(0.0, 0.0, 0.0)
    glVertex3d(-width / 2, 0.0, 0.0)
    glEnd()

    # Desenha Eixo +Z
    glColor3d(0.0, 1.0, 0.0)  # GREEN
    glBegin(GL_LINES)
    glVertex3d(0.0, 0.0, 0.0)
    glVertex3d(0.0, 0.0, width / 2)
    glEnd()

    # Desenha Eixo -Z
    glColor3d(0.8, 1.0, 0.8)  # GREEN claro
    glBegin(GL_LINES)
    glVertex3d(0.0, 0.0, 0.0)
    glVertex3d(0.0, 0.0, -width / 2)
    glEnd()


def keyboardEvent(key, x, y):
    global rotate, rotateCamera, scale, terminateFlag
    if key == b' ':
        rotate += 2
        scale += 0.1
        if scale > 1.5:
            scale -= 0.1
        if rotate > 360:
            rotate -= 360
        if rotateCamera < 45:
            rotateCamera += 1
    elif key == b'c':
        rotateCamera = 0
    elif key == b't':
        terminateFlag = True
    elif key == b'r':
        terminateFlag = False
        rotate = 0.0
        scale = 1.0
        for b in boidsList:
            b.position[0] = b.initialPosition[0]
            b.position[1] = b.initialPosition[1]
            b.position[2] = b.initialPosition[2]
            b.velocity = [0.0, 0.0, 0.0]
    elif key == b'n':
        terminateFlag = False
        rotate = 0.0
        scale = 1.0
        for b in boidsList:
            randomX = random() * 50
            randomY = random() * 50
            b.position[0] = b.initialPosition[0] = randomX
            b.position[1] = b.initialPosition[1] = randomY
            b.position[2] = b.initialPosition[2] = 1.0
            b.velocity = [0.0, 0.0, 0.0]
    glutPostRedisplay()


def initialize():
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(40.0, width / height, -100.0, 2.0)


def createMenu():
    def Window(option):
        global rotate, scale, rotateCamera, terminateFlag
        if option == 0:
            rotateCamera = 0.0
        elif option == 1:
            terminateFlag = False
            rotate = 0.0
            scale = 1.0
            for b in boidsList:
                b.position[0] = b.initialPosition[0]
                b.position[1] = b.initialPosition[1]
                b.position[2] = b.initialPosition[2]
                b.velocity = [0.0, 0.0, 0.0]
        elif option == 2:
            terminateFlag = False
            rotate = 0.0
            scale = 1.0
            for b in boidsList:
                randomX = random() * 50
                randomY = random() * 50
                b.position[0] = b.initialPosition[0] = randomX
                b.position[1] = b.initialPosition[1] = randomY
                b.position[2] = b.initialPosition[2] = 1.0
                b.velocity = [0.0, 0.0, 0.0]
        elif option == 3:
            terminateFlag = True
        glutPostRedisplay()
        return 0

    glutCreateMenu(Window)
    glutAddMenuEntry("Reset Camera - c", 0)
    glutAddMenuEntry("Reset Positions - r", 1)
    glutAddMenuEntry("New Positions - n", 2)
    glutAddMenuEntry("Terminate - t", 3)
    glutAttachMenu(GLUT_RIGHT_BUTTON)


def animate():
    def rule1(self):
        '''Boids try to fly towards the centre of mass of neighbouring boids'''
        pc = [0.0, 0.0, 0.0]
        for b in boidsList:
            if b == self:
                continue
            pc[0] += b.position[0]
            pc[1] += b.position[1]
            pc[2] += b.position[2]
        pc[0] /= len(boidsList) - 1
        pc[1] /= len(boidsList) - 1
        pc[2] /= len(boidsList) - 1

        pc[0] -= self.position[0]
        pc[1] -= self.position[1]
        pc[2] -= self.position[2]

        pc[0] /= 1000
        pc[1] /= 1000
        pc[2] /= 1000

        return pc

    def rule2(self):
        '''Boids try to keep a small distance away from other objects (including other boids)'''
        c = [0.0, 0.0, 0.0]
        for b in boidsList:
            if b == self:
                continue
            t1 = (b.position[0] - self.position[0]) ** 2
            t2 = (b.position[1] - self.position[1]) ** 2
            t3 = (b.position[2] - self.position[2]) ** 2
            distance = sqrt(t1 + t2 + t3)
            if distance < 2.0:
                c[0] -= (b.position[0] - self.position[0]) / 100
                c[1] -= (b.position[1] - self.position[1]) / 100
                c[2] -= (b.position[2] - self.position[2]) / 100
        return c

    def rule3(self):
        '''Boids try to match velocity with near boids'''
        pv = [0.0, 0.0, 0.0]
        for b in boidsList:
            if b == self:
                continue
            pv[0] += b.velocity[0]
            pv[1] += b.velocity[1]
            pv[2] += b.velocity[2]
        pv[0] /= len(boidsList) - 1
        pv[1] /= len(boidsList) - 1
        pv[2] /= len(boidsList) - 1

        pv[0] -= self.velocity[0]
        pv[1] -= self.velocity[1]
        pv[2] -= self.velocity[2]

        pv[0] /= 15
        pv[1] /= 15
        pv[2] /= 15

        return pv

    global stepX, stepY, rotate, terminateFlag

    for b in boidsList:
        v1 = rule1(b)
        v2 = rule2(b)
        v3 = rule3(b)

        b.velocity[0] += v1[0] + v2[0] + v3[0]
        b.velocity[1] += v1[1] + v2[1] + v3[1]
        b.velocity[2] += v1[2] + v2[2] + v3[2]
        b.position[0] += b.velocity[0]
        b.position[1] += b.velocity[1]
        b.position[2] += b.velocity[2]
        stepX[b.id - 1] = b.position[0] - b.initialPosition[0]
        stepY[b.id - 1] = b.position[1] - b.initialPosition[1]
        stepZ[b.id - 1] = b.position[2] - b.initialPosition[2]
    if terminateFlag:
        rotate += 5
        if rotate > 360:
            rotate -= 360
        for b in boidsList:
            b.position[2] -= 2
            if b.position[2] <= -1000:
                b.position[2] -= 9999
                continue
    glutPostRedisplay()


if __name__ == '__main__':
    width = height = 700
    boidsList = []
    stepX = []
    stepY = []
    stepZ = []
    rotate = 0.0
    rotateCamera = 0.0
    scale = 1.0
    terminateFlag = False
    start()
