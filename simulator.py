import time
import argparse
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

anim = animations.BasicStrobe()

# Time when the last beat occurred
last_beat = 0

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
        4, # Camera z
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

    """
    glBegin(GL_TRIANGLES)
    glVertex3f(0, 0, -4)
    glVertex3f(1, 1, -4)
    glVertex3f(1, 0, -4)
    glEnd()
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

def update(dt):
    global last_beat

    t = time.time()

    if t - last_beat > 0.5:
        last_beat = t
        anim.pulse()
        print('Pulse!')

    anim.update()


# TODO: function in the structure to instantiate a numpy array of colors
# should have dimensions (edges, leds, channels)
# we should operate in floating-point format until we need to draw

# TODO: start by just drawing OpenGL points for the LEDs



pyglet.clock.schedule_interval(update, animations.UPDATE_TIME)

pyglet.app.run()
