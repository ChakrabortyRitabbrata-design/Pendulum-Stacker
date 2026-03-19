# Pendulum Stacker

A gravity and physics-based block stacking game written in Python using `pygame` and `pymunk`.

## Overview
Control the top anchor of the pendulum crane using the `LEFT` and `RIGHT` arrows while compensating for dynamic randomized wind forces. Press `SPACE` to drop blocks and attempt to stack them without knocking your tower over!

## Features
*   **Realistic Physics:** Inherited velocity and strict gravity/friction modeling via the `pymunk` engine.
*   **Modern Pygame UI:** 
    * Native Glassmorphism overlays and frosted panels.
    * Real-time Particle trails and explosion effects.
    * Glowing semi-transparent Neon colors.
    * Dynamic starry and gradient background shading.

## Quick Start
You can launch the complete standalone version of the game using the executable:
`dist/PendulumStacker.exe`

Or, simply run it from source using standard Python:
```bash
pip install pygame pymunk
python main.py
```
