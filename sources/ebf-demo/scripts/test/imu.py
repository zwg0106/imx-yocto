# -*- coding: utf-8 -*-

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import socket
import json
from pygame.locals import *

SCREEN_SIZE = (800, 600)

address = ('', 5000)

def resize(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width) / height, 0.001, 10.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    gluLookAt(1.0, 2.0, -5.0,
              0.0, 0.0, 0.0,
              0.0, 1.0, 0.0)

def init():
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_BLEND)
    glEnable(GL_POLYGON_SMOOTH)
    glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)

def setupSocket():

    # setup socket, blocking by default
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(address)

def read_data():
    global ax, ay, az, acx, acy, acz, temp
    ax = ay = az = acx = acy = acz = temp = 0.0

    msg, addr = sock.recvfrom(1024)

    if msg:
        msg.decode()
        data = json.loads(msg)
        #print(data)

        ax, ay ,az = data["filter"]
        acx, acy, acz = data["accel"]
        temp = data["temp"]

def drawText(position, textString):
    font = pygame.font.SysFont("Courier", 18, True)
    textSurface = font.render(textString, True, (255,255,255,255), (0,0,0,255))
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glRasterPos3d(*position)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

def run():

    setupSocket()

    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, HWSURFACE | OPENGL | DOUBLEBUF)
    resize(*SCREEN_SIZE)
    init()
    clock = pygame.time.Clock()
    cube = Cube((0.0, 0.0, 0.0), (.5, .5, .7))
    angle = 0

    while True:
        then = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYUP and event.key == K_ESCAPE:
                return

        read_data()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        text = "pitch: " + str("{0:.1f}".format(ay)) + " roll: " + str("{0:.1f}".format(ax))
        drawText((1, -4, 2), text)

        text = "accx: " + str("{0:.2f}".format(acx)) + " accy: " + str("{0:.2f}".format(acy)) + " accz: " + str(
            "{0:.2f}".format(acz))
        drawText((1, -4.3, 2), text)

        text = "temp: " + str("{0:.1f}".format(temp))
        drawText((1, -4.6, 2), text)

        glColor((1., 1., 1.))
        glLineWidth(1)
        glBegin(GL_LINES)

        for x in range(-20, 22, 2):
            glVertex3f(x / 10., -1, -1)
            glVertex3f(x / 10., -1, 1)

        for x in range(-20, 22, 2):
            glVertex3f(x / 10., -1, 1)
            glVertex3f(x / 10., 1, 1)

        for z in range(-10, 12, 2):
            glVertex3f(-2, -1, z / 10.)
            glVertex3f(2, -1, z / 10.)

        for z in range(-10, 12, 2):
            glVertex3f(-2, -1, z / 10.)
            glVertex3f(-2, 1, z / 10.)

        for z in range(-10, 12, 2):
            glVertex3f(2, -1, z / 10.)
            glVertex3f(2, 1, z / 10.)

        for y in range(-10, 12, 2):
            glVertex3f(-2, y / 10., 1)
            glVertex3f(2, y / 10., 1)

        for y in range(-10, 12, 2):
            glVertex3f(-2, y / 10., 1)
            glVertex3f(-2, y / 10., -1)

        for y in range(-10, 12, 2):
            glVertex3f(2, y / 10., 1)
            glVertex3f(2, y / 10., -1)

        glEnd()

        glPushMatrix()
        glRotate(az, 0, 1, 0)
        glRotate(ay, 1, 0, 0)
        glRotate(ax, 0, 0, 1)

        cube.render()
        glPopMatrix()
        pygame.display.flip()


class Cube(object):

    def __init__(self, position, color):
        self.position = position
        self.color = color

    # Cube information
    num_faces = 6

    vertices = [(-1.0, -0.2, 0.5),
                (1.0, -0.2, 0.5),
                (1.0, 0.2, 0.5),
                (-1.0, 0.2, 0.5),
                (-1.0, -0.2, -0.5),
                (1.0, -0.2, -0.5),
                (1.0, 0.2, -0.5),
                (-1.0, 0.2, -0.5)]

    normals = [(0.0, 0.0, +1.0),  # front
               (0.0, 0.0, -1.0),  # back
               (+1.0, 0.0, 0.0),  # right
               (-1.0, 0.0, 0.0),  # left
               (0.0, +1.0, 0.0),  # top
               (0.0, -1.0, 0.0)]  # bottom

    vertex_indices = [(0, 1, 2, 3),  # front
                      (4, 5, 6, 7),  # back
                      (1, 5, 6, 2),  # right
                      (0, 4, 7, 3),  # left
                      (3, 2, 6, 7),  # top
                      (0, 1, 5, 4)]  # bottom

    def render(self):
        then = pygame.time.get_ticks()
        vertices = self.vertices
        # Draw all 6 faces of the cube
        glBegin(GL_QUADS)

        for face_no in range(self.num_faces):

            if face_no == 1:
                glColor(1.0, 0.0, 0.0)
            else:
                glColor(self.color)

            glNormal3dv(self.normals[face_no])
            v1, v2, v3, v4 = self.vertex_indices[face_no]
            glVertex(vertices[v1])
            glVertex(vertices[v2])
            glVertex(vertices[v3])
            glVertex(vertices[v4])
        glEnd()


if __name__ == "__main__":
    run()