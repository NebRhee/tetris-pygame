from colors import Colors
from position import Position
import pygame

class Block:
    def __init__(self, id):
        self.id = id
        self.rotation_state = 0
        self.cells = {}
        self.cell_size = 30
        self.colors = Colors.get_colors()
        self.offset = Position(0, 0)
        

    def rotate_cw(self):
        self.rotation_state = (self.rotation_state + 1) % 4

    def rotate_ccw(self):
        if (self.rotation_state == 0):
            self.rotation_state = 3
        else:
            self.rotation_state -= 1

    # Calculates positions of tetromino tiles in the grid
    def get_tile_positions(self):
        tetromino = self.cells[self.rotation_state]
        updated_tetromino = []

        for tile in tetromino: 
            new_position = Position(self.offset.row + tile.row, self.offset.col + tile.col)
            updated_tetromino.append(new_position)

        return updated_tetromino        # Returns a list of the updated positions

    # Move block by changing offset Position
    def move(self, rows, cols):
        self.offset.row += rows
        self.offset.col += cols

    def print_positions(self):
        tetromino = self.cells[self.rotation_state]
        for tile in tetromino:
            print(tile.row, tile.col, end="   ")
        print()

    def draw(self, screen, offset_x, offset_y):
        tetromino = self.get_tile_positions()   # List of updated tetromino tile positions

        # Draw block
        for tile in tetromino:
            tile_rect = pygame.Rect(tile.col* self.cell_size + offset_x, tile.row * self.cell_size + offset_y,
                                       self.cell_size - 1, self.cell_size - 1)
            pygame.draw.rect(screen, self.colors[self.id], tile_rect)
    