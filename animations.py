import math
import random
import numpy as np

# Frequency at which animations are updated
UPDATE_RATE = 30

# Time between each update (in seconds)
UPDATE_TIME = 1 / UPDATE_RATE

class Animation:
    """
    Base class for all animations
    """

    def __init__(self, struct):
        # 3D structure on which the animation will be mapped
        self.struct = struct

    def pulse(self, t):
        """
        Called when a beat or notable audio change occurs
        Note: some animations may choose not to implement this method
        """
        pass

    def update(self, t):
        """
        Called at a regular interval to update the animation
        """
        raise NotImplementedError

class TestSequence(Animation):
    """
    Test sequence. This is used to help us connect the
    LED strips in the correct order on the physical cube.
    """

    def __init__(self, struct):
        super().__init__(struct)

        self.edge_idx = 0

        self.led_idx = 0

    def update(self, t):
        # TODO: flash on first segment
        # We can add this later

        # Should have directional movement
        # Start with just going from one edge to another and iterating through the LEDs,
        # in order

        edge = self.struct.edges[self.edge_idx]

        self.led_idx += 1

        if self.led_idx >= edge.num_leds:
            self.edge_idx = (self.edge_idx + 1) % len(self.struct.edges)
            self.led_idx = 0

        self.struct.pixels[:, :] = 0
        self.struct.pixels[self.edge_idx, self.led_idx, 0] = 1

class BasicStrobe(Animation):
    """
    Basic strobe light that pulses to the beat
    """

    def __init__(self, struct):
        super().__init__(struct)

        self.pulse_time = 0

    def pulse(self, t):
        self.pulse_time = t

    def update(self, t):
        dt = t - self.pulse_time
        brightness = math.pow(0.94, 100 * dt)
        color = np.array([1, 1, 1]) * brightness
        self.struct.pixels[:, :] = color

class PosiStrobe(Animation):
    """
    Simple positional strobe effect
    """

    def __init__(self, struct):
        super().__init__(struct)

        self.pulse_time = 0
        self.pos = np.array([0, 0, 0])

    def pulse(self, t):
        self.pulse_time = t

        # TODO: method to compute min/max cube extents or
        # sample point around structure
        self.pos = np.random.uniform(
            np.array([-0.5, -0.5, -0.5]),
            np.array([0.5, 0.5, 0.5])
        )

    def update(self, t):
        dist = self.struct.poss - self.pos
        dist = np.linalg.norm(dist, axis=-1)
        dist = np.expand_dims(dist, -1)

        dt = t - self.pulse_time
        brightness = math.pow(0.94, 100 * dt)
        color = np.array([1, 0, 0]) * brightness / (dist*dist)

        self.struct.pixels = color

class TestAnimation(Animation):

    def __init__(self, struct):
        super().__init__(struct)

        self.pulse_time = 0
        self.pos = np.random.uniform(
            np.array([-0.5, -0.5, -0.5]),
            np.array([0.5, 0.5, 0.5])
        )

    def pulse(self, t):
        self.pulse_time = t
        green = np.array([0,1,0])
        blue = np.array([0,0,1])
        red = np.array([1,0,0])
        yellow = np.array([1,1,0])
        cyan = np.array([0,1,1])
        magenta = np.array([1,0,1])
        colors = [blue, cyan, magenta]
        color = colors[np.random.randint(0,4)]
        self.struct.pixels[:,:] = color


    def update(self, t):
        dist = self.struct.poss - self.pos
        dist = np.linalg.norm(dist, axis=-1)
        dist = np.expand_dims(dist, -1)
        dt = t - self.pulse_time
        brightness = math.pow(0.94, 100 * dt)
        color = np.array([.5,1,1]) * brightness

        self.struct.pixels[:,:] *= brightness


class EdgeStrobe(Animation):
    """
    Randomly flash one edge of the cube at a time
    """

    def __init__(self, struct):
        super().__init__(struct)

        self.cur_edge = 0
        self.pulse_time = 0

    def pulse(self, t):
        self.cur_edge = np.random.randint(0, self.struct.num_edges)
        self.pulse_time = t
        self.struct.pixels[:, :, :] = 0

    def update(self, t):
        dt = t - self.pulse_time
        brightness = math.pow(0.94, 100 * dt)
        color = np.array([1, 1, 1]) * brightness
        self.struct.pixels[self.cur_edge, :] = color

# IDEA: selectively flash a subset of the edges in white or red
# Ideally there should be some symmetry in the edge patterns
# IDEA: multi-flash pattern that changes to the beat

# Other animation ideas
# - Colored strobe
# - Positional strobe (based on distance to a point)
# - Shooting star, random direction change at vertex
# - Blood drops
# - Point light rotating around the cube, direction changes with the beat
# - Standing waves to the beat

def reg_animations():
    import inspect

    animations = []

    global_vars = globals()

    # Iterate through global names
    for global_name in sorted(list(global_vars.keys())):
        anim_class = global_vars[global_name]

        if not inspect.isclass(anim_class):
            continue

        if not issubclass(anim_class, Animation):
            continue

        if anim_class is Animation or anim_class is TestSequence:
            continue

        animations.append(anim_class)

    return animations

def random_animation(struct):
    anim_class = random.choice(animations)
    return anim_class(struct)

# List of animations we can pick from
animations = reg_animations()
