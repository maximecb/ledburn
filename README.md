# ledburn

Awesome animated LED structure project

```
sudo apt-get install libportaudio2

pip3 install numpy sounddevice
```

## Animations

Idea: we could dynamically change which frequency range we detect activity
pulses in based on what is most active in a given song so far.

Animations concepts:
- Concept of edges and vertices
- Each edge has a list of connections at each end
- Animations are classes with an internal state
- update method, and method to signal a beat

Animation ideas: see the bottom of the animations.py source file.
