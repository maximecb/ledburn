#!/usr/bin/env python3

import time
import argparse
import math
import pyglet
from pyglet.gl import *
from pyglet.window import key
from pyglet.window import mouse
import structure
import animations

window = pyglet.window.Window(
    width=800,
    height=600,
    caption='LEDBurn Simulator'
)

#anim = animations.BasicStrobe(structure.cube)
#anim = animations.PosiStrobe(structure.cube)
anim = animations.TestSequence(structure.cube)

# Time when the next beat should occur
next_beat = 0

# Number of beats so far
num_beats = 0

@window.event
def on_key_press(symbol, modifiers):
    print('A key was pressed')

    if symbol == key.LEFT:
        print('The left arrow key was pressed.')
    if symbol == key.ENTER:
        print('The enter key was pressed.')

@window.event
def on_draw():

    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glViewport(0, 0, window.width, window.height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(65, window.width / float(window.height), 0.05, 80)

    glMatrixMode(GL_MODELVIEW)

    glLoadIdentity()
    gluLookAt(
        0, # Camera x
        1, # Camera y
        2, # Camera z
        0, # Look at x
        0, # Look at y
        0, # Look at z
        0,
        1,
        0
    )

    draw_struct(structure.cube)

def draw_struct(struct):
    """
    Draw a structure and its LEDs
    Note: we define the drawing code here because we don't want to import
    the pyglet dependencies in the rest of the code.
    """

    glColor3f(1, 1, 1)
    glPointSize(5)
    glBegin(GL_POINTS)
    for vert in struct.verts:
        glVertex3f(*vert.pos)
    glEnd(GL_POINTS)

    glColor3f(0.2, 0.2, 0.2)
    glBegin(GL_LINES)
    for edge in struct.edges:
        p0 = edge.start.pos
        p1 = edge.end.pos
        glVertex3f(*p0)
        glVertex3f(*p1)
    glEnd(GL_LINES)

    struct = structure.cube
    pixels = struct.pixels
    poss = struct.poss

    # TODO: draw colored OpenGL points for the LEDs
    glColor3f(1, 1, 1)
    glPointSize(2)
    glBegin(GL_POINTS)

    for edge_idx in range(pixels.shape[0]):
        for led_idx in range(pixels.shape[1]):
            c = pixels[edge_idx, led_idx]
            p = poss[edge_idx, led_idx]
            glColor3f(*c)
            glVertex3f(*p)

    glEnd(GL_POINTS)


def update(dt):
    global anim
    global next_beat
    global num_beats

    # Get the current time in seconds
    t = time.time()

    # Slowly vary the tempo over time so we can test animations more robustly
    bpm = 120 + 30 * math.sin(t / 40)
    beats_per_sec = bpm / 60
    secs_per_beat = 1 / beats_per_sec

    # If it's time for the next beat
    if t > next_beat:
        if num_beats % 5 < 2:
            next_beat = t + secs_per_beat / 2
        else:
            next_beat = t + secs_per_beat

        anim.pulse(t)
        print('Pulse! #{} tempo={:.1f} t={:.1f}'.format(num_beats, bpm, t))
        num_beats += 1

    anim.update(t)

    # Randomly pick the next animation
    if num_beats % 20 == 0:
        anim = animations.random_animation(structure.cube)

pyglet.clock.schedule_interval(update, animations.UPDATE_TIME)

pyglet.app.run()
