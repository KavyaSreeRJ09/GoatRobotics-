import heapq

import pygame

# Constants
WIDTH = 600
HEIGHT = 600
GRID_SIZE = 50  # Size of each grid cell (50x50)
COLS = WIDTH // GRID_SIZE
ROWS = HEIGHT // GRID_SIZE

# Directions for movement (no diagonal movement)
DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

# Colors (all elements changed to white, except robot and path)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)  # Robot color remains green
RED = (255, 0, 0)  # Path color remains red
BLUE = (0, 0, 255)
GRAY = (169, 169, 169)

# Initialize Pygame
pygame.init()

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Robot Navigation")

# Font setup
font = pygame.font.SysFont('Arial', 24)

# A* algorithm for pathfinding
def heuristic(a, b):
    """Calculate the Manhattan distance heuristic."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(start, goal, grid):
    """A* algorithm for pathfinding, avoiding obstacles."""
    open_set = []
    heapq.heappush(open_set, (0, start))
    
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    came_from = {}
    
    while open_set:
        _, current = heapq.heappop(open_set)
        
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path
        
        for dx, dy in DIRECTIONS:
            neighbor = (current[0] + dx, current[1] + dy)
            
            # Check if the neighbor is within bounds and not an obstacle
            if 0 <= neighbor[0] < COLS and 0 <= neighbor[1] < ROWS and grid[neighbor[1]][neighbor[0]] != 1:
                tentative_g_score = g_score[current] + 1
                
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
    
    return None  # No path found

# Draw the rectangle (pillar) with different colors for each vertex
def draw_pillar(pillar_vertices):
    # Define colors for the vertices
    vertex_colors = [WHITE, GREEN, BLUE, RED]
    
    for i, vertex in enumerate(pillar_vertices):
        pygame.draw.circle(screen, vertex_colors[i], (vertex[0] * GRID_SIZE + GRID_SIZE // 2, vertex[1] * GRID_SIZE + GRID_SIZE // 2), GRID_SIZE // 4)

    pygame.draw.polygon(screen, WHITE, pillar_vertices)  # Pillar color remains white

# Draw the grid
def draw_grid():
    for y in range(0, HEIGHT, GRID_SIZE):
        for x in range(0, WIDTH, GRID_SIZE):
            rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, WHITE, rect, 1)  # Grid lines remain white


# Calculate the center of the pillar
def get_pillar_center(pillar_vertices):
    x_coords, y_coords = zip(*pillar_vertices)
    center_x = sum(x_coords) / len(pillar_vertices)
    center_y = sum(y_coords) / len(y_coords)
    return (int(center_x), int(center_y))

# Draw the robot
def draw_robot(position):
    pygame.draw.circle(screen, GREEN, (position[0] * GRID_SIZE + GRID_SIZE // 2, position[1] * GRID_SIZE + GRID_SIZE // 2), GRID_SIZE // 3)

# Draw path
def draw_path(path):
    for point in path:
        pygame.draw.rect(screen, RED, (point[0] * GRID_SIZE + GRID_SIZE // 4, point[1] * GRID_SIZE + GRID_SIZE // 4, GRID_SIZE // 2, GRID_SIZE // 2))

# Main game loop
def main():
    running = True
    clock = pygame.time.Clock()
    
    grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]  # 0 is free space, 1 is obstacle
    pillar_vertices = []  # List to store the four pillar vertices
    obstacles = []  # List of dynamic obstacles
    robot_position = None
    goal_position = None
    path = []
    current_action = 'set_robot'  # Current action being performed: set_robot, set_pillar, add_obstacle
    
    while running:
        screen.fill(BLACK)  # Fill the background with black
        
        draw_grid()  # Draw the grid
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                grid_x, grid_y = x // GRID_SIZE, y // GRID_SIZE
                
                if current_action == 'set_robot' and robot_position is None:
                    # Set the robot's starting position
                    robot_position = (grid_x, grid_y)
                    current_action = 'set_pillar'  # After setting robot, move to pillar setting
                
                elif current_action == 'set_pillar' and len(pillar_vertices) < 4:
                    # Set the pillar's vertices
                    pillar_vertices.append((grid_x, grid_y))
                    if len(pillar_vertices) == 4:
                        # Calculate center of the pillar
                        goal_position = get_pillar_center(pillar_vertices)
                        current_action = 'add_obstacle'  # After setting pillar, start adding obstacles
                
                elif current_action == 'add_obstacle':
                    # Add obstacles (optional, you can click to add obstacles)
                    if (grid_x, grid_y) not in pillar_vertices and (grid_x, grid_y) not in obstacles and (grid_x, grid_y) != robot_position:
                        obstacles.append((grid_x, grid_y))
                
        # Draw the pillar
        if len(pillar_vertices) == 4:
            draw_pillar(pillar_vertices)
        
        # Draw the obstacles
        for obs in obstacles:
            pygame.draw.rect(screen, WHITE, (obs[0] * GRID_SIZE, obs[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))  # Obstacles drawn in white
        
        # Calculate path if the goal is set and robot is initialized
        if goal_position and robot_position:
            path = a_star(robot_position, goal_position, grid)
            if path:
                draw_path(path)
            
            # Move robot step-by-step along the path
            if path:
                if robot_position != goal_position:
                    robot_position = path[0]
            
        # Draw robot at its current position
        if robot_position:
            draw_robot(robot_position)
        
        pygame.display.flip()
        clock.tick(10)  # Adjust the speed of the robot

# Run the game
if __name__ == '__main__':
    main()

