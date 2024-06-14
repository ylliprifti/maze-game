from browser import document, html, window
import random

# Constants
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE
WHITE = "white"
BLACK = "black"
GREEN = "green"
RED = "red"

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

# Player position
player_pos = [1, 1]
end_pos = [COLS - 2, ROWS - 2]

# Create the canvas
canvas = document["gameCanvas"]
ctx = canvas.getContext("2d")

def create_maze(rows, cols):
    maze = [[1 for _ in range(cols)] for _ in range(rows)]

    def carve(x, y):
        maze[y][x] = 0
        directions = DIRECTIONS[:]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + 2*dx, y + 2*dy
            if 0 <= nx < cols and 0 <= ny < rows and maze[ny][nx] == 1:
                maze[ny - dy][nx - dx] = 0
                carve(nx, ny)

    carve(1, 1)
    maze[1][1] = 0
    maze[rows - 2][cols - 2] = 0
    return maze

def draw_maze(maze):
    for y in range(ROWS):
        for x in range(COLS):
            color = WHITE if maze[y][x] == 0 else BLACK
            ctx.fillStyle = color
            ctx.fillRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)

def draw_player(position, color):
    x, y = position
    ctx.fillStyle = color
    ctx.fillRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)

def move_player(position, direction, maze):
    x, y = position
    dx, dy = direction
    new_x, new_y = x + dx, y + dy
    if 0 <= new_x < COLS and 0 <= new_y < ROWS and maze[new_y][new_x] == 0:
        return [new_x, new_y]
    return position

def update(event):
    global player_pos
    key = event.key
    if key == "ArrowUp":
        player_pos = move_player(player_pos, UP, maze)
    elif key == "ArrowDown":
        player_pos = move_player(player_pos, DOWN, maze)
    elif key == "ArrowLeft":
        player_pos = move_player(player_pos, LEFT, maze)
    elif key == "ArrowRight":
        player_pos = move_player(player_pos, RIGHT, maze)

    ctx.clearRect(0, 0, WIDTH, HEIGHT)
    draw_maze(maze)
    draw_player(player_pos, GREEN)
    draw_player(end_pos, RED)

    if player_pos == end_pos:
        ctx.fillStyle = "black"
        ctx.font = "50px Arial"
        ctx.fillText("You Win!", WIDTH // 2 - 100, HEIGHT // 2)

# Generate maze and draw initial state
maze = create_maze(ROWS, COLS)
draw_maze(maze)
draw_player(player_pos, GREEN)
draw_player(end_pos, RED)

# Bind update function to keydown event
window.bind("keydown", update)


