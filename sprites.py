# File created by Chris D'Amico


import pygame as pg
from pygame.sprite import Sprite
from settings import *



# write a player class
class Player(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.player
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE

    # def move(self, dx=0, dy=0):
    #     self.x += dx
    #     self.y += dy
        
    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = PLAYER_SPEED
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y



    def update(self):
        # self.rect.x = self.x * TILESIZE
        # self.rect.y = self.y * TILESIZE
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        # add x collision later
        self.collide_with_walls('x')
        self.rect.y = self.y
        # add y collision later
        self.collide_with_walls('y')
        

class Wall(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Mob(Sprite):
    def __init__(self, game, x, y, speed):
        self.groups = game.all_sprites, game.mob
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)  # Set the mob color to red
        self.rect = self.image.get_rect()
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = speed
        self.direction = 1  # 1 for right, -1 for left
        
    # def move(self):
    #     self.x += self.speed * self.direction

    # def check_collision(self):
        # hits = pg.sprite.spritecollide(self, self.game.player, False)
        # if hits:
        #     print("Player killed!")
        #     self.kill()
    #     pass

    # def check_wall_collision(self):
    #     hits = pg.sprite.spritecollide(self, self.game.walls, False)
    #     if hits:
    #         for wall in hits:
    #             if self.direction == 1:
    #                 self.direction = -1
    #                 self.rect.right = wall.rect.left
    #             elif self.direction == -1:
    #                 self.direction = 1
    #                 self.rect.left = wall.rect.right

    # def update(self):
    #     self.move()
    #     self.check_collision()
    #     self.check_wall_collision()
    #     self.rect.x = self.x
    #     self.rect.y = self.y
