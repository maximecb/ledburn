import math
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
        print(dist.min(), dist.max())

        print(dist.shape)

        dt = t - self.pulse_time
        brightness = math.pow(0.94, 100 * dt)
        color = np.array([1, 0, 0]) * brightness / (dist*dist)

        print(color.shape)

        self.struct.pixels = color

# TODO: Colored, positional strobe
# Pick a random position inside the cube

# IDEA: selectively flash a subset of the edges in white or red
# Ideally there should be some symmetry in the edge patterns

# Other animation ideas
# - Colored strobe
# - Positional strobe (based on distance to a point)
# - Shooting star, random direction change at vertex
# - Blood drops
# - Point light rotating around the cube, direction changes with the beat
# - Standing waves to the beat
