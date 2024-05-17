# File created by Chris D'Amico

'''
Sources
- https://github.com/ccozort/cozort_chris_game_engine_Spring_2024/

'''

import pygame as pg
from pygame.sprite import Sprite
from settings import *
from random import *
# from PIL import Image
from os import *
import sys
vec = pg.math.Vector2


SPRITESHEET = "theBell.png"

# needed for animated sprite
game_folder = path.dirname(__file__)
img_folder = path.join(game_folder, 'image_files')

# needed for animated sprite
class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        # image = pg.transform.scale(image, (width, height))
        image = pg.transform.scale(image, (width * 1, height * 1))
        return image
       
# write a player class
class Player(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.player
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.transform.scale(game.player_img, (64, 64))
        self.rect = self.image.get_rect()
        # needed for animated sprite
        self.spritesheet = Spritesheet(path.join(img_folder, SPRITESHEET))
        # needed for animated sprite
        self.load_images()
        # self.image = game.player_img
        # self.image.fill(GREEN)
        # needed for animated sprite
        self.image = self.standing_frames[0]
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.hitpoints = 50
        self.speed = 300
        self.attack = 30
        # needed for animated sprite
        self.current_frame = 0
        # needed for animated sprite
        self.last_update = 0
        self.material = True
        # needed for animated sprite
        self.jumping = False
        # needed for animated sprite
        self.walking = False
    # def move(self, dx=0, dy=0):
    #     self.x += dx
    #     self.y += dy
    
    def shoot(self):
        Projectile(self.game, self.rect.centerx, self.rect.top, 'right')  # Assumes shooting right

    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -self.speed
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = self.speed
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -self.speed
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = self.speed
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071
        # if keys[pg.K_SPACE]:
        #     self.player.shoot()


    def collide_with_obj(self, group, kill, desc):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits and desc == "food":
            print("I collided with food")
            self.image.fill(GREEN)
        if hits and desc == "powerup":
            print("I collided with powerup")
            self.image.fill(GREEN)
        if hits and desc == "mob":
            print("I collided with mob")
            self.image.fill(GREEN)
            self.hitpoints -= 10
        if hits and desc == 'weapon':
            print('I collided with weapon')
            self.image.fill(GREEN)
            self.attack += 20


    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Coin":
                self.moneybag += 1
            if str(hits[0].__class__.__name__) == "PowerUp":
                self.speed += 700
            if str(hits[0].__class__.__name__) == "Mob":
                self.hitpoints -= 10

     # needed for animated sprite
    def load_images(self):
        self.standing_frames = [self.spritesheet.get_image(0,0, 32, 32), 
                                self.spritesheet.get_image(32,0, 32, 32)]
        # for frame in self.standing_frames:
        #     frame.set_colorkey(BLACK)

      
        # add other frame sets for different poses etc.
    # needed for animated sprite        
    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 350:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
            bottom = self.rect.bottom
            self.image = self.standing_frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom

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
                
    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 350:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
            bottom = self.rect.bottom
            self.image = self.standing_frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom

    def update(self):
        # self.rect.x = self.x * TILESIZE
        # self.rect.y = self.y * TILESIZE
        # needed for animated sprite
        self.animate()
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        # add x collision later
        self.collide_with_walls('x')
        self.rect.y = self.y
        # add y collision later
        self.collide_with_walls('y')
        self.collide_with_obj(self.game.power_ups, True, "powerup")
        self.collide_with_obj(self.game.foods, True, "food")
        self.collide_with_obj(self.game.mobs, True, "mob")
        self.collide_with_obj(self.game.weapons, True, "weapon")
        self.rect.width = self.rect.width
        self.rect.height = self.rect.height
        

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
    def __init__(self, game, x, y):
        # add powerup groups later....
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        # self.image.fill(RED)
        self.image = self.game.mob_img
        self.image = pg.transform.scale(game.mob_img, (64, 64))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.vx, self.vy = 100, 100
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = randint(1,3)
        self.hitpoints = 4

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
        if str(hits[0].__class__.__name__) == "Store":
                    self.game.open_store()

    def update(self):
        if self.hitpoints < 1:
            self.kill()
        # self.image.blit(self.game.screen, self.pic)
        # pass
        # # self.rect.x += 1
        # add x collision later
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        # self.collide_with_walls('x')
        # self.collide_with_walls('y')
        
        if self.rect.x < self.game.player.rect.x:
            self.vx = 100
        if self.rect.x > self.game.player.rect.x:
            self.vx = -100    
        if self.rect.y < self.game.player.rect.y:
            self.vy = 100
        if self.rect.y > self.game.player.rect.y:
            self.vy = -100
        self.rect.x = self.x
        # self.collide_with_walls('x')
        self.rect.y = self.y
        # self.collide_with_walls('y')

    def respawn(self):
        self.hitpoints = 20
        self.x = random.randint(0, self.game.map_width - 1)
        self.y = random.randint(0, self.game.map_height - 1)
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
        
class PowerUp(Sprite):
    def __init__(self, game, x, y):
        # add powerup groups later....
        self.groups = game.all_sprites, game.power_ups
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.transform.scale(game.powerup_img, (64, 64))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Food(Sprite):
    def __init__(self, game, x, y):
        # add powerup groups later....
        self.groups = game.all_sprites, game.foods
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(LIGHTGREY)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# glorified powerup :)
class Weapon(Sprite):
    def __init__(self, game, x, y, dir):
        self.groups = game.all_sprites, game.weapons
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.transform.scale(game.weapon_img, (96, 96))
        self.rect = self.image.get_rect()
        self.dir = dir
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.pos = vec(x,y)
        
        
    # from ccozort sword class
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Mob":
                print("you hurt a mob!")
                hits[0].hitpoints -= 1
            if str(hits[0].__class__.__name__) == "Mob2":
                print("you hurt a mob!")
                hits[0].hitpoints -= 1
# ccozort's coin class
class Coin(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        
class Projectile(pg.sprite.Sprite):
    def __init__(self, game, x, y, dir):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.transform.scale(game.weapon_img, (10, 5))  # Adjust size as needed
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 10  # Speed of the projectile
        self.dir = dir

    def update(self):
        # Update the projectile's position; modify if you have different directions
        if self.dir == 'right':
            self.rect.x += self.speed
        elif self.dir == 'left':
            self.rect.x -= self.speed
        # Remove the sprite if it leaves the screen
        if self.rect.right < 0 or self.rect.left > WIDTH:
            self.kill()

# integrated from GPT
class Shop:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.font = pg.font.Font(None, 36)
        self.items = ['Item 1', 'Item 2', 'Item 3']
        self.selected_item = None

    def draw(self):
        self.screen.fill(BLACK)
        for i, item in enumerate(self.items):
            color = WHITE if i != self.selected_item else RED
            text = self.font.render(item, True, color)
            self.screen.blit(text, (100, 100 + i * 50))

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = pg.mouse.get_pos()
            for i, _ in enumerate(self.items):
                if 100 <= mouse_pos[0] <= 200 and 100 + i * 50 <= mouse_pos[1] <= 150 + i * 50:
                    self.selected_item = i

        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.game.show_main_screen()

        elif event.type == pg.QUIT:
            self.game.quit()
# some store code from https://github.com/cgxysqiubdW708/che_james_game_engine_spring_2024/blob/main/main.py
alreadycamo = False

class Store:
    def __init__(self, game,x,y):
        self.game = game
        self.GAME_WINDOW_WIDTH, self.GAME_WINDOW_HEIGHT = game.screen.get_size()
        self.warning_box_visible = False

        # # Player stats
        # self.player_health = game.player1.hitpoints
        # self.player_attack = game.player1.hitpoints
        # self.player_coins = game.player1.moneybagS

    def set_player_health(self, new_health):
        self.player_health = new_health
        self.game.player1.hitpoints = new_health

    def set_player_attack(self, new_attack):
        self.player_attack = new_attack
        self.game.player1.attack = new_attack

    def has_enough_coins_for_any_powerup(self):
        for powerup in self.powerups:
            if self.player_coins >= powerup["cost"]:
                return True
        return False

    def draw_warning_box(self, text):
        if not self.warning_box_visible:
            return

        warning_box_width = 300
        warning_box_height = 100
        warning_box_x = (self.GAME_WINDOW_WIDTH - warning_box_width) // 2
        warning_box_y = (self.GAME_WINDOW_HEIGHT - warning_box_height) // 2

        pg.draw.rect(self.game.screen, (128, 128, 128), (warning_box_x, warning_box_y, warning_box_width, warning_box_height))

        font = pg.font.Font(None, 36)
        text_render = font.render(text, True, (255, 255, 255))
        text_rect = text_render.get_rect(center=(warning_box_x + warning_box_width // 2, warning_box_y + warning_box_height // 2))
        self.game.screen.blit(text_render, text_rect)

    def open(self):
        global alreadycamo, mobcamo
        # Store UI box dimensions and position
        box_width = 500
        box_height = 400
        box_x = (self.GAME_WINDOW_WIDTH - box_width) // 2
        box_y = (self.GAME_WINDOW_HEIGHT - box_height) // 2

        # Store UI
        store_open = True
        while store_open:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    store_open = False
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        store_open = False
                        self.warning_box_visible = False  # Close the warning box
                elif event.type == pg.MOUSEBUTTONDOWN:
                    pos = event.pos
                    self.handle_buy_button_click(pos)
                    store_open = self.handle_exit_button_click(pos)

                    # Check if the warning box was clicked
                    warning_box_width = 300
                    warning_box_height = 100
                    warning_box_x = (self.GAME_WINDOW_WIDTH - warning_box_width) // 2
                    warning_box_y = (self.GAME_WINDOW_HEIGHT - warning_box_height) // 2
                    warning_box_rect = pg.Rect(warning_box_x, warning_box_y, warning_box_width, warning_box_height)
                    if warning_box_rect.collidepoint(pos):
                        self.warning_box_visible = False  # Close the warning box

            # Clear the game window
            self.game.screen.fill((0, 0, 0))

            # Set mobcamo to true to fix bug where mobs despawn when store is closed
            if mobcamo == True:
                alreadycamo = True

            if mobcamo == False:
                alreadycamo = False
                mobcamo = True
                print("no mobcamo")

            # Draw the store UI box
            pg.draw.rect(self.game.screen, (128, 128, 128), (box_x, box_y, box_width, box_height))

            # Render player stats
            font = pg.font.Font(None, 36)
            stats_text = font.render(f"Health: {self.player_health} | Attack: {self.player_attack} | Coins: {self.player_coins}", True, (255, 255, 255))
            self.game.screen.blit(stats_text, (box_x + 10, box_y + 10))

            # Render powerup options and buy buttons
            y = box_y + 60
            for i, powerup in enumerate(self.powerups):
                powerup_text = font.render(f"{i + 1}. {powerup['name']} - Cost: {powerup['cost']}", True, (255, 255, 255))
                self.game.screen.blit(powerup_text, (box_x + 10, y))

                # Draw the buy button
                buy_button_width = 100
                buy_button_height = 30
                buy_button_x = box_x + box_width - buy_button_width - 20
                buy_button_y = y  # Adjusted vertical position to avoid overlap
                pg.draw.rect(self.game.screen, (0, 255, 0), (buy_button_x, buy_button_y, buy_button_width, buy_button_height))
                buy_button_text = font.render("Buy", True, (0, 0, 0))
                buy_button_text_rect = buy_button_text.get_rect(center=(buy_button_x + buy_button_width // 2, buy_button_y + buy_button_height // 2))
                self.game.screen.blit(buy_button_text, buy_button_text_rect)

                y += 60  # Increased vertical spacing between powerup options

            # Draw the exit button
            exit_button_width = 100
            exit_button_height = 30
            exit_button_x = box_x + (box_width - exit_button_width) // 2
            exit_button_y = box_y + box_height - exit_button_height - 20
            pg.draw.rect(self.game.screen, (255, 0, 0), (exit_button_x, exit_button_y, exit_button_width, exit_button_height))
            exit_button_text = font.render("Exit", True, (0, 0, 0))
            exit_button_text_rect = exit_button_text.get_rect(center=(exit_button_x + exit_button_width // 2, exit_button_y + exit_button_height // 2))
            self.game.screen.blit(exit_button_text, exit_button_text_rect)

            # Draw the warning box if the player doesn't have enough coins for any powerup
            if not self.has_enough_coins_for_any_powerup() and self.warning_box_visible:
                self.draw_warning_box("Not enough coins")

            pg.display.flip()

    def handle_buy_button_click(self, pos):
        box_width = 500
        box_height = 400
        box_x = (self.GAME_WINDOW_WIDTH - box_width) // 2
        box_y = (self.GAME_WINDOW_HEIGHT - box_height) // 2

        y = box_y + 60
        for i, powerup in enumerate(self.powerups):
            buy_button_width = 100
            buy_button_height = 30
            buy_button_x = box_x + box_width - buy_button_width - 20
            buy_button_y = y  # Adjusted vertical position to match the button position in open
            buy_button_rect = pg.Rect(buy_button_x, buy_button_y, buy_button_width, buy_button_height)
            if buy_button_rect.collidepoint(pos):
                if self.player_coins >= powerup["cost"]:
                    self.player_coins -= powerup["cost"]
                    if powerup["name"] == "Health Potion":
                        powerup["effect"](self.player_health + 1)
                    elif powerup["name"] == "Attack Boost":
                        powerup["effect"](self.player_attack + 5)
                    else:
                        powerup["effect"]()  # Call the effect function as-is for other powerups
                    print(f"Purchased {powerup['name']}")
                else:
                    print("Not enough coins")
                    self.warning_box_visible = True  # Show the warning box
                    self.draw_warning_box("Not enough coins")  # Draw the warning box

            y += 60  # Increased vertical spacing between powerup options

    def handle_exit_button_click(self, pos):
        global mobcamo
        box_width = 500
        box_height = 400
        box_x = (self.GAME_WINDOW_WIDTH - box_width) // 2
        box_y = (self.GAME_WINDOW_HEIGHT - box_height) // 2

        exit_button_width = 100
        exit_button_height = 30
        exit_button_x = box_x + (box_width - exit_button_width) // 2
        exit_button_y = box_y + box_height - exit_button_height - 20
        exit_button_rect = pg.Rect(exit_button_x, exit_button_y, exit_button_width, exit_button_height)

        if alreadycamo == True:
            pass
        elif alreadycamo == False:
            mobcamo = False

        if exit_button_rect.collidepoint(pos):
            self.game.player1.reset_position_after_store()  # Call the new method to reset player position
            return False  # Exit the store
        else:
            return True  # Stay in the store
        
    # def reset_position_after_store(self):
    #     # Move the player down by 2 tiles
    #     self.y = currenty + 2 * TILESIZE
    #     self.rect.y = self.y