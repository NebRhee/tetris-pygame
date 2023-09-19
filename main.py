import pygame, sys, os
from tetris_game import TetrisGame
from colors import Colors

"""
    To build and create the executable run this in the terminal in the directory
    pyinstaller --add-data "/path/to/lineclear.ogg:audio" --add-data "/path/to/gamemusic.ogg:audio" --onefile --noconsole main.py 
"""

def resource_path(relative_path):
    """Get path to resource"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".") # Use OS library to generate absolute path

    return os.path.join(base_path, relative_path)

def print_file(file_path):
    file_path = resource_path(file_path)
    with open(file_path) as fp:
        for line in fp:
            print(line)


pygame.init()

font = pygame.font.Font(None, 40)
game_over_font = pygame.font.Font(None, 50)

score_surface = font.render("Score", True, Colors.white) # Text, antialias, color
hold_surface = font.render("Hold", True, Colors.white)
next_surface = font.render("Next", True, Colors.white)
cleared_surface = font.render("Cleared", True, Colors.white)
game_over_surface = game_over_font.render("Game Over", True, Colors.red)
time_surface = font.render("Time (s)", True, Colors.white)

hold_rect = pygame.Rect(20, 55, 160, 160) # x, y, w, h
next_rect = pygame.Rect(520, 55, 165, 420)
cleared_rect = pygame.Rect(20, 450, 160, 70)
score_rect = pygame.Rect(20, 580, 160, 70)
time_rect = pygame.Rect(520, 580, 160, 70)

SCREEN_WIDTH = 705
SCREEN_HEIGHT = 690

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()

# In milliseconds
INITIAL_KEY_HOLD_DELAY = 150 
REPEAT_KEY_HOLD_DELAY = 70
MAX_UPDATE_DELAY = 650
MIN_UPDATE_DELAY = 70


# Drop time constants
THRESHOLD_1 = 30000 # 40s
THRESHOLD_2 = 60000 # 60s
DELAY_DECREASE_1 = 10
DELAY_DECREASE_2 = 5
DELAY_DECREASE_3 = 3
SCORE_DECREASE_1 = 0.045
SCORE_DECREASE_2 = 0.03
SCORE_DECREASE_3 = 0.012

update_delay = MAX_UPDATE_DELAY

GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, update_delay) # Game update


game = TetrisGame() # Game instance
line_clear_audio = resource_path("audio/lineclear.ogg")
music_audio = resource_path("audio/gamemusic.ogg")
game.set_audio_paths(line_clear_audio, music_audio)

# Key hold timers
left_key_hold_timer = 0
right_key_hold_timer = 0
down_key_hold_timer = 0


#last_update_time = pygame.time.get_ticks()
start_time = pygame.time.get_ticks()

game.play_music()
# Game loop
while True:
    if not game.game_over:
        current_time = pygame.time.get_ticks() # Current time in ms
        time_difference = current_time - start_time # Elapsed time in ms
        time_difference_s = (time_difference / 1000)
        time_difference_formatted = "{:.1f}".format(time_difference_s)

    # Handle events, including keyboard input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Key presses
        if event.type == pygame.KEYDOWN:
            # Reset game
            if event.key == pygame.K_r:
                game.reset()
                start_time = pygame.time.get_ticks()
            # Movement
            elif event.key == pygame.K_LEFT:
                game.move_left()
                left_key_hold_timer = pygame.time.get_ticks() + INITIAL_KEY_HOLD_DELAY
            elif event.key == pygame.K_RIGHT and game.game_over == False:
                game.move_right()
                right_key_hold_timer = pygame.time.get_ticks() + INITIAL_KEY_HOLD_DELAY
            elif event.key == pygame.K_DOWN and game.game_over == False:
                game.move_down()
                down_key_hold_timer = pygame.time.get_ticks() + REPEAT_KEY_HOLD_DELAY
            elif event.key == pygame.K_SPACE and game.game_over == False:
                game.instant_drop()
            # Rotation
            elif event.key == pygame.K_z and game.game_over == False:
                game.try_rotate_ccw()
            elif (event.key == pygame.K_x or event.key == pygame.K_UP) and game.game_over == False:
                game.try_rotate_cw()
            # Hold block
            elif event.key == pygame.K_c and game.game_over == False:
                game.hold_block()
        # Game timer
        elif event.type == GAME_UPDATE and game.game_over == False:
            game.move_down()
            if game.is_lowest_position():
                update_delay = MAX_UPDATE_DELAY + 100
            else:
                if time_difference < THRESHOLD_1: # 0 - 30s
                    update_delay = max(MIN_UPDATE_DELAY, MAX_UPDATE_DELAY - time_difference_s * DELAY_DECREASE_1 - (game.score * SCORE_DECREASE_1))
                    
                elif time_difference < THRESHOLD_2: # 30 - 60s
                    update_delay = max(MIN_UPDATE_DELAY, MAX_UPDATE_DELAY - time_difference_s * DELAY_DECREASE_2 - (game.score * SCORE_DECREASE_2))
                    
                else: # 60+ s
                    update_delay = max(MIN_UPDATE_DELAY, MAX_UPDATE_DELAY - time_difference_s * DELAY_DECREASE_3 - (game.score * SCORE_DECREASE_3))
                    

            pygame.time.set_timer(GAME_UPDATE,int(update_delay))
            
    if game.is_lowest_position():
        update_delay = MAX_UPDATE_DELAY + 100

    # Left movement with keyholding
    if pygame.key.get_pressed()[pygame.K_LEFT]:
        if current_time >= left_key_hold_timer:
            game.move_left()
            left_key_hold_timer = current_time + REPEAT_KEY_HOLD_DELAY

    # Right movement with keyholding
    if pygame.key.get_pressed()[pygame.K_RIGHT]:
        if current_time >= right_key_hold_timer:
            game.move_right()
            right_key_hold_timer = current_time + REPEAT_KEY_HOLD_DELAY

    # Downward movement with keyholding
    if pygame.key.get_pressed()[pygame.K_DOWN]:
        if current_time >= down_key_hold_timer:
            game.move_down()
            down_key_hold_timer = current_time + REPEAT_KEY_HOLD_DELAY


    # Draw to screen
    score_value_surface = font.render(str(game.score), True, Colors.white)
    cleared_value_surface = font.render(str(game.lines_cleared), True, Colors.white)
    time_value_surface = font.render(str(time_difference_formatted), True, Colors.white)

    screen.fill(Colors.dark_blue)
    screen.blit(hold_surface, (67, 20, 50, 50)) # x, y, w, h
    screen.blit(next_surface, (570, 20, 50, 50))
    screen.blit(cleared_surface, (47, 415, 50, 50))
    screen.blit(score_surface, (62, 547, 50, 50))
    screen.blit(time_surface, (553, 547, 50, 50))
    
    pygame.draw.rect(screen, Colors.black, hold_rect, 0, 10) # Surface, color, rect,  b-w, b-r
    pygame.draw.rect(screen, Colors.black, next_rect, 0, 10)
    pygame.draw.rect(screen, Colors.black, cleared_rect, 0, 10)
    screen.blit(cleared_value_surface, cleared_value_surface.get_rect(centerx=cleared_rect.centerx, centery=cleared_rect.centery))
    pygame.draw.rect(screen, Colors.black, score_rect, 0, 10) 
    screen.blit(score_value_surface, score_value_surface.get_rect(centerx=score_rect.centerx, centery=score_rect.centery))

    # Time
    pygame.draw.rect(screen, Colors.black, time_rect, 0, 10)
    screen.blit(time_value_surface, time_value_surface.get_rect(centerx=time_rect.centerx, centery=time_rect.centery))

    # Update Delay Debug
    #speed_value_surface = font.render(str(update_delay), True, Colors.white)
    #screen.blit(speed_value_surface, (600, 500, 50, 50))

    
    
    game.draw(screen)
    # Game over screen
    if game.is_game_over():
        game.stop_music()
        screen.blit(game_over_surface, (10, 290, 50, 50))

    # Update game loop
    pygame.display.update()
    clock.tick(60)
    
