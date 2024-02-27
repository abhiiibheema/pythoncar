import pygame
import time
import math
import random

RED_CAR = pygame.transform.scale(pygame.image.load("car1.png"), (int(150 * 0.55), int(84 * 0.55)))
coin_image = pygame.image.load("coin.png")
coin_image = pygame.transform.scale(coin_image, (50, 30))
BLACK_CAR = pygame.transform.scale(pygame.image.load("car2.png"),(int(150 * 0.55), int(84 * 0.55)))
BULLET_VEL = 4
WIDTH, HEIGHT = 900, 500

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game!")

FPS = 60

class AbstractCar:
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.1

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel
        self.img = pygame.transform.rotate(self.IMG, self.angle)

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

    def move_backward(self):
        self.vel = 4
        self.move()

    def move_forward(self):
        self.vel = -4
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal
        
class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = coin_image
        self.width = self.img.get_width()
        self.height = self.img.get_height()

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))


def is_collision(obj1, obj2):
    obj1_rect = pygame.Rect(obj1.x, obj1.y, obj1.img.get_width(), obj1.img.get_height())
    obj2_rect = pygame.Rect(obj2.x, obj2.y, obj2.width, obj2.height)
    return obj1_rect.colliderect(obj2_rect)

class PlayerCar(AbstractCar):
    IMG = RED_CAR
    START_POS = (180, 200)

class EnemyCar(AbstractCar):
    IMG = BLACK_CAR
    START_POS = (WIDTH - 180, HEIGHT - 200)  # Starting position for the enemy car

def draw(win, player_car, enemy_car, coins):
    win.fill((255, 255, 255))
    for coin in coins:
        coin.draw(win)
    player_car.draw(win)
    enemy_car.draw(win)
    pygame.display.update()

def spawn_coin():
    x = random.randint(50, WIDTH - 50)
    y = random.randint(50, HEIGHT - 50)
    return Coin(x, y)

run = True
clock = pygame.time.Clock()
player_car = PlayerCar(4, 4)
enemy_car = EnemyCar(4, 4)
coins = [spawn_coin()]  # Start with one initial coin
score = 0

while run:
    clock.tick(FPS)

    draw(WIN, player_car, enemy_car, coins)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    moved_player = False
    moved_enemy = False

    if keys[pygame.K_a]:
        player_car.rotate(left=True)
    if keys[pygame.K_d]:
        player_car.rotate(right=True)
    if keys[pygame.K_w]:
        moved_player = True
        player_car.move_forward()
    if keys[pygame.K_s]:
        moved_player = True
        player_car.move_backward()

    if keys[pygame.K_LEFT]:
        enemy_car.rotate(left=True)
    if keys[pygame.K_RIGHT]:
        enemy_car.rotate(right=True)
    if keys[pygame.K_UP]:
        moved_enemy = True
        enemy_car.move_forward()
    if keys[pygame.K_DOWN]:
        moved_enemy = True
        enemy_car.move_backward()

    # Collision detection with player car
    for coin in coins[:]:
        if is_collision(player_car, coin):
            coins.remove(coin)
            score += 1
            coins.append(spawn_coin())  # Spawn a new coin when collected

    # Collision detection with enemy car
    for coin in coins[:]:
        if is_collision(enemy_car, coin):
            coins.remove(coin)
            coins.append(spawn_coin())  # Spawn a new coin when collected

    pygame.display.set_caption("Racing Game! - Score: {}".format(score))
    pygame.display.update()

pygame.quit()