import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
GRAVITY = 0.8
JUMP_STRENGTH = -20
PLAYER_SPEED = 5

# Colors
WHITE = (255, 255, 255)
BLUE = (50, 150, 255)
GREEN = (50, 255, 50)
RED = (255, 50, 50)
BROWN = (139, 69, 19)

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 40)
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.color = BLUE
    
    def update(self, platforms):
        # Handle input
        keys = pygame.key.get_pressed()
        self.vel_x = 0
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = PLAYER_SPEED
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.vel_y = JUMP_STRENGTH
            self.on_ground = False
        
        # Apply gravity
        self.vel_y += GRAVITY
        
        # Move horizontally
        self.rect.x += self.vel_x
        self.check_collisions(platforms, 'horizontal')
        
        # Move vertically
        self.rect.y += self.vel_y
        self.check_collisions(platforms, 'vertical')
        
        # Keep player on screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        
        # Reset if player falls off screen
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = 100
            self.rect.y = 400
            self.vel_y = 0
    
    def check_collisions(self, platforms, direction):
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if direction == 'horizontal':
                    if self.vel_x > 0:  # Moving right
                        self.rect.right = platform.rect.left
                    elif self.vel_x < 0:  # Moving left
                        self.rect.left = platform.rect.right
                
                elif direction == 'vertical':
                    if self.vel_y > 0:  # Falling down
                        self.rect.bottom = platform.rect.top
                        self.vel_y = 0
                        self.on_ground = True
                    elif self.vel_y < 0:  # Jumping up
                        self.rect.top = platform.rect.bottom
                        self.vel_y = 0
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        # Draw simple eyes
        pygame.draw.circle(screen, WHITE, (self.rect.x + 8, self.rect.y + 10), 3)
        pygame.draw.circle(screen, WHITE, (self.rect.x + 22, self.rect.y + 10), 3)


class Platform:
    def __init__(self, x, y, width, height, color=BROWN):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Basic Platformer Game")
        self.clock = pygame.time.Clock()
        
        # Create player
        self.player = Player(100, 400)
        
        # Create platforms
        self.platforms = [
            Platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40),  # Ground
            Platform(200, 500, 150, 20),  # Platform 1
            Platform(400, 400, 150, 20),  # Platform 2
            Platform(600, 300, 150, 20),  # Platform 3
            Platform(100, 350, 100, 20),  # Platform 4
            Platform(350, 250, 100, 20),  # Platform 5
        ]
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
        return True
    
    def update(self):
        self.player.update(self.platforms)
    
    def draw(self):
        self.screen.fill(WHITE)
        
        # Draw platforms
        for platform in self.platforms:
            platform.draw(self.screen)
        
        # Draw player
        self.player.draw(self.screen)
        
        # Draw instructions
        font = pygame.font.Font(None, 36)
        text = font.render("Use ARROW KEYS or WASD to move, SPACE/UP to jump", True, (50, 50, 50))
        self.screen.blit(text, (10, 10))
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)  # 60 FPS
        
        pygame.quit()
        sys.exit()

# Run the game
if __name__ == "__main__":
    game = Game()
    game.run()