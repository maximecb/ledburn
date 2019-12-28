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

class BasicStrobe:
    """
    Basic on-off strobe light that doesn't react to the beat
    """

    def __init__(self):
        super().__init__()

    def update(self):
        # TODO
        pass
