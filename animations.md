How should we implement animations?

Classes with methods such as `update()` and `pulse()`. The `update` method will get called regularly (eg: 20 to 30 times a second) so that animations can keep moving even when there is no beat.

We will need some kind of data structure to represent the topology of the cube/dome, both in terms of 3D positions, and in terms of connectivity. It might be useful to have Edge, Vertex and Structure classes (or named tuples). We could put a function to update the LED states in the Structure class.

The animations will maintain their own internal state, and be able to update the LED states of the structure based on their own internal logic. The internal logic of animations may depend on the topology of the structures, and so animations will need to have access to the structure when instantiated.
