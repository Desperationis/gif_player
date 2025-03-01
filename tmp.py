import pygame
import os
from pygame._sdl2 import Window  # For window maximization

# Configuration (adjust these values)
FRAME_FOLDER = "gif_frames"  # Folder containing individual frames
DESIRED_WIDTH = 400          # Animation width in pixels
DESIRED_HEIGHT = 800         # Animation height
FRAME_DELAY = 10            # Milliseconds between frames (lower = faster)
BACKGROUND_COLOR = (255, 255, 255)  # White background

# Initialize Pygame
pygame.init()

# Create maximized window
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
Window.from_display_module().maximize()  # SDL2 method for maximization [1][7]

# Load animation frames
gif_frames = []
try:
    for filename in sorted(os.listdir(FRAME_FOLDER)):
        if filename.lower().endswith(('.png', '.jpg', '.bmp')):
            img = pygame.image.load(os.path.join(FRAME_FOLDER, filename)).convert_alpha()
            img = pygame.transform.scale(img, (DESIRED_WIDTH, DESIRED_HEIGHT))
            gif_frames.append(img)
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

