import random
import time
from queue import PriorityQueue

import pygame

# Constants
GRID_SIZE = 10
CELL_SIZE = 60
WIDTH, HEIGHT = GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE
FPS = 60
OBSTACLE_MOVE_INTERVAL = 3  # Interval for obstacle movement in seconds
STEP_TIME = 1  # Time per step for robot movement

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dynamic Robot Navigation")
import random
import time
from queue import PriorityQueue

import pygame

# Constants
GRID_SIZE = 10
CELL_SIZE = 60
WIDTH, HEIGHT = GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE
FPS = 60
OBSTACLE_MOVE_INTERVAL = 3  # Interval for obstacle movement in seconds
STEP_TIME = 1  # Time per step for robot movement

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dynamic Robot Navigation")
clock = pygame.time.Clock()


# Utility Functions
def draw_grid():
    """Draws the grid lines."""
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (WIDTH, y))


def draw_obstacles(obstacles):
    """Draws the obstacles on the grid."""
    for obstacle in obstacles:
        rect = pygame.Rect(obstacle[1] * CELL_SIZE, obstacle[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, BLACK, rect)


def draw_robot(position):
    """Draws the robot on the grid."""
    rect = pygame.Rect(position[1] * CELL_SIZE, position[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, GREEN, rect)


def draw_destination(position):
    """Draws the destination on the grid."""
    rect = pygame.Rect(position[1] * CELL_SIZE, position[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, RED, rect)


def draw_path(path):
    """Draws the current path on the grid."""
    for pos in path:
        rect = pygame.Rect(pos[1] * CELL_SIZE, pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, YELLOW, rect)


def heuristic(a, b):
    """Heuristic for A* pathfinding."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_star(start, goal, obstacles):
    """A* Pathfinding Algorithm."""
    open_set = PriorityQueue()
    open_set.put((0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while not open_set.empty():
        current = open_set.get()[1]

        if current == goal:
            # Reconstruct path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        neighbors = [(current[0] + dx, current[1] + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]
        for neighbor in neighbors:
            if 0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE and neighbor not in obstacles:
                tentative_g_score = g_score[current] + 1
                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    open_set.put((f_score[neighbor], neighbor))

    return []  # No path found


def generate_random_obstacles():
    """Generates 30 random obstacles."""
    obstacles = set()
    while len(obstacles) < 30:
        obstacle = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
        obstacles.add(obstacle)
    return obstacles


def move_obstacles(obstacles, robot, destination):
    """Moves obstacles randomly while ensuring their count remains constant."""
    new_obstacles = set()
    for obstacle in obstacles:
        valid_move = False
        for _ in range(10):  # Try up to 10 times to find a valid move
            direction = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
            new_pos = (obstacle[0] + direction[0], obstacle[1] + direction[1])

            # Ensure the new position is within bounds and not overlapping robot or destination
            if (0 <= new_pos[0] < GRID_SIZE and 
                0 <= new_pos[1] < GRID_SIZE and 
                new_pos not in new_obstacles and 
                new_pos != robot and 
                new_pos != destination):
                new_obstacles.add(new_pos)
                valid_move = True
                break

        # If no valid move is found, keep the obstacle in its current position
        if not valid_move:
            new_obstacles.add(obstacle)

    return new_obstacles

def main():
    obstacles = generate_random_obstacles()
    robot = None
    destination = None
    path = []
    last_obstacle_move_time = time.time()

    running = True
    while running:
        screen.fill(WHITE)
        draw_grid()
        draw_obstacles(obstacles)
        if robot:
            draw_robot(robot)
        if destination:
            draw_destination(destination)
        if path:
            draw_path(path)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                grid_pos = (y // CELL_SIZE, x // CELL_SIZE)

                if robot is None and grid_pos not in obstacles:
                    robot = grid_pos
                elif destination is None and grid_pos not in obstacles:
                    destination = grid_pos

        # Move obstacles every OBSTACLE_MOVE_INTERVAL seconds
        if time.time() - last_obstacle_move_time > OBSTACLE_MOVE_INTERVAL:
            obstacles = move_obstacles(obstacles, robot, destination)
            last_obstacle_move_time = time.time()

        # Dynamically calculate the path at each step
        if robot and destination and robot != destination:
            path = a_star(robot, destination, obstacles)

            if path:
                robot = path[0]  # Move to the next step
                path.pop(0)  # Remove the current step from the path
                time.sleep(STEP_TIME)

            if robot == destination:
                print("Robot reached the destination!")
                time.sleep(2)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
clock = pygame.time.Clock()


# Utility Functions
def draw_grid():
    """Draws the grid lines."""
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (WIDTH, y))


def draw_obstacles(obstacles):
    """Draws the obstacles on the grid."""
    for obstacle in obstacles:
        rect = pygame.Rect(obstacle[1] * CELL_SIZE, obstacle[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, BLACK, rect)


def draw_robot(position):
    """Draws the robot on the grid."""
    rect = pygame.Rect(position[1] * CELL_SIZE, position[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, GREEN, rect)


def draw_destination(position):
    """Draws the destination on the grid."""
    rect = pygame.Rect(position[1] * CELL_SIZE, position[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, RED, rect)


def draw_path(path):
    """Draws the current path on the grid."""
    for pos in path:
        rect = pygame.Rect(pos[1] * CELL_SIZE, pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, YELLOW, rect)


def heuristic(a, b):
    """Heuristic for A* pathfinding."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_star(start, goal, obstacles):
    """A* Pathfinding Algorithm."""
    open_set = PriorityQueue()
    open_set.put((0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while not open_set.empty():
        current = open_set.get()[1]

        if current == goal:
            # Reconstruct path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        neighbors = [(current[0] + dx, current[1] + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]
        for neighbor in neighbors:
            if 0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE and neighbor not in obstacles:
                tentative_g_score = g_score[current] + 1
                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    open_set.put((f_score[neighbor], neighbor))

    return []  # No path found


def generate_random_obstacles():
    """Generates 30 random obstacles."""
    obstacles = set()
    while len(obstacles) < 30:
        obstacle = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
        obstacles.add(obstacle)
    return obstacles


def move_obstacles(obstacles, robot, destination):
    """Moves obstacles randomly while avoiding the robot and destination."""
    new_obstacles = set()
    for obstacle in obstacles:
        direction = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
        new_pos = (obstacle[0] + direction[0], obstacle[1] + direction[1])

        if 0 <= new_pos[0] < GRID_SIZE and 0 <= new_pos[1] < GRID_SIZE and new_pos not in {robot, destination}:
            new_obstacles.add(new_pos)
        else:
            new_obstacles.add(obstacle)  # Keep original position if new one is invalid
    return new_obstacles


def main():
    obstacles = generate_random_obstacles()
    robot = None
    destination = None
    path = []
    last_obstacle_move_time = time.time()

    running = True
    while running:
        screen.fill(WHITE)
        draw_grid()
        draw_obstacles(obstacles)
        if robot:
            draw_robot(robot)
        if destination:
            draw_destination(destination)
        if path:
            draw_path(path)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                grid_pos = (y // CELL_SIZE, x // CELL_SIZE)

                if robot is None and grid_pos not in obstacles:
                    robot = grid_pos
                elif destination is None and grid_pos not in obstacles:
                    destination = grid_pos

        # Move obstacles every OBSTACLE_MOVE_INTERVAL seconds
        if time.time() - last_obstacle_move_time > OBSTACLE_MOVE_INTERVAL:
            obstacles = move_obstacles(obstacles, robot, destination)
            last_obstacle_move_time = time.time()

        # Dynamically calculate the path at each step
        if robot and destination and robot != destination:
            path = a_star(robot, destination, obstacles)

            if path:
                robot = path[0]  # Move to the next step
                path.pop(0)  # Remove the current step from the path
                time.sleep(STEP_TIME)

            if robot == destination:
                print("Robot reached the destination!")
                time.sleep(2)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()



