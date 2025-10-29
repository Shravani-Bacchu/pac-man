import pygame as pg
import random

pg.init()

WIDTH, HEIGHT = 600, 600
GRID_SIZE = 30
ROWS, COLS = HEIGHT // GRID_SIZE, WIDTH // GRID_SIZE

white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 38, 66)
red = (128, 14, 19)
yellow = (255, 249, 71)
green = (41, 82, 74)

maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 3, 1, 0, 1, 3, 0, 0, 0, 0, 1, 3, 1, 0, 1, 3, 0, 1],
    [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

pellet_positions = [
    (row_idx, col_idx)
    for row_idx, row in enumerate(maze)
    for col_idx, cell in enumerate(row)
    if cell == 2
]

def draw_maze(screen):
    for row_idx, row in enumerate(maze):
        for col_idx, cell in enumerate(row):
            x, y = col_idx * GRID_SIZE, row_idx * GRID_SIZE
            if cell == 1:
                pg.draw.rect(screen, green, (x, y, GRID_SIZE, GRID_SIZE))
            elif cell == 2:
                pg.draw.circle(screen, white, (x + GRID_SIZE // 2, y + GRID_SIZE // 2), 5)
            elif cell == 3:
                pg.draw.circle(screen, yellow, (x + GRID_SIZE // 2, y + GRID_SIZE // 2), 12)
            elif cell == 4:
                pg.draw.circle(screen, red, (x + GRID_SIZE // 2, y + GRID_SIZE // 2), 12)


def get_position():
    pacman_pos = None
    ghost_positions = []
    for row_idx, row in enumerate(maze):
        for col_idx, cell in enumerate(row):
            if cell == 4:
                pacman_pos = [row_idx, col_idx]
            elif cell == 3:
                ghost_positions.append([row_idx, col_idx])
    return pacman_pos, ghost_positions


pacman_pos, ghost_positions = get_position()
score = 0
lives = 5


def move_pacman(direction, screen):
    global pacman_pos, score

    row, col = pacman_pos
    new_row, new_col = row, col

    if direction == "UP":
        new_row -= 1
    elif direction == "DOWN":
        new_row += 1
    elif direction == "LEFT":
        new_col -= 1
    elif direction == "RIGHT":
        new_col += 1

    # Check if next cell is not a wall
    if maze[new_row][new_col] != 1:
        if (new_row, new_col) in pellet_positions:
            pellet_positions.remove((new_row, new_col))
            score += 15
        maze[row][col] = 0
        maze[new_row][new_col] = 4
        pacman_pos = [new_row, new_col]

    check_collision(screen)


def move_ghosts(screen):
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for ghost in ghost_positions:
        row, col = ghost
        random.shuffle(directions)
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if maze[new_row][new_col] in [0, 2]:
                maze[row][col] = 0
                if (row, col) in pellet_positions:
                    maze[row][col] = 2
                ghost[0], ghost[1] = new_row, new_col
                maze[new_row][new_col] = 3
                break
    check_collision(screen)


def check_collision(screen):
    global lives, pacman_pos
    for ghost in ghost_positions:
        if pacman_pos == ghost:
            lives -= 1
            if lives > 0:
                display_message(screen, "You lost a life!", red)
            else:
                display_message(screen, "Game Over!", red)
                pg.quit()
                exit()

            old_row, old_col = pacman_pos
            maze[old_row][old_col] = 0
            pacman_pos = [1, 1]
            maze[1][1] = 4
            break


def display_message(screen, message, color=white):
    font = pg.font.Font(None, 50)
    text = font.render(message, True, color)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pg.display.flip()
    pg.time.delay(2000)


def main():
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Pac-Man")
    clock = pg.time.Clock()

    while True:
        screen.fill(black)
        draw_maze(screen)

        font = pg.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, white)
        lives_text = font.render(f"Lives: {lives}", True, white)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (WIDTH - 150, 10))

        move_ghosts(screen)
        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    move_pacman("UP", screen)
                elif event.key == pg.K_DOWN:
                    move_pacman("DOWN", screen)
                elif event.key == pg.K_LEFT:
                    move_pacman("LEFT", screen)
                elif event.key == pg.K_RIGHT:
                    move_pacman("RIGHT", screen)

        clock.tick(5)


if __name__ == "__main__":
    main()
