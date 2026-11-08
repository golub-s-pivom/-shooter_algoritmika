
from pygame import *
from random import randint


font.init()
font1 = font.Font(None, 36)
mixer.init()
win_width, win_height = 700, 500
global lost
lost = 0
killed = 0

class GameSprite(sprite.Sprite):
    def __init__(self, sprite_image, sprite_x, sprite_y, sprite_speed,w,h):
        super().__init__()
        self.image = transform.scale(image.load(sprite_image), (w,h))
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
    def fire(self):
        bullet = Bullet('bullet.png',self.rect.centerx-10,self.rect.top,6,20,40)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80,win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
fire_sond = mixer.Sound('fire.ogg')

player = player = Player("rocket.png", 5, win_height - 80, 10,65,65)
monsters = sprite.Group()
count_m = 5
y_cor=-10
for i in range(count_m):
    x_cor = randint(0,win_width)
    speed = randint(1,3)
    monster = Enemy('ufo.png',x_cor,y_cor,speed,65,65)
    monsters.add(monster)
bullets = sprite.Group()
window = display.set_mode((win_width, win_height))
display.set_caption('Молодой шутерок')
background = transform.scale(image.load("galaxy.jpg"),(win_width,win_height ))

FPS = 60
clock = time.Clock()
mixer.music.load('space.ogg')
mixer.music.play()
game = True
while game:
    if killed or lost >= 10:
        game =  False
        



    window.blit(background,(0,0))
    player.reset()
    
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
                fire_sond.play()
    player.update()
    monsters.draw(window)
    monsters.update()
    bullets.draw(window)
    bullets.update()
    text_lose = font1.render( 'Пропущено:' + str(lost), 1, (255,255,255))
    kill_text = font1.render('Убито:' + str(killed), 1,(255,255,255))
    window.blit(text_lose,(0,0))
    window.blit(kill_text,(0,50))


    collides = sprite.groupcollide(monsters, bullets, True, True)
    for enemy in collides: 
        killed += 1

    display.update()
    clock.tick(FPS)
if killed >= 10:
    game = False
    win_text = font1.render('Чё за огузки', True, (50, 205, 50))
    window.blit(win_text, (win_width // 2 - 150, win_height // 2))
    display.update()
    time.wait(2000)

if lost >= 10:
    game = False
    lose_text = font1.render('Ты пойман мексиканской пиньятой', True, (255, 0, 0))
    window.blit(lose_text, (win_width // 2 - 150, win_height // 2))
    display.update()
    time.wait(2000)
    

