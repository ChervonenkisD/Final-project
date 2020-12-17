import pygame
import random

GREY = (170, 170, 170)
WHITE = (255, 255, 255)
BLAC = (29, 29, 29)

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 900
FPS = 30

class Player(pygame.sprite.Sprite):
    
    def __init__(self, x, y, img='player.png'):
        super().__init__()
        
        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.change_x = 0
        self.change_y = 0
        self.walls = None
        
        self.coins = None
        self.collected_coins = 0
        
        self.enemies = pygame.sprite.Group()
        self.alive = True
        
    def update(self):
        self.rect.x += self.change_x
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                self.rect.left = block.rect.right
                
        self.rect.y += self.change_y
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom
                
        coins_hit_list = pygame.sprite.spritecollide(self, self.coins, False)
        for coin in coins_hit_list:
            self.collected_coins += 1
            coin.kill()
            
        if pygame.sprite.spritecollideany(self, self.enemies, False):
            self.alive = False
            
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        
        self.image = pygame.Surface([width, height])
        self.image.fill(BLAC)
        
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, img='coin.png'):
        super().__init__()
        
        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, img='enemy.png'):
        super().__init__()
        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.start = x
        self.stop = x + random.randint(180, 240)
        self.direction = 1
        
    def update(self):
        if self.rect.x >= self.stop:
            self.rect.x = self.stop
            self.direction = -1
        if self.rect.x <= self.start:
            self.rect.x = self.start
            self.direction = 1
        self.rect.x += self.direction*2
pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption('Maze')


all_sprite_list = pygame.sprite.Group()
wall_list = pygame.sprite.Group()

wall_coords = [
    [0, 890, 1400, 10],
    [0, 0, 10, 900],
    [500, 375, 10, 900],
    [900, 825, 10, 75],
    [1000, 825, 10, 75],
    [1000, 825, 200, 10],
    [600, 750, 10, 75],
    [600, 825, 200, 10],
    [1390, 0, 10, 900],
    [500, 375, 400, 10],
    [0, 0, 1400, 10],
    [0, 150, 300, 10],
    [0, 225, 200, 10],
    [300, 75, 10, 150],
    [300, 75, 200, 10],
    [500, 75, 10, 150],
    [400, 150, 10, 75],
    [400, 225, 100, 10],
    [500, 75, 10, 150],
    [300, 300, 600, 10],
    [600, 0, 10, 75],
    [600, 75, 200, 10],
    [600, 150, 200, 10],
    [600, 150, 10, 150],
    [700, 225, 200, 10],
    [900, 0, 10, 300],
    [1000, 0, 10, 450],
    [600, 450, 300, 10],
    [600, 525, 200, 10],
    [600, 750,100, 10],
    [600, 450, 10, 225],
    [700, 600, 100, 10],
    [700, 600, 10, 150],
    [1000, 525, 400, 10],
    [1000, 525, 10, 225],
    [1000, 750, 200, 10],
    [1200, 600, 10, 150],
    [1100, 75, 10, 375],
    [1100, 75, 200, 10],
    [1100, 225, 200, 10],
    [1100, 300, 100, 10],
    [1100, 450, 300, 10],
    [1300, 75, 10, 75],
    [1300, 225, 10, 75],
    [1300, 375, 10, 75],
    [1200, 150, 100, 10],
    [1200, 375, 100, 10],
    [900, 450, 10, 300],
    [800, 600, 10, 150],
]
for coord in wall_coords:
    wall = Wall(coord[0], coord[1], coord[2], coord[3])
    wall_list.add(wall)
    all_sprite_list.add(wall)
    
    
coins_list = pygame.sprite.Group()
coins_coord = [[250, 75], [100, 450], [360, 675], [800, 112.5], [800, 525], [850, 412,5], [900, 787.5], [1100, 37.5], [1100,600], [1250, 300], [1300, 675], [1350, 150]]

for coord in coins_coord:
    coin = Coin(coord[0], coord[1])
    coins_list.add(coin)
    all_sprite_list.add(coin)
    
enemies_list = pygame.sprite.Group()
enemies_coord = [[10, 500], [500, 75]]
for coord in enemies_coord:
    enemy = Enemy(coord[0], coord[1])
    enemies_list.add(enemy)
    all_sprite_list.add(enemy)
    
    
player = Player(50, 50)
player.walls = wall_list
all_sprite_list.add(player)

player.coins = coins_list

player.enemies = enemies_list

font = pygame.font.SysFont('Arial', 24, True)
text = font.render('Game Over', True, WHITE)
text_vin = font.render('the maze is completed', True, WHITE)

clock = pygame.time.Clock()
done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.change_x = -3
            elif event.key == pygame.K_RIGHT:
                player.change_x = 3
            elif event.key == pygame.K_UP:
                player.change_y = -3
            elif event.key == pygame.K_DOWN:
                player.change_y = 3
                
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.change_x = 0
            elif event.key == pygame.K_RIGHT:
                player.change_x = 0
            elif event.key == pygame.K_UP:
                player.change_y = 0
            elif event.key == pygame.K_DOWN:
                player.change_y = 0
    screen.fill(GREY)
    
    if not player.alive:
        screen.blit(text, (100, 100))
    else:
        all_sprite_list.update()
        all_sprite_list.draw(screen)
        
        
    pygame.display.flip()
    clock.tick(60)

pygeme.quit()
