import argparse
import pyglet
from pyglet.gl import *
from pyglet.window import key
from pyglet.window import mouse
import structure
import animations


def draw_struct(struct):
    """
    Draw a structure and its LEDs
    """

    pass





window = pyglet.window.Window(
    width=800,
    height=600,
    caption='LEDBurn Simulator'
)

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
        2, # Camera y
        0, # Camera z
        0, # Look at x
        0, # Look at y
        -4, # Look at z
        0,
        1,
        0
    )





    glBegin(GL_TRIANGLES)
    glVertex3f(0, 0, -4)
    glVertex3f(1, 1, -4)
    glVertex3f(1, 0, -4)
    glEnd()





def update(dt):
    pass

pyglet.clock.schedule_interval(update, animations.UPDATE_TIME)

pyglet.app.run()
