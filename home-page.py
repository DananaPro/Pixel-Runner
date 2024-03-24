import pygame
from sys import exit
from random import randint

# Function to display the score
def display_score():
    # Calculate current score based on elapsed time
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    # Render the score surface
    score_surf = test_font.render(f"Score: {current_time}", False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    # Display the score surface on the screen
    screen.blit(score_surf, score_rect)
    return current_time

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

# Function to move obstacles
def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            # If the obstacle is a snail, blit the snail image; otherwise, blit the fly image
            if obstacle_rect.bottom == 300:
                screen.blit(snail_surf, obstacle_rect)
            else:
                screen.blit(fly_surf, obstacle_rect)

        # Remove obstacles that have moved off the screen
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else:
        return []

# Initialize pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Runner")

# Set up the clock
clock = pygame.time.Clock()

# Load font
test_font = pygame.font.Font("font/Pixeltype.ttf", 50)

# Flag to indicate if the game is active
game_active = False
start_time = 0
score = 0

# Load images
sky_surface = pygame.image.load("graphics/sky.png").convert_alpha()
ground_surface = pygame.image.load("graphics/ground.png").convert_alpha()

# Load snail and fly surfaces
snail_surf = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
fly_surf = pygame.image.load("graphics/fly/fly1.png").convert_alpha()

# Initialize the list of obstacle rectangles
obstacle_rect_list = []

# Load player surface and define player rectangle
player_surf = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
player_rect = player_surf.get_rect(midbottom=(80, 300))
player_gravity = 0

# Load player standing surface and define player standing rectangle
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))

# Game name and message
game_name = test_font.render('Pixel Runner', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(400, 80))
game_message = test_font.render("Press space to run", False, (111, 196, 169))
game_message_rect = game_message.get_rect(center=(400, 320))

# Timer for generating obstacles
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500) 

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:  # If mouse is clicked
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
                    # If player is clicked and grounded, make it jump
                    player_gravity = -20  # Apply upward velocity to jump
            if event.type == pygame.KEYDOWN:  # If a key is pressed
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    # If spacebar is pressed and grounded, make it jump
                    player_gravity = -20  # Apply upward velocity to jump
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE or event.type == pygame.MOUSEBUTTONDOWN:
                # If spacebar is pressed, start the game
                game_active = True  # Set game to active
                start_time = int(pygame.time.get_ticks() / 1000)

        if event.type == obstacle_timer and game_active:
            if randint(0, 2):
                # Generate snail obstacles at regular intervals
                obstacle_rect_list.append(snail_surf.get_rect(bottomright=(randint(900, 1100), 300)))
            else:
                # Generate fly obstacles at regular intervals
                obstacle_rect_list.append(fly_surf.get_rect(bottomright=(randint(900, 1100), 210)))
    
    if game_active:
        # Draw everything on the screen during active gameplay
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        score = display_score()  # Display and update score

        # Apply gravity to player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            # If player is below the ground, keep it on the ground
            player_rect.bottom = 300            
        screen.blit(player_surf, player_rect)  # Render walking animation
        
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        
        # Check collision between player and snail
        game_active = collisions(player_rect, obstacle_rect_list)
        
    else:
        # Display game over message when the game is not active
        screen.fill((94, 129, 162))  # Fill screen with a color
        screen.blit(player_stand, player_stand_rect)  # Render standing image
        obstacle_rect_list.clear()
        player_rect.midbottom = (80,300)
        
        
        score_message = test_font.render(f"Your score: {score}", False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(400, 330))
        screen.blit(game_name, game_name_rect)
        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    # Update the display
    pygame.display.update()

    # Control frame rate
    clock.tick(60)
