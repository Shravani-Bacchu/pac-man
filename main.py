import pygame as pg
import random

pg.init()

WIDTH,HEIGHT = 600,600
GRID_SIZE = 30

ROWS,COLS=HEIGHT//GRID_SIZE,WIDTH//GRID_SIZE

white = (255,255,255)
black = (0,0,0)
blue = (0, 38, 66)
red = (128, 14, 19)
yellow =(255, 249, 71)
green =(41, 82, 74)

maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 3, 1, 0, 1, 3, 0, 0, 0, 0, 1, 3, 1, 0, 1, 3, 0, 1],
    [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

pellet_positions = [(row_idx, col_idx) for row_idx, row in enumerate(maze)for col_idx, cell in enumerate(row)if cell==2]

def draw_maze(screen):
    for row_idx, row in enumerate(maze):
        for col_idx, cell in enumerate(row):
            x,y = col_idx * GRID_SIZE,row_idx * GRID_SIZE
            if cell == 1:
                pg.draw.rect(screen,green,(x, y, GRID_SIZE, GRID_SIZE))
            elif cell == 2:
                pg.draw.circle(screen, white, (x + GRID_SIZE // 2, y + GRID_SIZE // 2), 5)
            elif cell == 3:
                pg.draw.circle(screen, yellow, (x + GRID_SIZE // 2, y + GRID_SIZE // 2), 12)
            elif cell == 4:
                pg.draw.circle(screen, green, (x + GRID_SIZE // 2, y + GRID_SIZE // 2), 12)
              
def get_position():
    pacman_pos = None
    ghost_positions = []
    for row_idx, row in enumerate(maze):
        for col_idx, cell in enumerate(row):
            if cell==4:
                pacman_pos = [row_idx,col_idx]
            elif cell==3:
                ghost_positions.append([row_idx,col_idx])
    return pacman_pos,ghost_positions
pacman_pos, ghost_positions = get_position()
score =0
lives = 5

def move_pacman(direction,screen):
    global pacman_pos,score
    row,col = pacman_pos
    new_row,new_col = row,col
    if direction == "UP":
        new_row -=1
    elif direction =="DOWN":
        new_row +=1
    elif direction =="LEFT":
        new_col -=1
    elif direction =="RIGHT":
        new_col +=1
    if maze[new_row][new_col] !=1:
        if (new_row,new_col) in pellet_positions:
            pellet_positions.remove((new_row,new_col))
            score +=15
        maze[row][col] = 0
        maze[new_row][new_col]= 4
        pacman_pos = [new_row] [new_col]
    check_collision(screen)
