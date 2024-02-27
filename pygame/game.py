import pygame
import random
import client

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
CAR_SPEED = 5
BULLET_VEL = 3  # Adjusted bullet speed
MAX_BULLETS = 999

# Colors
WHITE = (255, 255, 255)

# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Two Cars Game")
clock = pygame.time.Clock()

# Load car images
car1_image = pygame.image.load("car1.png")
car2_image = pygame.image.load("car2.png")
coin_image = pygame.image.load("coin.png")
target_image = pygame.image.load('target.png')

# Resize images
car1_image = pygame.transform.scale(car1_image, (50, 30))
car2_image = pygame.transform.scale(car2_image, (50, 30))
coin_image = pygame.transform.scale(coin_image, (20, 20))
target_image = pygame.transform.scale(target_image, (50, 20))

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.points = 0
        self.bullets = pygame.sprite.Group()
        self.angle = 0
        self.rotation_vel = 5  # Rotation velocity
        self.vel = 0
        self.acceleration = 0.1
        self.max_vel = 10

    def update(self):
        # Keep the player inside the screen
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH - self.rect.width, HEIGHT - self.rect.height))

        # Rotate the image based on the angle
        self.image = pygame.transform.rotate(self.original_image, self.angle)

        # Move the player in the direction they are facing
        dx = self.vel * round(pygame.math.cos(pygame.math.radians(self.angle)))
        dy = self.vel * round(pygame.math.sin(pygame.math.radians(self.angle)))
        self.rect.x += dx
        self.rect.y += dy

    def shoot(self):
        # Create a new bullet with the player's current angle
        new_bullet = Bullet(self.rect.centerx, self.rect.centery, self.angle)
        self.bullets.add(new_bullet)
        all_sprites.add(new_bullet)

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        print(self.vel)
        self.update()

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.update()

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.angle = angle

    def update(self):
        # Update the bullet position based on the angle
        if self.angle == 180:
            self.rect.y -= BULLET_VEL
        elif self.angle == 360:
            self.rect.y += BULLET_VEL
        elif self.angle == 270:
            self.rect.x -= BULLET_VEL
        elif self.angle == 90:
            self.rect.x += BULLET_VEL

# Coin class
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = coin_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - 20)
        self.rect.y = random.randint(0, HEIGHT - 20)

# Target class
class Target(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = target_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - 50)
        self.rect.y = random.randint(0, HEIGHT - 20)

# Sprite groups
all_sprites = pygame.sprite.Group()
players = pygame.sprite.Group()
coins = pygame.sprite.Group()
targets = pygame.sprite.Group()

# Create players
player1 = Player(car1_image, 100, 100)
player2 = Player(car2_image, 700, 500)
players.add(player1, player2)
all_sprites.add(player1, player2)

# Create coins
for _ in range(5):
    coin = Coin()
    coins.add(coin)
    all_sprites.add(coin)

# Create target
target = Target()
targets.add(target)
all_sprites.add(target)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle shooting events for player 1
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LCTRL and len(player1.bullets) < MAX_BULLETS:
            player1.shoot()

        # Handle shooting events for player 2
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RCTRL and len(player2.bullets) < MAX_BULLETS:
            player2.shoot()

    keys1 = pygame.key.get_pressed()
    keys2 = pygame.key.get_pressed()

    # Player 1 controls (WASD)
    if keys1[pygame.K_w]:
        player1.move_forward()
    if keys1[pygame.K_s]:
        player1.reduce_speed()
    if keys1[pygame.K_a]:
        player1.rotate(left=True)
    if keys1[pygame.K_d]:
        player1.rotate(right=True)

    # Player 2 controls (Arrow keys)
    if keys2[pygame.K_UP]:
        player2.move_forward()
    if keys2[pygame.K_DOWN]:
        player2.reduce_speed()
    if keys2[pygame.K_LEFT]:
        player2.rotate(left=True)
    if keys2[pygame.K_RIGHT]:
        player2.rotate(right=True)

    # Keep the players inside the screen
    player1.rect.clamp_ip(pygame.Rect(0, 0, WIDTH - player1.rect.width, HEIGHT - player1.rect.height))
    player2.rect.clamp_ip(pygame.Rect(0, 0, WIDTH - player2.rect.width, HEIGHT - player2.rect.height))

    # Update bullets
    player1.bullets.update()
    player2.bullets.update()

    # Check for collisions with bullets and target
    bullet_hits1 = pygame.sprite.spritecollide(target, player1.bullets, True)
    bullet_hits2 = pygame.sprite.spritecollide(target, player2.bullets, True)
    # Update player points based on bullet hits
    player1.points += len(bullet_hits1)
    player2.points += len(bullet_hits2)

    # Check for collisions with players
    player1_hit = pygame.sprite.spritecollide(player1, player2.bullets, True)
    player2_hit = pygame.sprite.spritecollide(player2, player1.bullets, True)
    # Update player points based on bullet hits on players
    player1.points += len(player1_hit)
    player2.points += len(player2_hit)

    # Check for collisions with coins
    coin_hits1 = pygame.sprite.spritecollide(player1, coins, True)
    coin_hits2 = pygame.sprite.spritecollide(player2, coins, True)
    # Check for collisions with target
    target_hit1 = pygame.sprite.spritecollide(player1, targets, False)
    target_hit2 = pygame.sprite.spritecollide(player2, targets, False)
    # Update player points
    player1.points += len(coin_hits1)
    player2.points += len(coin_hits2)

    # Spawn new coins
    for _ in range(5 - len(coins)):
        coin = Coin()
        coins.add(coin)
        all_sprites.add(coin)

    # Draw everything
    screen.fill(WHITE)
    all_sprites.draw(screen)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit the game
pygame.quit()
