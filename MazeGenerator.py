"""
Maze generator project. December 2024.
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 11:07:23 2024

@author: sila
"""

import random
import matplotlib.pyplot as plt
import time

WIDTH = 39 # Width of the maze (must be odd).
HEIGHT = 19 # Height of the maze (must be odd).
assert WIDTH % 2 == 1 and WIDTH >= 3
assert HEIGHT % 2 == 1 and HEIGHT >= 3

# Use these characters for displaying the maze:
EMPTY = 0
WALL = 1
START = 2
END = 3
NORTH, SOUTH, EAST, WEST = 'n', 's', 'e', 'w'

# Create the filled-in maze data structure to start:
maze = {}
for x in range(WIDTH):
    for y in range(HEIGHT):
        maze[(x, y)] = WALL # Every space is a wall at first.

def display_maze(maze):
    """Displays the maze visually using matplotlib."""
    grid = [[maze[(x, y)] for x in range(WIDTH)] for y in range(HEIGHT)]
    plt.figure(figsize=(WIDTH / 5, HEIGHT / 5))
    plt.imshow(grid, cmap="binary", interpolation="none")
    plt.axis('off')
    plt.show()

def display_maze_with_colors(maze):
    """Displays the maze visually using matplotlib, with START and END in different colors."""
    grid = [[maze[(x, y)] for x in range(WIDTH)] for y in range(HEIGHT)]

    # Create a colormap for custom display
    cmap = plt.cm.get_cmap("viridis", 4)  # Custom colormap for 4 unique values
    cmap.set_under("blue")  # START as blue
    cmap.set_over("red")    # END as red

    # Define a color mapping for START and END
    colors = ["white", "black", "blue", "red"]
    cmap = plt.matplotlib.colors.ListedColormap(colors)

    plt.figure(figsize=(WIDTH / 5, HEIGHT / 5))
    plt.imshow(grid, cmap=cmap, interpolation="none", vmin=0, vmax=3)
    plt.axis('off')
    plt.show()

def visit(x, y):
    """Carve out" empty spaces in the maze at x, y and then
    recursively move to neighboring unvisited spaces. This
    function backtracks when the mark has reached a dead end."""
    maze[(x, y)] = EMPTY # "Carve out" the space at x, y.

    while True:
        # Check which neighboring spaces adjacent to
        # the mark have not been visited already:
        unvisitedNeighbors = []
        if y > 2 and (x, y - 2) not in hasVisited:
            unvisitedNeighbors.append(NORTH)

        if y < HEIGHT - 3 and (x, y + 2) not in hasVisited:
            unvisitedNeighbors.append(SOUTH)

        if x > 2 and (x - 2, y) not in hasVisited:
            unvisitedNeighbors.append(WEST)

        if x < WIDTH - 3 and (x + 2, y) not in hasVisited:
            unvisitedNeighbors.append(EAST)

        if len(unvisitedNeighbors) == 0:
            # BASE CASE
            # All neighboring spaces have been visited, so this is a
            # dead end. Backtrack to an earlier space:
            return
        else:
            # RECURSIVE CASE
            # Randomly pick an unvisited neighbor to visit:
            nextIntersection = random.choice(unvisitedNeighbors)

            # Move the mark to an unvisited neighboring space:

            if nextIntersection == NORTH:
                nextX = x
                nextY = y - 2
                maze[(x, y - 1)] = EMPTY # Connecting hallway.
            elif nextIntersection == SOUTH:
                nextX = x
                nextY = y + 2
                maze[(x, y + 1)] = EMPTY # Connecting hallway.
            elif nextIntersection == WEST:
                nextX = x - 2
                nextY = y
                maze[(x - 1, y)] = EMPTY # Connecting hallway.
            elif nextIntersection == EAST:
                nextX = x + 2
                nextY = y
                maze[(x + 1, y)] = EMPTY # Connecting hallway.

            hasVisited.append((nextX, nextY)) # Mark as visited.
            visit(nextX, nextY) # Recursively visit this space.

def find_random_empty_cells(maze):
    """Find two random empty cells in the maze and set them as START and END."""
    empty_cells = [(x, y) for x in range(WIDTH) for y in range(HEIGHT) if maze[(x, y)] == EMPTY]
    if len(empty_cells) < 2:
        raise ValueError("Not enough empty cells to place start and end.")

    start_cell, end_cell = random.sample(empty_cells, 2)
    maze[start_cell] = START
    maze[end_cell] = END
    return start_cell, end_cell

# Carve out the paths in the maze data structure:
random.seed(time.time())
startx= random.randint(1, WIDTH-1)
starty= random.randint(1, HEIGHT-1)
hasVisited = [(startx, starty)] # Start by visiting the top-left corner.
visit(startx, starty)

# Display the final resulting maze data structure:
display_maze(maze)

find_random_empty_cells(maze)

display_maze_with_colors(maze)