from blocks import *
from grid import Grid
from collections import deque
import random
import copy
import pygame

class TetrisGame:
    def __init__(self):
        self.grid = Grid()
        self.game_over = False
        self.bag = deque(maxlen=14) # Queue will always have 7 to 14 elements, initially 7
        self.current_placed = False 
        self.current_block = self.get_current_block()
        self.held_block = None
        self.can_hold = True
        self.score = 0
        self.lines_cleared = 0
        self.ghost_block = copy.deepcopy(self.current_block)

        self.clear_sound = None
        self.music_sound = None
    
    # Generates and shuffles 7 blocks
    def generate_shuffled_bag(self):
        bag = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        random.shuffle(bag)
        return bag

    def get_current_block(self): 
        if len(self.bag) < 7:
            new_bag = self.generate_shuffled_bag()
            self.bag.extend(new_bag) # Generate and add next 7-bag to the queue
        self.current_block = self.bag.popleft()
        return self.current_block
    
    # Movement
    
    def move_left(self):
        self.current_block.move(0, -1)
        if not self.block_fits():
            self.current_block.move(0, 1)

    def move_right(self):
        self.current_block.move(0, 1)
        if not self.block_fits():
            self.current_block.move(0, -1)

    def move_down(self):
        self.current_block.move(1, 0)
        if not self.block_fits():
            self.current_block.move(-1, 0)
            self.place_block()
            self.current_placed = True

    def try_rotate_cw(self):
        self.current_block.rotate_cw()
        tetromino = self.current_block.get_tile_positions()
        # Check if tetromino is within bounds
        for tile in tetromino:
            if not (self.grid.is_empty(tile.row, tile.col)):
                self.current_block.rotate_ccw()
                return

    
    def try_rotate_ccw(self):
        self.current_block.rotate_ccw()
        tetromino = self.current_block.get_tile_positions()
        # Check if tetromino is within bounds
        for tile in tetromino:
            if not (self.grid.is_empty(tile.row, tile.col)):
                self.current_block.rotate_cw()
                return



        

    # Check if rotation is valid
    # def try_rotate_ccw(self):
    #     self.test_block = copy.deepcopy(self.current_block)
    #     self.test_block.rotate_ccw() # Rotated Position

    #     if not self.grid.is_valid_position(self.test_block): # If rotation is not valid
    #         if self.grid.is_valid_position(self.test_block.move(0, -1)): # Left
    #             self.current_block = self.test_block
    #         elif self.grid.is_valid_position(self.test_block.move(0, 2)): # Right
    #             self.current_block = self.test_block
    #         elif self.grid.is_valid_position(self.test_block.move(-1, 1)): # Up
    #             self.current_block = self.test_block
    #         elif self.grid.is_valid_position(self.test_block.move(-2, 0)): # Down
    #             self.current_block = self.test_block
    #     else:
    #         self.current_block = self.test_block



                    

    def is_game_over(self):
        return not (self.grid.is_row_empty(0) and self.grid.is_row_empty(1)) # Returns true if either of the top two rows is occupied
    
    def place_block(self):
        tetromino = self.current_block.get_tile_positions() 
        for tile in tetromino:
            self.grid.grid[tile.row][tile.col] = self.current_block.id
        
        new_lines_cleared = self.grid.clear_full_rows()
        if new_lines_cleared > 0:
            self.clear_sound.set_volume(0.20)
            self.clear_sound.play()
            self.lines_cleared += new_lines_cleared
            self.update_score(new_lines_cleared)


        if (self.is_game_over()):
            self.game_over = True
        else:
            self.current_block = self.get_current_block()
            self.can_hold = True
    
    # Instantly drops the block into place
    def instant_drop(self):
        while self.block_fits() and self.current_placed == False:
            self.move_down()
        self.current_placed = False

    def block_fits(self):
        tetromino = self.current_block.get_tile_positions() # Retrieves updated positions of the block inside the grid
        for tile in tetromino:
            # If block is not within bounds or collides with grid blocks
            if not (self.grid.is_empty(tile.row, tile.col)):
                return False
        return True
    
    def hold_block(self):
        if not self.can_hold:
            return
        
        if self.held_block == None:
            self.held_block = self.current_block
            self.current_block = self.get_current_block()
        else:
            temp = self.current_block
            self.current_block = self.held_block
            self.held_block = temp
        
        self.held_block.__init__()
        self.can_hold = False

    # Checks if the ghost block and current block are in the same positions
    def is_lowest_position(self):
        current_tetromino = self.current_block.get_tile_positions()
        ghost_tetromino = self.ghost_block.get_tile_positions()
        
        for curr_tile, ghost_tile in zip(current_tetromino, ghost_tetromino):
            #curr_tile.print_pos(ghost_tile) DEBUG
            if not curr_tile.is_equal(ghost_tile): # True if equal
                #print("Not equal")
                return False
        
        #print("EQUAL")
        return True
        

    """Ghost Block Methods"""
    def find_lowest_valid_position(self):
        # Copy the block attributes every time this is called
        self.ghost_block = copy.deepcopy(self.current_block)
        self.ghost_block.id = 8
        while self.ghost_block_fits():
            self.ghost_block.move(1, 0)
        self.ghost_block.move(-1, 0) # Lowest valid position

    def ghost_block_fits(self):
        tetromino = self.ghost_block.get_tile_positions() # Retrieves updated positions of the block inside the grid
        for tile in tetromino:
            # If block is not within bounds or collides with grid blocks
            if not (self.grid.is_empty(tile.row, tile.col)):
                return False
        return True

    def ghost_fits_rotation(self):
        tetromino = self.ghost_block.get_tile_positions() # Retrieves updated positions of the block inside the grid
        for tile in tetromino:
            if not self.grid.is_empty(tile.row, tile.col):
                # Check along x axis
                if (tile.col >= self.grid.cols):
                    self.current_block.move(0, -1)
                    break
                elif (tile.col < 0):
                    self.current_block.move(0, 1)
                    break
                # Check below
                else:
                    self.current_block.move(-1, 0)
                    break

    """Rest of the game methods"""
    def update_score(self, lines_cleared):
        if lines_cleared == 1:
            self.score += 100
        elif lines_cleared == 2:
            self.score += 300
        elif lines_cleared == 3:
            self.score += 500
        elif lines_cleared == 4:
            self.score += 800      

    def reset(self):
        self.grid.reset()
        self.game_over = False
        self.bag = deque(maxlen=14) # Queue will always have 7 to 14 elements, initially 7
        self.current_placed = False 
        self.current_block = self.get_current_block()
        self.score = 0
        self.lines_cleared = 0
        self.stop_music()
        self.play_music()
        
    def draw(self, screen):         
        self.grid.draw(screen)
        # Draw ghost block
        self.find_lowest_valid_position()
        self.ghost_block.draw(screen, 201, 1)

        self.current_block.draw(screen, 201, 1)

        y_offset = 72
    
        # Draw next blocks
        for i in range(5):
            if self.bag[i].id == 1 or self.bag[i].id == 4:
                self.bag[i].draw(screen, 455, y_offset)
            else:
                self.bag[i].draw(screen, 470, y_offset)
            y_offset += 80

        # Draw held block
        if self.held_block is not None:
            y_offset = 100
            if self.held_block.id == 1:
                self.held_block.draw(screen, -49, y_offset - 15)
            elif self.held_block.id == 4:
                self.held_block.draw(screen, -49, y_offset)
            else:
                self.held_block.draw(screen, -32, y_offset)

    def set_audio_paths(self, clear_sound_path, music_path):
        self.clear_sound = pygame.mixer.Sound(clear_sound_path)
        pygame.mixer_music.load(music_path)
        pygame.mixer_music.set_volume(0.35)

    def play_music(self):
        pygame.mixer_music.play(-1)

    def stop_music(self):
        pygame.mixer_music.stop()