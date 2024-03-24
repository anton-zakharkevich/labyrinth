from pygame import *

clock = time.Clock()
FPS = 60

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 595:
            self.rect.x += self.speed
        if keys_pressed[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys_pressed[K_DOWN] and self.rect.y < 395:
            self.rect.y += self.speed

class Enemy(GameSprite):
    def update(self):
        if self.rect.x <= 470:
            self.direction = 'right'
        if self.rect.x >= width - 85:
            self.direction = 'left'

        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_y, wall_x, wall_width, wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.height = wall_height
        self.image = Surface((self.width, self.height))
        self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

window = display.set_mode((700, 500))
display.set_caption('Лабиринт')
background = transform.scale(image.load('background.jpg'), (700, 500))
game = True
mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()

height = 500
width = 700

player = Player('hero.png',5, height -80, 4)
monster = Enemy('cyborg.png', width -80, 280, 2)
final = GameSprite('treasure.png', width -120, height -80, 0)
wall = Wall(120, 230, 180, 100, 80, 20, 400)
wall2 = Wall(120, 230, 180, 0, 190, 20, 385)
wall3 = Wall(120, 230, 180, 385, 190, 150, 3)
wall4 = Wall(120, 230, 180, 100, 450, 20, 400)
#wall5 = Wall(120, 230, 180, 100, )
finish = False
font.init()
font = font.SysFont('Arial', 70)
win = font.render('YOU WIN!', True, (255, 215, 0))
lose = font.render('YOU LOSE!', True, (180, 0, 0))

money = mixer.Sound('money.ogg')
kick = mixer.Sound('kick.ogg')
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    if finish != True:
        window.blit(background,(0, 0))
        player.reset()
        player.update()
        monster.reset()
        monster.update()
        wall.draw_wall()
        wall2.draw_wall()
        wall3.draw_wall()
        wall4.draw_wall()
        final.reset()
        if sprite.collide_rect(player, monster) or sprite.collide_rect(player, wall) or sprite.collide_rect(player, wall3) or sprite.collide_rect(player, wall2) or sprite.collide_rect(player, wall4):
            finish = True
            window.blit(lose, (200, 200))
            kick.play()
        if sprite.collide_rect(player, final):
            finish = True
            window.blit(win, (200, 200))
            money.play()

    display.update()
    clock.tick(FPS)

