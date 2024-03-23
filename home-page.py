import pygame
from sys import exit

def display_score():

    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f"score: {current_time}", False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time

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

# Load snail surface and define rectangle
snail_surf = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
snail_rect = snail_surf.get_rect(bottomright=(600, 300))

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

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:  # If mouse is clicked
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
                    # If player is clicked and grounded
                    player_gravity = -20  # Apply upward velocity to jump
            if event.type == pygame.KEYDOWN:  # If a key is pressed
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    # If spacebar is pressed and grounded
                    player_gravity = -20  # Apply upward velocity to jump
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE or event.type == pygame.MOUSEBUTTONDOWN:
                # If spacebar is pressed
                game_active = True  # Set game to active
                snail_rect.left = 800  # Reset snail position
                start_time = int(pygame.time.get_ticks() / 1000)

    if game_active:
        # Draw everything on the screen
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        score = display_score()
        
        # Update snail position
        snail_rect.x -= 5
        if snail_rect.right <= 0:
            snail_rect.left = 800
        screen.blit(snail_surf, snail_rect)

        # Apply gravity to player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            # If player is below the ground
            player_rect.bottom = 300  # Set player to ground level
            player_gravity = 0  # Reset gravity
        
        screen.blit(player_surf, player_rect)  # Render walking animation
        
        # Check collision between player and snail
        if player_rect.colliderect(snail_rect):
            game_active = False

    else:
        # If game is not active (collision occurred), fill screen with a color
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)  # Render standing image
        score_massage =test_font.render(f"your score:  {score}",False,(111,196,169))
        score_massage_rect = score_massage.get_rect(center = (400,330))
        screen.blit(game_name, game_name_rect)
        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_massage,score_massage_rect)

    # Update the display
    pygame.display.update()

    # Tick clock to control frame rate
    clock.tick(60)
