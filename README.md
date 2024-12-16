
## (1 - GRID ROBOTICS)

The provided code simulates a dynamic robot navigation system in a grid environment with moving obstacles using Python and Pygame. The robot uses the A pathfinding algorithm* to find an optimal path to its destination while avoiding obstacles that move randomly at set intervals.

## Features
Grid Environment: The simulation operates on a 10x10 grid where each cell represents a navigable area.
A Pathfinding Algorithm*: The robot dynamically calculates the shortest path to the destination while avoiding obstacles.
Dynamic Obstacles: Obstacles move randomly within the grid at regular intervals, adding complexity to the navigation.

## Visualization:

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
Python ,
Pygame for visualization ,
PriorityQueue from the queue library for efficient A* implementation.

# Installation and Usage
pip install pygame

python roboticNavigation.py

## (2- ROBOT CENTER MOVEMENT )

This project demonstrates a dynamic robot navigation system where a robot must navigate through a grid environment to reach the center of a custom-defined pillar while avoiding obstacles. The project is built using Python and Pygame and employs the A pathfinding algorithm* to dynamically calculate the optimal path to the target.

# Features

Grid Environment: A 12x12 grid (600x600 pixels) serves as the simulation environment.

# Interactive Setup:

Users can define the robot's starting position.

Users can specify the pillar by selecting four vertices, with the robot aiming to reach the calculated center of the pillar.

Users can place additional obstacles after defining the pillar.

# Dynamic Pathfinding:

The robot dynamically calculates its path to the pillar's center using the A algorithm*.
Obstacles are avoided while navigating the grid.

# Visualization:
The robot is represented by a green circle.

The pillar's center is marked by a white polygon with colored vertices.

Obstacles are displayed as white rectangles.

The robot’s path is visualized in red.

# How It Works

Grid and Setup:
The simulation begins with a blank 12x12 grid.
The user sets up the robot's starting position, pillar vertices, and optional obstacles through mouse clicks.

Pillar Center Calculation:
The center of the pillar is computed as the average of the four vertices provided by the user.

Dynamic Pathfinding:
The robot calculates and follows the shortest path to the pillar center while avoiding obstacles.

Goal:
The robot successfully reaches the calculated center of the pillar.

# Controls (Mouse Input)

First click: Set the robot's starting position.

Next four clicks: Define the vertices of the pillar.

Automatic Navigation:
Once the pillar and robot positions are set, the robot automatically navigates to the pillar's center.

# Technologies Used
Python ,
Pygame for visualization ,
HeapQueue for efficient A* algorithm implementation. 

# Installation and Usage
pip install pygame

python Centerpoints.py
