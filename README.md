# Beyond Frame: Digital Window

**Beyond Frame** is an interactive digital window project that allows viewers to explore the hidden space beyond the frame of a painting.

Instead of viewing a painting from a fixed perspective, the system tracks the viewer's position in real time and dynamically changes the virtual camera in Unreal Engine. As the viewer moves left, right, up, down, or closer to the display, the perspective changes accordingly, creating the illusion of looking through a real window into a three-dimensional world.

## Concept

Traditional paintings present only what exists inside the frame.

Beyond Frame explores the question:

**"What exists beyond the visible frame?"**

The project reconstructs the space surrounding a painting as a 3D environment and allows viewers to discover areas that would normally remain hidden.

## How It Works

1. Two camera modules capture the viewer.
2. Python and OpenCV detect the viewer's face and calculate the X, Y, and Z (depth) position.
3. The tracking data is transmitted to Unreal Engine through TCP communication.
4. Unreal Engine maps the viewer's position to a virtual camera.
5. The rendered perspective changes in real time according to the viewer's movement.

This creates a motion-parallax effect similar to looking through a physical window.

## Technology

- Unreal Engine 5.5.4
- Python
- OpenCV
- OpenCV DNN Face Detection
- Stereo Camera / Depth Estimation
- TCP Socket Communication
- Blueprint
- 3D Modeling

## Hardware

- OV5693 Camera Modules × 2
- Display
- PC

## System Architecture

Stereo Camera
→ OpenCV Face Tracking
→ XYZ / Depth Calculation
→ TCP Communication
→ Unreal Engine
→ Virtual Camera Movement
→ Real-time Rendering

## My Role

**Team Leader / Technical Development**

- Project planning and technical direction
- Real-time viewer tracking system development
- Stereo-camera-based depth estimation
- Python–Unreal Engine TCP communication
- Unreal Engine camera control and Blueprint implementation
- 3D modeling
- Post-processing system development and management
- Task distribution and project schedule coordination

## Project

Graduation Exhibition Project  
Chung-Ang University, School of Arts & Technology
