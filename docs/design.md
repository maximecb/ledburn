# Structure and Animations

Animations should probably be implemented as classes with methods such
as `update()` and `pulse()`. The `update` method will get called
regularly (eg: 20 to 30 times a second) so that animations
can keep moving even when there is no beat.

We will need some kind of data structure to represent the topology of the
cube/dome, both in terms of 3D positions, and in terms of connectivity. It
might be useful to have Edge, Vertex and Structure classes (or named tuples).
We could put a function to update the LED states in the Structure class.

The animations will maintain their own internal state, and be able to update
the LED states of the structure based on their own internal logic. The
internal logic of animations may depend on the topology of the structures,
and so animations will need to have access to the structure when instantiated.

# The Simulator

How will the simulator work?

Each animation touches some internal state (tensor of LEDs). This normally
gets periodically pushed to one or more LED controllers. With the simulator,
we instead have a renderer reading and displaying this data instead.
