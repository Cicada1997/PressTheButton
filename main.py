import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set window size
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Moving Button")

# Colors
WHITE = (255, 255, 255)
DARK_GREEN = (0, 100, 0)
LIGHT_GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Button properties
BUTTON_WIDTH = 80
BUTTON_HEIGHT = 40
BUTTON_RADIUS = 10
BUTTON_COLOR = DARK_GREEN
BUTTON_TEXT_COLOR = WHITE
BUTTON_TEXT = "Click Me"
BUTTON_FONT = pygame.font.SysFont(None, 24)

# Margin to keep the button inside the window
MARGIN_CURSOR = 300  # Margin from cursor to button
MARGIN_WINDOW = 0  # Margin from window edges to button

# Function to create a button
def create_button(x, y):
    button_rect = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
    pygame.draw.rect(window, BUTTON_COLOR, button_rect, border_radius=BUTTON_RADIUS)

    # Gradient background
    gradient_rect = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT // 2)
    gradient = pygame.Surface((BUTTON_WIDTH, BUTTON_HEIGHT // 2), pygame.SRCALPHA)
    pygame.draw.rect(gradient, (255, 255, 255, 100), gradient_rect)
    window.blit(gradient, gradient_rect)

    # Button text
    text = BUTTON_FONT.render(BUTTON_TEXT, True, BUTTON_TEXT_COLOR)
    text_rect = text.get_rect(center=button_rect.center)
    window.blit(text, text_rect)

    return button_rect

# Function to calculate the distance between two points
def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

# Function to teleport the button to the opposite side
def teleport_to_opposite_side(button_rect, dx, dy):
    if dx > 0:  # Moving right
        button_rect.left = 0
    elif dx < 0:  # Moving left
        button_rect.right = WINDOW_WIDTH
    if dy > 0:  # Moving down
        button_rect.top = 0
    elif dy < 0:  # Moving up
        button_rect.bottom = WINDOW_HEIGHT

# Main function
def main():
    clock = pygame.time.Clock()

    # Initial position of the button
    button_x = random.randint(MARGIN_WINDOW, WINDOW_WIDTH - BUTTON_WIDTH - MARGIN_WINDOW)
    button_y = random.randint(MARGIN_WINDOW, WINDOW_HEIGHT - BUTTON_HEIGHT - MARGIN_WINDOW)
    dx = random.choice([-1, 1])
    dy = random.choice([-1, 1])

    while True:
        window.fill(WHITE)

        # Create the button
        button_rect = create_button(button_x, button_y)

        # Calculate the distance between cursor and button center
        dist = distance(pygame.mouse.get_pos(), button_rect.center)

        # Calculate speed multiplier based on distance (exponential increase)
        speed_multiplier = math.exp((MARGIN_CURSOR - dist) / (MARGIN_CURSOR / 3))  # Faster movement

        # Move the button away from the cursor if it's too close
        if dist < MARGIN_CURSOR:
            diff_x = button_rect.centerx - pygame.mouse.get_pos()[0]
            diff_y = button_rect.centery - pygame.mouse.get_pos()[1]
            angle = math.atan2(diff_y, diff_x)
            dx = int(math.cos(angle) * 2 * speed_multiplier)
            dy = int(math.sin(angle) * 2 * speed_multiplier)

        # Move the button
        button_x += dx
        button_y += dy

        # Teleport the button to the opposite side if it hits an edge
        if button_x > WINDOW_WIDTH - BUTTON_WIDTH:
            button_x = 0
        elif button_x < 0:
            button_x = WINDOW_WIDTH - BUTTON_WIDTH
        if button_y > WINDOW_HEIGHT - BUTTON_HEIGHT:
            button_y = 0
        elif button_y < 0:
            button_y = WINDOW_HEIGHT - BUTTON_HEIGHT

        pygame.display.update()
        clock.tick(60)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

if __name__ == "__main__":
    main()
