# Description
The provided code simulates a dynamic robot navigation system in a grid environment with moving obstacles using Python and Pygame. The robot uses the A pathfinding algorithm* to find an optimal path to its destination while avoiding obstacles that move randomly at set intervals.

# Features
Grid Environment: The simulation operates on a 10x10 grid where each cell represents a navigable area.
A Pathfinding Algorithm*: The robot dynamically calculates the shortest path to the destination while avoiding obstacles.
Dynamic Obstacles: Obstacles move randomly within the grid at regular intervals, adding complexity to the navigation.

# Visualization:
The robot is represented as a green square.
The destination is marked in red.
Obstacles are represented as black squares.
The robot’s planned path is visualized with yellow squares.

# Interactive Setup:
Users can set the robot's start position and the destination by clicking on the grid.

# How It Works
Grid Setup: A 10x10 grid is drawn on the screen, with each cell sized at 60x60 pixels.
Obstacle Generation: 30 random static obstacles are initially placed on the grid.
Obstacle Movement: Obstacles move every 3 seconds to a random adjacent cell, ensuring they do not overlap with the robot or the destination.
Robot Navigation: The robot calculates its path to the destination using the A* algorithm, dynamically recalculating as obstacles move.
Goal: The robot successfully reaches the destination while avoiding obstacles.

# Controls
Left Mouse Click:
First click: Set the robot's starting position.
Second click: Set the destination position.
The robot begins navigating towards the destination immediately after both positions are set.

# Technologies Used
Python
Pygame for visualization
PriorityQueue from the queue library for efficient A* implementation

# Installation and Usage
pip install pygame
python roboticNavigation.py


