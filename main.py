from Classes.Boid import Boid
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from random import random

width = height = 700


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
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
    glClear(GL_COLOR_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if not boidsList:
        for i in range(3):
            boidsList.append(Boid(i + 1, random() * 10, random() * 10))
            #print(boidsList[i])
    center = defineCenter(boidsList)
    #print (center)
    gluLookAt(0.0, 0.0, 0.0,
              center[0], center[1], center[2],
              0.0, 1.0, 0.0)
    #desenhaEixos()
    for b in boidsList:
        b.drawBoid()
        b.moveBoid(center)

    glutSwapBuffers()


def defineCenter(boidsList):
    center = [0, 0, 50]
    for b in boidsList:
        center[0] += b.x
        center[1] += b.y

    center[0] /= len(boidsList)
    center[1] /= len(boidsList)

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
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(40.0, width / height, 1, 100.0)


def createMenu():
    pass


def animate():
    pass


if __name__ == '__main__':
    boidsList = []
    main()
