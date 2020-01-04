import numpy as np

# Frequency at which animations are updated
UPDATE_RATE = 30

# Time between each update (in seconds)
UPDATE_TIME = 1 / UPDATE_RATE

class Animation:
    """
    Base class for all animations
    """

    def __init__(self):
        pass

    def update(self):
        """
        Called at a regular interval to update the animation
        """

        raise NotImplementedError

    def pulse(self):
        """
        Called when a beat or notable audio change occurs
        """

        pass

class BasicStrobe(Animation):
    """
    Basic strobe light that pulses to the beat
    """

    def __init__(self):
        super().__init__()

    def update(self):
        # TODO
        pass

    def pulse(self):
        pass

# IDEA: selectively flash a subset of the edges in white or red
# Ideally there should be some symmetry in the edge patterns

# Other animation ideas
# - Colored strobe
# - Positional strobe (based on distance to a point)
# - Shooting star, random direction change at vertex
# - Blood drops
# - Point light rotating around the cube, direction changes with the beat
# - Standing waves to the beat
