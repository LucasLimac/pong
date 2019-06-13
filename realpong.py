import pygame
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from math import *
from random import *
from numpy import *


### Colors
WHITE = (255, 255, 255)
BLACK = (0,0,0)

#Score
pygame.font.init()
comic = pygame.font.SysFont('Comic Sans MS', 30)
p1score = 0
p2score = 0


W = 4
H = 2

translate0 = 0
translate1 = 0

#cubo 1
p1x = W/30
p1y = H/2 - ((W/60)**2)/2

#cubo 2
p2x = W/30
p2y = H/2 - ((W/60)**2)/2

vertices = (
    ( p1x,-p1y,-0.3),
    ( p1x, p1y,-0.3),
    (-p1x, p1y,-0.3),
    (-p1x,-p1y,-0.3),
    ( p1x,-p1y, 0.3),
    ( p1x, p1y, 0.3),
    (-p1x,-p1y, 0.3),
    (-p1x, p1y, 0.3),
    )


linhas = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7),
    )
 
faces = (
    (0,1,2,3),
    (3,2,7,6),
    (6,7,5,4),
    (4,5,1,0),
    (1,5,7,2),
    (4,0,3,6)
    )
 
cores = ( (1,0,0),(1,1,0),(0,1,0),(0,1,1),(0,0,1),(1,0,1),(0.5,1,1),(1,0,0.5) )
 
def Cubo():
    glBegin(GL_QUADS)
    i = 0
    for face in faces:
        glColor3fv(cores[i])
        for vertex in face:
            #glColor3fv(cores[vertex])
            glVertex3fv(vertices[vertex])
        i = i+1
    glEnd()
 
    glColor3fv((0,0.5,0))
    glBegin(GL_LINES)
    for linha in linhas:
        for vertice in linha:
            glVertex3fv(vertices[vertice])
    glEnd()



# esfera
teta0 = (-math.pi)/2
tetaF = (math.pi)/2
phi0 = 0
phiF = 2*math.pi
r = 0.3
dphi = math.pi/10
dteta = math.pi/10

def Px(teta):    
    return r*cos(teta)

def Py(teta):
    return r*sin(teta)

def Qx(r2, phi):
    return r2*cos(phi)

def Qz(r2, phi):
    return r2*sin(phi)


def esfera():
    teta = teta0
    phi = phi0
    glBegin(GL_LINES)
    while(tetaF > teta):
        #glVertex3f(Px(teta), Py(teta), 0)
        phi = phi0
        while(phiF > phi):
            P = (Qx(Px(teta), phi), Py(teta), Qz(Px(teta), phi))
            Q = (Qx(Px(teta), phi + dphi), Py(teta), Qz(Px(teta), phi + dphi))
            R = (Qx(Px(teta + dteta), phi), Py(teta + dteta), Qz(Px(teta + dteta), phi))
            S = (Qx(Px(teta + dteta), phi + dphi), Py(teta + dteta), Qz(Px(teta + dteta), phi + dphi))
            
            glVertex3fv(P)
            glVertex3fv(R)
            glVertex3fv(R)
            glVertex3fv(S)
            glVertex3fv(P)
            glVertex3fv(Q)
            glVertex3fv(R)
            glVertex3fv(Q)
            glVertex3fv(Q)
            glVertex3fv(S)


            phi += dphi
        teta += dteta
    glEnd()

def desenha():
    
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    #glRotatef(2,1,3,0)
    glPushMatrix()
    glTranslatef(3.5,translate0,0.0)
    Cubo()
    glPopMatrix()
    glPushMatrix()
    glTranslatef(-4,translate1,0.0)
    Cubo()
    glPopMatrix()
    esfera()
    glutSwapBuffers()
  
def timer(i):
    glutPostRedisplay()
    glutTimerFunc(50,timer,1)
 
def teclaEspecialPressionada(tecla, x, y):
    global translate1             
    if tecla == GLUT_KEY_UP:
        print ("CIMA")
        translate1 -= 0.1
    elif tecla == GLUT_KEY_DOWN:
        print ("BAIXO")
        translate1 += 0.1


def drawscore():
    score = comic.render(str(p1score) + " - " + str(p2score), False, WHITE)
    screen.blit(score, (W/2,30))

def keyPressed(tecla, x, y):
    global translate0

    if tecla == b'w' or tecla == b'W':
        print("W")
        translate0 -= 0.1
    elif tecla == b's' or tecla == b'S':
        print("S")
        translate0 += 0.1   
    

# PROGRAMA PRINCIPAL

### Initialize
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption('Snake ML v.1.0.0')
screen.fill(BLACK)
pygame.display.flip()


glutInit(sys.argv)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH | GLUT_MULTISAMPLE)
glutInitWindowSize(800,600)
glutCreateWindow("CUBO")
glutDisplayFunc(desenha)
glEnable(GL_MULTISAMPLE)
glEnable(GL_DEPTH_TEST)
glClearColor(0.,0.,0.,1.)
gluPerspective(45,800.0/600.0,0.1,50.0)
glTranslatef(0.0,0.0,-12)
#glRotatef(-100,50,1,1)
#glRotatef(90.0, 10.0, 10.0, 90.0)
glRotatef(180.0, 10.0, 10.0, 90.0)
glutTimerFunc(50,timer,1)
drawscore()
glutKeyboardFunc(keyPressed)
glutSpecialFunc(teclaEspecialPressionada)
glutMainLoop() 





    