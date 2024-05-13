# File Created by Chris D'Amico

'''
Sources
- https://github.com/ccozort/cozort_chris_game_engine_Spring_2024/

'''

# Import Libraries and Modular Files
import pygame as pg
import sys
from random import *
from settings import *
from sprites import *
from os import path
import os
from time import *


print(sys.executable)

'''
Goals:
Alpha-
Weapons (add image to sprite) ✅
Shop
Scrolling Map
Music ✅
Settings Menu

Beta-
Player Sprite Shoots Projectiles 
'''

# player = Player
speed = PLAYER_SPEED


class Game:
    # initialize game window
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.images = {}
        self.audio = {}
        self.load_data()


    # def music_player(self):
    #     pg.mixer.music.load(path.join(self.snd_folder, 'bg_music2.mp3'))
    #     pg.mixer.music.play(-1)  # -1 means loop indefinitely
        

    # load game data
    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map_data = []
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)
                print(self.map_data)
                print(enumerate(self.map_data))
        # access files from folders
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, 'image_files')
        self.snd_folder = path.join(self.game_folder, 'audio_assets')

        self.player_img = pg.image.load(path.join(self.img_folder, 'player.png')).convert_alpha()
        self.weapon_img = pg.image.load(path.join(self.img_folder, 'mantis.png')).convert_alpha()
        self.mob_img = pg.image.load(path.join(self.img_folder, 'enemy.jpg')).convert_alpha()
        self.powerup_img = pg.image.load(path.join(self.img_folder, 'maxdoc.jpg')).convert_alpha()
        self.bg_img = pg.image.load(path.join(self.img_folder, 'nightcity.jpg')).convert_alpha()


    # Modify the 'new' method in the Game class to create Mob instances
    def new(self):
        # init all variables, setup groups, instantiate classes
        pg.mixer.music.load(path.join(self.snd_folder, 'bg_music2.mp3'))
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.power_ups = pg.sprite.Group()
        self.foods = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.player = pg.sprite.Group()
        self.weapons = pg.sprite.Group()
        # self.player = Player(self, 10, 10)
        # for x in range(10, 20):
        #     Wall(self, x, 5)
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                # print(col)
                # print(tiles)
                # uses a string character to denote an instance of a game object...
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'U':
                    PowerUp(self, col, row)
                if tile == 'F':
                    Food(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
                if tile == 'W':
                    Weapon(self, col, row, dir)


# defined run method in game engine
    def run(self):
        # music
        # self.music_player()
        pg.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            #image
            # self.image_path()
            # this is input
            self.events()
            # this is processing
            self.update()
            # this output
            self.draw()
            # health bar
            


    def quit(self):
        pg.quit()
        sys.exit()
        # Stop the music when the loop exits  
        pg.mixer.music.stop()
    

    def update(self):
        self.all_sprites.update()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x,0), (x, HEIGHT))
        for y in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0,y), (WIDTH, y))

    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x*TILESIZE,y*TILESIZE)
        surface.blit(text_surface, text_rect)

    def draw(self):
        # Load the background image
        background = pg.image.load(path.join(self.img_folder, 'nightcity.jpg')).convert_alpha()
    
        # Scale the background image to fit the screen
        background = pg.transform.scale(background, (WIDTH, HEIGHT))
    
        # Blit the background image onto the screen
        self.screen.blit(background, (0, 0))
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def draw_health_bar(surf, x, y, pct):
        if pct < 0:
            pct = 0
            BAR_LENGTH = 32
            BAR_HEIGHT = 10
            fill = (pct / 100) * BAR_LENGTH
            outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
            fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
            pg.draw.rect(surf, GREEN, fill_rect)
            pg.draw.rect(surf, WHITE, outline_rect, 2)

    # player input
    def events(self):
        for event in pg.event.get():
                # when you hit the red x the window closes the game ends
                if event.type == pg.QUIT:
                    self.quit()
                    print("the game has ended..")
                elif event.type == pg.KEYDOWN: 
                    if event.key == pg.K_SPACE:
                        self.player.shoot()
                # keyboard events
                # if event.type == pg.KEYDOWN:
                #     if event.key == pg.K_LEFT:
                #         self.player.move(dx=-1)
                # if event.type == pg.KEYDOWN:
                #     if event.key == pg.K_RIGHT:
                #         self.player.move(dx=1)
                # if event.type == pg.KEYDOWN:
                #     if event.key == pg.K_UP:
                #         self.player.move(dy=-1)
                # if event.type == pg.KEYDOWN:
                #     if event.key == pg.K_DOWN:
                #         self.player.move(dy=1)

    def show_start_s(self):
        pass

    def show_game_s():
        pass

    def show_shop_s(self):
        # Show the shop screen
        while True:
            for event in pg.event.get():
                self.shop.handle_event(event)
            self.shop.draw()
            pg.display.flip()

# instanciating the game class
g = Game()
# g.show_ss()\
while True:
    g.new()
    g.run()