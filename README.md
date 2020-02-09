# ledburn

Awesome animated LED structure project

```
sudo apt-get install libportaudio2

pip3 install numpy sounddevice pyglet
```

## Animations

Animations concepts:
- Concept of edges and vertices
- Each edge has a list of connections at each end
- Animations are classes with an internal state
- update method, and method to signal a beat/pulse

## Ideas

Right now, for mapping the structure, there is a test sequence animation.
This will be ok for the cube, but it might not be good enough for more
complex structure. Something we could do instead, is to connect the LED
strips of the physical structure in any order, and correctly map the edges
in software. This would simplify the assembly process for the physical
structure.

For animation ideas, see the bottom of the `animations.py` source file.
