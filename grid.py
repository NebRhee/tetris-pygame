import pygame
from colors import Colors

class Grid:
    
    # Constructor
    def __init__(self):
        self.rows = 23
        self.cols = 10
        self.cell_size = 30
        self.grid = [[0 for j in range(self.cols)] for i in range(self.rows)]
        self.colors = Colors.get_colors()

    def print_grid(self):
        for row in range(self.rows):
            for col in range(self.cols):
                print(self.grid[row][col], end = " ")
            print()

    # Check if cell is within bounds
    def is_inside(self, row, col):
        return (row >= 0 and row < self.rows and col >=0 and col < self.cols)
        
    # Check if cell is empty 
    def is_empty(self, row, col):
        return self.is_inside(row, col) and self.grid[row][col] == 0
    
    # def collides_with_block(self, block):
    #     for tile in block.get_tile_positions():
    #         if not self.is_empty(tile.row, tile.col):
    #             return True
    #     return False

    # def out_of_bounds(self, block):
    #     for tile in block.get_tile_positions():
    #         if (
    #             tile.col < 0 or
    #             tile.col >= self.cols or
    #             tile.row >= self.rows
    #         ):
    #             return True
    #     return False
    
    # def is_valid_position(self, block):
    #     #block.print_positions()
    #     return not self.collides_with_block(block) and not self.out_of_bounds(block)






    # Check if row is full (for clearing)
    def is_row_full(self, row):
        for col in range(self.cols):
            if self.grid[row][col] == 0:
                return False
        return True
    
    # Check if row is empty
    def is_row_empty(self, row):
        for col in range(self.cols):
            if self.grid[row][col] != 0:
                return False
        return True

    # Clear row and increment cleared
    def clear_row(self, row):
        for col in range(self.cols):
            self.grid[row][col] = 0

    # Move row down
    def move_row_down(self, row, clearedRows):
        for col in range(self.cols):
            # Overwrite empty row
            self.grid[row + clearedRows][col] = self.grid[row][col]
            self.grid[row][col] = 0

    # Iterate through entire grid and clear full rows, incrementing cleared
    def clear_full_rows(self):
        cleared = 0

        # Bottom to top
        for row in range(self.rows - 1, -1, -1):
            if self.is_row_full(row):
                self.clear_row(row)
                cleared += 1
            elif cleared > 0:
                self.move_row_down(row, cleared)
        
        return cleared


    
    def reset(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.grid[row][col] = 0


    def draw(self, screen):
        for row in range(self.rows):
            for col in range (self.cols):
                cell_value = self.grid[row][col]
                cell_box = pygame.Rect(col*self.cell_size + 201, row*self.cell_size + 1,
                                       self.cell_size - 1, self.cell_size - 1)
                # surface, color, rect
                pygame.draw.rect(screen, self.colors[cell_value], cell_box)