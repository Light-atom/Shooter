#Создай собственный Шутер!

from pygame import *
from random import *
from time import time as timer #импортируем функцию для засекания времени, чтобы интерпретатор не искал эту функцию в pygame модуле time, даём ей другое название сами


class GameSprite(sprite.Sprite):

    def __init__(self, player_image, player_x, player_y, size_X, size_Y, player_speed = 3):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(size_X, size_Y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.speed = player_speed
        

    def blid(self):
        window.blit(self.image,(self.rect.x, self.rect.y))



class Player(GameSprite):

    def move(self):
        keys_pressed = key.get_pressed()

        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 915:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx - 25, self.rect.top - 25, 50, 50, -10)
        Bullet_Group.add(bullet)


class Bullet(GameSprite):
        
    def update(self):
        
        self.rect.y += self.speed 

        if self.rect.y == 0:
            self.kill() 


Bullet_Group = sprite.Group()


class Enemy(GameSprite):

    def update(self):
        self.rect.y += self.speed

        global lose 
        if self.rect.y > 900:
            self.rect.y = 0
            self.rect.x = randint(15, 985)
            lose += 1 

class Asteroid(GameSprite):

    def update(self):
        self.rect.y += self.speed

        
        if self.rect.y > 900:
            self.rect.y = 0
            self.rect.x = randint(15, 985)
            



Enemy_group = sprite.Group()
        
for i in range(5):
    Enemy_i = Enemy("ufo.png", randint(15, 985), 0, 80, 50, randint(3, 5))
    Enemy_group.add(Enemy_i)
    """num = randint(0, 2) 
    
    if num == 0 :  
        Enemy_i = Enemy("ufo.png", randint(15, 985), 0, 80, 50, randint(3, 5))
        Enemy_group.add(Enemy_i)

    if num == 1 : 

        Enemy_i = Enemy("ufo.png", randint(15, 985), 0, 40, 25, randint(5, 7))
        Enemy_group.add(Enemy_i)

    if num == 2 : 

        Enemy_i = Enemy("ufo.png", randint(15, 985), 0, 160, 100, randint(1, 2))
        Enemy_group.add(Enemy_i)"""

Asteroid_group = sprite.Group()
for i in range(3):
    Asteroid_i = Asteroid("asteroid.png", randint(15, 985), 0, 80, 50, randint(3, 5))
    Asteroid_group.add(Asteroid_i)

window = display.set_mode((1000, 800))
display.set_caption("Шутер")
background = transform.scale(image.load("galaxy.jpg"), (1000, 800))

#текст 
font.init()
Text = font.Font(None, 35)


#Музыка-фон 

mixer.init()
mixer.music.load("space.ogg")
# mixer.music.play() # отключил 

#Игровые эффекты 
fire = mixer.Sound("fire.ogg")
kick = mixer.Sound("kick.ogg")



#Sprite ! 

Player_game  = Player("rocket.png", 380, 660, 120, 140, 15)


#игровой цикл
health = 5
reload_bullet = 5
lose_player_to_enemy = 0 
lose = 0
score = 0
finish = False
run = True
clock = time.Clock()
FPS = 60

while run:

    

    for e in event.get():
        if e.type == QUIT:
            run = False
    
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                reload_bullet -= 1
                if reload_bullet == 0: 
                    text = Text.render('Wait, reload...', True, (255 , 0, 0))
                    window.blit(text, (500, 800))
                    start_time = timer()
                Player_game.fire()
                fire.play()
                
    if finish != True:
        
        window.blit(background,(0, 0))
        Player_game.blid()
        Player_game.move()

        Bullet_Group.draw(window)
        Bullet_Group.update()

        Asteroid_group.draw(window)
        Asteroid_group.update()

        Enemy_group.draw(window)
        Enemy_group.update()

        text_lose_score = Text.render("Пропущено:"+str(lose), True, (255, 255, 255))
        healt = Text.render(str(health), True, (0, 255, 0))
        
        window.blit(text_lose_score, (10, 50))
        window.blit(healt, (900, 50))

        sprite_list = sprite.groupcollide ( Enemy_group, Bullet_Group, True, True)
        player_to_enemy = sprite.spritecollide(Player_game,Enemy_group, False)
        player_to_asteroid = sprite.spritecollide(Player_game, Asteroid_group, True)


        for i in player_to_enemy:
            lose_player_to_enemy += 1
            kick.play()

        for i in player_to_asteroid: 
            health -= 1
            kick.play()
            for i in range(1):
                Asteroid_i = Asteroid("asteroid.png", randint(15, 985), 0, 80, 50, randint(3, 5))
                Asteroid_group.add(Asteroid_i)

            Asteroid_group.draw(window)
            Asteroid_group.update()

        for i in sprite_list: 
            score += 1
            Enemy_i = Enemy("ufo.png", randint(15, 985), 0, 80, 50, randint(1, 5))
            Enemy_group.add(Enemy_i)
            

        if lose == 10:
            text_lose1 = Text.render("Вы проиграли !", True, (255, 0, 0))
            text_lose2 = Text.render("Вы пропустили 10 НЛО!", True, (255, 0, 0))
            window.blit(text_lose1, (400, 400))
            window.blit(text_lose2, (400, 425))
            finish = True

        if lose_player_to_enemy == 1: 
            text_lose_player1 = Text.render("Вы проиграли !", True, (255, 0, 0))
            text_lose_player2 = Text.render("Вы врезались НЛО!", True, (255, 0, 0))
            window.blit(text_lose_player1, (400, 400))
            window.blit(text_lose_player2, (400, 425))
            finish = True 

        if health == 0: 
            text_lose_player1 = Text.render("Вы проиграли !", True, (255, 0, 0))
            text_lose_player2 = Text.render("Вы потеряли все жизни ", True, (255, 0, 0))
            window.blit(text_lose_player1, (400, 400))
            window.blit(text_lose_player2, (400, 425))
            finish = True 

        if score == 10 :
            text_win1 = Text.render("Вы выйграли !", True, (0, 255, 0))
            text_win2 = Text.render("Вы повергли 10 монстров !", True, (0, 255, 0))
            window.blit(text_win1, (400, 400))
            window.blit(text_win2, (400, 425))
            finish = True

        text_win_score = Text.render("Счет:"+str(score),True, (255, 255, 255))
        window.blit(text_win_score, (10, 25))
        display.update()
        
        clock.tick(FPS)