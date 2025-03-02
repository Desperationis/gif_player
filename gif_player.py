import pygame
import os
from pygame._sdl2 import Window  # For window maximization

import pygame
import os
from pygame._sdl2 import Window

# Configuration (adjust these values)
FRAME_FOLDER = "gif_frames"
DESIRED_WIDTH = 300
DESIRED_HEIGHT = 1000
FRAME_DELAY = 10
BACKGROUND_COLOR = (255, 255, 255)
ROTATION_DEGREE = 0  # New: Set rotation angle in degrees (0 for no rotation)
PRESERVE_ASPECT_RATIO = True  # New: Maintain original width/height ratio

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)


gif_frames = []

try:
    for filename in sorted(os.listdir(FRAME_FOLDER)):
        if filename.lower().endswith(('.png', '.jpg', '.bmp')):
            img = pygame.image.load(os.path.join(FRAME_FOLDER, filename)).convert_alpha()
            
            # Aspect ratio preservation logic [4][7]
            if PRESERVE_ASPECT_RATIO:
                original_ratio = img.get_height() / img.get_width()
                new_height = int(DESIRED_WIDTH * original_ratio)
            else:
                new_height = DESIRED_HEIGHT

            scaled_img = pygame.transform.scale(img, (DESIRED_WIDTH, new_height))
            
            # Rotation logic [3][5][6]
            rotated_img = pygame.transform.rotate(scaled_img, ROTATION_DEGREE)
            gif_frames.append(rotated_img)
except FileNotFoundError:
    print(f"Error: Frame folder '{FRAME_FOLDER}' not found!")
    pygame.quit()
    exit()

# Animation state
current_frame = 0
last_update = pygame.time.get_ticks()
clock = pygame.time.Clock()
running = True

# Main loop
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # [3][8]
            running = False

    # Update animation frame
    now = pygame.time.get_ticks()
    if now - last_update >= FRAME_DELAY:
        current_frame = (current_frame + 1) % len(gif_frames)
        last_update = now

    # Draw frame
    screen.fill(BACKGROUND_COLOR)
    if gif_frames:
        frame_rect = gif_frames[current_frame].get_rect(
            center=(screen.get_width()//2, screen.get_height()//2)
        )
        screen.blit(gif_frames[current_frame], frame_rect)

    pygame.display.flip()
    clock.tick(60)  # Main loop FPS

pygame.quit()

