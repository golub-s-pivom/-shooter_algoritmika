
from pygame import *

win_width, win_height = 800, 600

class GameSprite(sprite.Sprite):
    def __init__(self, sprite_image, sprite_x, sprite_y, sprite_speed):
        super().__init__()
        self.image = transform.scale(image.load(sprite_image), (65, 65))
        self.speed = sprite_speed
        self.rect = self.image.get_rect()
        self.rect.x = sprite_x
        self.rect.y = sprite_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 65:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 65:
            self.rect.y += self.speed

class Enemy(GameSprite):
    def __init__(self,sprite_image,sprite_x,sprite_y, sprite_speed):
        super().__init__(sprite_image,sprite_x,sprite_y, sprite_speed)
        self.side = "left"
    def update(self):
        if self.rect.x <= 390:
           self.side = "right"
        elif self.rect.x >= win_width - 85:
            self.side = "left"
        
        if self.side == "left":
            self.rect.x -= self.speed
        elif self.side == "right":
            self.rect.x += self.speed


class Wall(sprite.Sprite):
    def __init__(self, color_red,color_blue, color_green,wall_width,wall_height,wall_x,wall_y):
        self.image = Surface((wall_width,wall_height))
        self.image.fill((color_red,color_blue,color_green))
        self.rect = self.image.get_rect()
        self.rect.y = wall_y
        self.rect.x = wall_x
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

window = display.set_mode((win_width, win_height))
display.set_caption('Maze')
background = transform.scale(image.load("background.jpg"),(win_width, win_height))

player = Player("hero.png", 5, win_height - 80, 10)
enemy = Enemy("cyborg.png", win_width - 80, 280, 30)
treasure = GameSprite("treasure.png", win_width - 700, win_height - 400, 0)

wo1 = Wall(154,205,50,800,15,0,10)
wo2 = Wall(154,205,50,15,390,350,115)
wo3 = Wall(154,205,50,350,15,10,380)

FPS = 60
game = True

clock = time.Clock()

font.init()
font = font.Font(None, 70)

win = font.render('you win', True, (50, 205, 50))
lose = font.render('you lose', True, (255,0,0))

while game:
    window.blit(background,(0,0))
    for e in event.get():
        if e.type == QUIT:
            game = False
    
    player.update()
    enemy.update()
    treasure.update()

    player.reset()
    enemy.reset()
    treasure.reset()

    wo1.reset()
    wo2.reset()
    wo3.reset()

    if sprite.collide_rect(player,wo1) or sprite.collide_rect(player,wo2) or sprite.collide_rect(player,wo3) or sprite.collide_rect(player,enemy):
        game = False
        window.blit(lose, (200,200))

    if sprite.collide_rect(player, treasure):
        game = False
        window.blit(win (200,200))

    display.update()
    clock.tick(FPS)

