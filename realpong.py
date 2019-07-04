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


#cubo 1 e 2
p1x = W/30
p1y = H/2 - ((W/60)**2)/2


paddle_width = W/60
paddle_height = paddle_width**2


# esfera
teta0 = (-math.pi)/2
tetaF = (math.pi)/2
phi0 = 0
phiF = 2*math.pi
r = 0.3
dphi = math.pi/10
dteta = math.pi/10
ballX =  0.0
ballY = 0.0
ballXMax = 3.0
ballYMax = 4.0
ballXMin = -3.5
ballYMin = -5.0
xSpeed = 0.1
ySpeed = 0.007

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

texture = []


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






def Px(teta):    
    return r*cos(teta)

def Py(teta):
    return r*sin(teta)

def Qx(r2, phi):
    return r2*cos(phi)

def Qz(r2, phi):
    return r2*sin(phi)


def esfera():
    global ballX, ballXMax, ballXMin, ballY, ballYMax, ballYMin, xSpeed, ySpeed
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
    
    #velocidade
    ballX += xSpeed
    ballY += ySpeed


    #Chechar se passou do limites

    
    

    #lado esquerdo <<----
    if ballX > ballXMax:
        ballX = ballXMax
        xSpeed = -xSpeed
        if abs(ySpeed) < 0.01:
            ySpeed = translate0-ballY 
        if -1 > (translate0-ballY) and  (translate0-ballY) < 1:
            exit() 
    #lado direito -->>>
    elif ballX < ballXMin:
        ballX = ballXMin
        xSpeed = -xSpeed
        if abs(ySpeed) < 0.01:
            ySpeed = translate1-ballY
        if -1 > (translate1-ballY) and  (translate1-ballY) < 1:
            exit()
    #lado inferior 
    if ballY > ballYMax:
        ballY = ballYMax
        ySpeed = -ySpeed
    #lado superior
    elif ballY < ballYMin:
        ballY = ballYMin
        ySpeed = -ySpeed

    glEnd()


def Base():

    glColor3d(0.0,0.0,0.7)
    glBegin(GL_POLYGON)
    #sup direito
    glVertex2d(-4.5,-6.5)
    #superior esquerdo
    glVertex2d(3.8,-5.5)
    #inferior esquerdo
    glVertex2d(3.7,5)
    glVertex2d(-4.3,5)
    glEnd()
    glFlush()

def desenha():
    
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    #glRotatef(2,1,3,0) 
    Base()
    glPushMatrix()
    glTranslatef(3.5,translate0,0.0)
    Cubo()
    glPopMatrix()
    glPushMatrix()
    glTranslatef(-4,translate1,0.0)
    Cubo()
    glPopMatrix()
    #vel da esfera
    glPushMatrix()
    glTranslatef(ballX,ballY,0.0)
    esfera()
    glPopMatrix()
    glutSwapBuffers()
  
def timer(i):
    glutPostRedisplay()
    glutTimerFunc(50,timer,1)
 
def teclaEspecialPressionada(tecla, x, y):
    global translate1      
    print("TRANSLATE 1")
    print((translate1-ballY))
    print("TRANSLATE 0")
    print((translate0-ballY))


    if tecla == GLUT_KEY_UP:
        translate1 -= 0.1
    elif tecla == GLUT_KEY_DOWN:
        translate1 += 0.1



def drawscore():
    score = comic.render(str(p1score) + " - " + str(p2score), False, WHITE)
    screen.blit(score, (300,100))


def keyPressed(tecla, x, y):
    global translate0, translate1

    if tecla == b'w' or tecla == b'W':
        translate0 -= 0.1
    elif tecla == b's' or tecla == b'S':
        translate0 += 0.1 

    

# PROGRAMA PRINCIPAL

### Initialize
screen = pygame.display.set_mode((300, 300))
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

glutKeyboardFunc(keyPressed)
glutSpecialFunc(teclaEspecialPressionada)
glutMainLoop() 





    