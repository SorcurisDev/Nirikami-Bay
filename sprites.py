import pygame
from config import *
import math
import random
from pytmx.util_pygame import load_pygame
from npc_objects import *

class spriteSheet:

    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert_alpha()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height], pygame.SRCALPHA)
        sprite.blit(self.sheet, (0,0), (x, y , width, height))
        return sprite

class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        self._layer = PLAYER_LAYER

        self.total_fish_caught = 0
        self.money = 1000
        self.name = "Player"

        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'
        self.animation_loop = 0

        self.image = self.game.get_idle(1,1, self.width, self.height, self.game.character_spritesheet)

        self.rect = self.image.get_rect()
        self.rect.x = WIN_WIDTH/2 - 32
        self.rect.y = WIN_HEIGHT/2 - 32

        self.last_collided = None
        self.door_switch = True
        self.grace_away = 0

        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self,self.groups)

        #Player IN-GAME statuse
        self.rod_using = "Woodenpoli"
        self.rod_power = RODS[self.rod_using][1]

        self.inventory = []

    def insert_Inventory(self, item):
        for items in RODS:
            if item == RODS[items][0]:
                self.inventory.append(RODS[items])
        for items in FISHES:
            if item == FISHES[items][0]:
                self.inventory.append(FISHES[items])

    def update(self):
        self.movement()
        self.animate()
        self.collide_enemy()
        self.collide_door()

        self.rect.x += self.x_change
        self.collide_blocks("x")
        self.rect.y += self.y_change
        self.collide_blocks("y")

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        self.map_parent = self.game.currMap

        if not self.door_switch:
            if self.grace_away >= 32:
                self.door_switch = True
        else:
            self.grace_away = 0

        keys = pygame.key.get_pressed()
        if not self.game.act_inplay and not self.game.catch_fish and not self.game.on_interacting:
            if keys[pygame.K_LEFT]: 
                for sprite in self.game.all_sprites:
                    if sprite.map_parent == self.game.currMap:
                        sprite.rect.x += PLAYER_SPEED
                self.x_change -= PLAYER_SPEED
                self.facing = "left"
                self.last_collided = None
                self.grace_away += 1
                self.game.saying = False
            if keys[pygame.K_RIGHT]:
                for sprite in self.game.all_sprites:
                    if sprite.map_parent == self.game.currMap:
                        sprite.rect.x -= PLAYER_SPEED
                self.x_change += PLAYER_SPEED
                self.facing = "right"
                self.last_collided = None
                self.grace_away += 1
                self.game.saying = False
            if keys[pygame.K_UP]:
                for sprite in self.game.all_sprites:
                    if sprite.map_parent == self.game.currMap:
                        sprite.rect.y += PLAYER_SPEED
                self.y_change -= PLAYER_SPEED
                self.facing = "up"
                self.last_collided = None
                self.grace_away += 1
                self.game.saying = False
            if keys[pygame.K_DOWN]:
                for sprite in self.game.all_sprites:
                    if sprite.map_parent == self.game.currMap:
                        sprite.rect.y -= PLAYER_SPEED
                self.y_change += PLAYER_SPEED
                self.facing = "down"
                self.last_collided = None
                self.grace_away += 1
                self.game.saying = False

    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            pass
            #self.kill()
            #self.game.playing = False

    def collide_door(self):
        if self.door_switch:
            hits = pygame.sprite.spritecollide(self, self.game.doors, False)
            if hits:
                self.door_switch = False
                self.game.currMap = DOOR_NAMES[hits[0].doorname]

    def collide_blocks(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    for sprite in self.game.all_sprites:
                        if sprite.map_parent == self.game.currMap:
                            sprite.rect.x += PLAYER_SPEED
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    for sprite in self.game.all_sprites:
                        if sprite.map_parent == self.game.currMap:
                            sprite.rect.x -= PLAYER_SPEED
                    self.rect.x = hits[0].rect.right
                self.last_collided = hits[0]

        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    for sprite in self.game.all_sprites:
                        if sprite.map_parent == self.game.currMap:
                            sprite.rect.y += PLAYER_SPEED
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    for sprite in self.game.all_sprites:
                        if sprite.map_parent == self.game.currMap:
                            sprite.rect.y -= PLAYER_SPEED
                    self.rect.y = hits[0].rect.bottom
                self.last_collided = hits[0]
    
    def animate(self):
        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.game.get_idle(2, 2, self.width, self.height, self.game.character_spritesheet)
            else:
                self.image = self.game.ani_get(self.animation_loop, 2, 2, self.width, self.height, self.game.character_spritesheet)
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
                if not self.game.channel2.get_busy():
                    self.game.channel2.play(self.game.footsteps)
        if self.facing == "left":
            if self.x_change == 0:
                self.image = self.game.get_idle(1, 1, self.width, self.height, self.game.character_spritesheet)
            else:
                self.image = self.game.ani_get(self.animation_loop, 2, 1, self.width, self.height, self.game.character_spritesheet)
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
                if not self.game.channel2.get_busy():
                    self.game.channel2.play(self.game.footsteps)
        if self.facing == "up":
            if self.y_change == 0:
                self.image = self.game.get_idle(1, 3, self.width, self.height, self.game.character_spritesheet)
            else:
                self.image = self.game.ani_get(self.animation_loop, 2, 3, self.width, self.height, self.game.character_spritesheet)
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
                if not self.game.channel2.get_busy():
                    self.game.channel2.play(self.game.footsteps)
                
        if self.facing == "down":
            if self.y_change == 0:
                self.image = self.game.get_idle(1, 0, self.width, self.height, self.game.character_spritesheet)
            else:
                self.image = self.game.ani_get(self.animation_loop, 2, 0, self.width, self.height, self.game.character_spritesheet)
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
                if not self.game.channel2.get_busy():
                    self.game.channel2.play(self.game.footsteps)

class Fish(pygame.sprite.Sprite):
        def __init__(self, game, x, y, map):
            self.game = game
            self._layer = ENEMY_LAYER
            self.map_parent = map

            self.width = TILE_SIZE
            self.height = TILE_SIZE

            self.image = self.game.get_idle(0,0, self.width, self.height, self.game.fish_spritesheet)

            self.rect = self.image.get_rect()
            self.rect.x = math.floor(x)
            self.rect.y = math.floor(y)

            self.groups = self.game.all_sprites, self.game.enemies
            pygame.sprite.Sprite.__init__(self, self.groups)

            self.animation_loop = 0
            self.respawn_loop = 0
            self.caught = False
            self.respawn_interval = random.randint(RESPAWN_INTERVALS[0], RESPAWN_INTERVALS[1])
            self.dontAnimate = False

        def update(self):
            if not self.caught:
                self.checkIfExists()
                if not self.dontAnimate:
                    self.animate()
            else:
                self.image = self.game.blankCase
                if self.respawn_loop >= self.respawn_interval:
                    self.respawn_loop = 0
                    self.animation_loop = 0
                    self.game.enemies.add(self)
                    self.caught = False
                else:
                    self.respawn_loop += 0.1

        def checkIfExists(self):
            map_remained = self.game.currMap
            check_sprites = self.game.enemies.sprites()
            if self.map_parent == map_remained:
                if not self in check_sprites:
                    self.game.enemies.add(self)
                    self.dontAnimate = False
            else:
                if self in check_sprites:
                    self.game.enemies.remove(self)
                    self.dontAnimate = True

        def animate(self):
        
            self.image = self.game.ani_get(self.animation_loop, 15, 0, self.width, self.height, self.game.fish_spritesheet)
            self.animation_loop += 0.1
            if self.animation_loop >= 16:
                self.animation_loop = 0

class Door(pygame.sprite.Sprite):
    def __init__(self, game, x, y, name, width, height, map):
        self.game = game
        self.doorname = name
        self.map_parent = map
        self._layer = DOORS_LAYER

        self.image = self.game.blankCase
        self.rect = self.image.get_rect()
        self.rect.x = math.floor(x)
        self.rect.y = math.floor(y)
        self.rect.width = width
        self.rect.height = height

        self.groups = self.game.all_sprites, self.game.doors
        pygame.sprite.Sprite.__init__(self, self.groups)

    def update(self):
        self.checkIfExists()

    def checkIfExists(self):
        map_remained = self.game.currMap
        check_sprites = self.game.doors.sprites()
        if self.map_parent == map_remained:
            if not self in check_sprites:
                self.game.doors.add(self)
        else:
            if self in check_sprites:
                self.game.doors.remove(self)

class Collision_Boxes(pygame.sprite.Sprite):
    def __init__(self, game, x, y, image, width, height, map):
        self.game = game
        self.image = image
        self.map_parent = map
        self._layer = GROUND_LAYER
        
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.rect.width = math.floor(width)
        self.rect.height = math.floor(height)

        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

    def update(self):
        self.checkIfExists()

    def checkIfExists(self):
        map_remained = self.game.currMap
        check_sprites = self.game.blocks.sprites()
        if self.map_parent == map_remained:
            if not self in check_sprites:
                self.game.blocks.add(self)
        else:
            if self in check_sprites:
                self.game.blocks.remove(self)


class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y, img, map):
        self.game = game
        self._layer = GROUND_LAYER
        self.map_parent = map
        self.backup_img = img
        self.image = img

        self.image.set_colorkey(BLACK)

        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE

class Inventory():
    def __init__(self, game, text):
        self.game = game
        self.text = text
        self.font = pygame.font.Font('img/sdv.ttf', 25)

        self.diaSwitch = False
        self.diaSwitchPressed = False

        self.fg = BLACK

        self.imgBended = pygame.transform.scale(self.game.dialog_box, (600, 35))

        self.image = self.imgBended
        self.rect = self.image.get_rect()

        self.content = self.font.render(self.text, True, self.fg)
        TempCo = self.rect.x+25
        self.content_rect = self.content.get_rect(x=TempCo, y=5)
        self.image.blit(self.content, self.content_rect)

        Inv_Items.append(self)
        self.game.player.insert_Inventory(self.text)

    def function(self):
        pass

    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False

class Option():
    def __init__(self, game, text):
        self.game = game
        self.text = text
        self.font = pygame.font.Font('img/sdv.ttf', 25)

        self.diaSwitch = False
        self.diaSwitchPressed = False

        self.fg = BLACK

        self.imgBended = pygame.transform.scale(self.game.dialog_box, (600, 35))

        self.image = self.imgBended
        self.rect = self.image.get_rect()

        self.content = self.font.render(self.text, True, self.fg)
        TempCo = self.rect.x+25
        self.content_rect = self.content.get_rect(x=TempCo, y=5)
        self.image.blit(self.content, self.content_rect)

        Option_Items.append(self)
    
    def function(self):
        if self.text == "Help":
            self.game.saying_cont = "Help provided"
            self.game.saying = True
        if self.text == "Credits":
            self.game.saying_cont = "Of course that's sorcuris"
            self.game.saying = True
        if self.text == "Dev Website":
            self.game.saying_cont = "Wala pa paps"
            self.game.saying = True


    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False

class ShopList():
    def __init__(self, game, text, itemCont, itemPrice):
        self.game = game
        self.text = text
        self.itemCont = itemCont
        self.itemPrice = itemPrice
        self.font = pygame.font.Font('img/sdv.ttf', 25)

        self.diaSwitch = False
        self.diaSwitchPressed = False

        self.fg = BLACK

        self.imgBended = pygame.transform.scale(self.game.dialog_box, (600, 35))

        self.image = self.imgBended
        self.rect = self.image.get_rect()

        self.content = self.font.render(self.text, True, self.fg)
        TempCo = self.rect.x+25
        self.content_rect = self.content.get_rect(x=TempCo, y=5)
        self.image.blit(self.content, self.content_rect)

        Shop_Items.append(self)
    
    def function(self):
        self.game.itemAccess.fetchFunc(self.itemCont, self.game.player.money, self.itemPrice)

    def update(self):
        pass

    def is_pressed(self, pos, pressed):
       if not self.itemCont == None:
            if not self.diaSwitchPressed:
                if self.rect.collidepoint(pos):
                    self.diaSwitch = True
                    self.game.saying_cont = ITEM_SELL[self.itemCont][1]
                    self.game.saying = True
                else:
                    if self.diaSwitch:
                        self.diaSwitch = False
                        self.game.saying = False

            if self.rect.collidepoint(pos):
                if pressed[0]:
                    self.diaSwitchPressed = True
                    return True
                if not pressed[0]:
                    if not self.game.saying:
                        self.diaSwitchPressed = False
                    if not self.itemCont == None:
                        self.game.itemAccess.switch = True
                return False
            return False

class Button(pygame.sprite.Sprite):
    def __init__(self, game, x, y, content):
        self.font = pygame.font.Font('img/sdv.ttf', 25)

        self.game = game
        self.content = content

        self.diaSwitch = False
        self.diaSwitchPressed = False

        self.fg = BLACK

        wH = 25 * len(self.content) 
        if wH >= WIN_WIDTH+10:
            wH -= WIN_WIDTH/2
        self.imgBended = pygame.transform.scale(self.game.dialog_box, (111, 35))

        self.image = self.imgBended
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.text = self.font.render(self.content, True, self.fg)
        TempCo = 5
        self.text_rect = self.text.get_rect(x=TempCo, y=5)
        self.image.blit(self.text, self.text_rect)

        Buttons_Temp.append(self)
    
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        
        if self.is_pressed(mouse_pos, mouse_pressed):

            #Code here every UI Button function
            if self.content == "Close":
                self.game.menu_box_on = False
            if self.content == "Menu":
                self.game.menu_box_on = True
                self.game.menu_to_list = Option_Items
            if self.content == "Inventory":
                self.game.menu_box_on = True
                self.game.menu_to_list = Inv_Items


    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False
    

class Text(pygame.sprite.Sprite):
    def __init__(self, game, x, y, content, content_chg=None):
        self.game = game
        self.content_chg = content_chg
        self._layer = TEXTS_LAYER
        self.content = content

        self.font = pygame.font.Font('img/sdv.ttf', 25)

        self.image = self.font.render(self.content, True, BLACK)
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.groups = self.game.textOthers
        pygame.sprite.Sprite.__init__(self, self.groups)

    def update(self):

        self.image = self.font.render(self.content, True, BLACK)
        
        if self.content_chg == "Fishpoints":
            tpc = "Fish Caught: " +str(self.game.player.total_fish_caught)
            self.content = tpc
        if self.content_chg == "Money":
            tpc = "Money: " +str(self.game.player.money)
            self.content = tpc

class Attack(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.game.act_inplay = True
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.image = self.game.get_idle(0,0, self.width, self.height, self.game.attack_spritesheet)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.animation_loop = 0

    def update(self):
        self.animate()
        self.collide()

    def collide(self):
        if not self.game.catch_fish:
            hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
            if hits:
                self.game.bar_height[0][1] = WIN_HEIGHT-105
                self.game.bar_height[1][1] = WIN_HEIGHT-105
                self.game.catch_fish = True
                self.game.fish_on_line = hits[0]

    def animate(self):
        direction = self.game.player.facing

        if direction == "up":
            self.image = self.game.ani_get(self.animation_loop, 7, 2, self.width, self.height, self.game.attack_spritesheet)
            self.animation_loop += 0.5
            if self.animation_loop >= 8:
                self.kill()
                self.game.act_inplay = False
        if direction == "down":
            self.image = self.image = self.game.ani_get(self.animation_loop, 7, 3, self.width, self.height, self.game.attack_spritesheet)
            self.animation_loop += 0.5
            if self.animation_loop >= 8:
                self.kill()
                self.game.act_inplay = False
        if direction == "left":
            self.image = self.image = self.game.ani_get(self.animation_loop, 5, 1, self.width, self.height, self.game.attack_spritesheet)
            self.animation_loop += 0.5
            if self.animation_loop >= 6:
                self.kill()
                self.game.act_inplay = False
        if direction == "right":
            self.image = self.image = self.game.ani_get(self.animation_loop, 5, 0, self.width, self.height, self.game.attack_spritesheet)
            self.animation_loop += 0.5
            if self.animation_loop >= 6:
                self.kill()
                self.game.act_inplay = False

class Sign(pygame.sprite.Sprite):
    def __init__(self, game, x, y, img, width, height, name, map):
        self.game = game
        self.name = name
        self.map_parent = map
        self.image = img

        self.rect = self.image.get_rect()
        self.rect.x = math.floor(x)
        self.rect.y = math.floor(y)
        self.rect.width = math.floor(width)
        self.rect.height = math.floor(height)

        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        
    def interact(self):
        if not self.game.saying:
            self.game.saying = True
            self.game.saying_cont = SIGN_CONTS[self.name]

class Npc(pygame.sprite.Sprite):
    def __init__(self, game, x, y, nameOf, map):
        self.game = game
        self._layer = NPC_LAYER
        self.nameOf = nameOf
        self.map_parent = map

        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.animation_loop = 0
        self.dontAnimate = False

        if self.nameOf == "serafina":
            self.object_sheet = self.game.serafina
            self.image = self.game.get_idle(1, 0, self.width, self.height, self.object_sheet)
        if self.nameOf == "taiya":
            self.object_sheet = self.game.taiya
            self.image = self.game.get_idle(1, 0, self.width, self.height, self.object_sheet)
        if self.nameOf == "reno":
            self.object_sheet = self.game.reno
            self.image = self.game.get_idle(0, 1, self.width, self.height, self.object_sheet)

        self.rect = self.image.get_rect()
        self.rect.x = math.floor(x)
        self.rect.y = math.floor(y)
        self.rect.width = self.width
        self.rect.height = self.height

        if self.nameOf == "serafina":
            self.object_created = Serafina(self)
        if self.nameOf == "taiya":
            self.object_created = Taiya(self)
        if self.nameOf == "reno":
            self.object_created = Reno(self)

    def checkIfExists(self):
        map_remained = self.game.currMap
        check_sprites = self.game.blocks.sprites()
        if self.map_parent == map_remained:
            if not self in check_sprites:
                self.game.blocks.add(self)
                self.dontAnimate = False
        else:
            if self in check_sprites:
                self.game.blocks.remove(self)
                self.dontAnimate = True
                
class Backdrop(pygame.sprite.Sprite):
    def __init__(self, game, x, y, width, height):
        self.game = game
        self.width = width
        self.height = height
        self.map_parent = self.game.currMap
        self._layer = SEA_LAYER

        self.image = self.game.get_idle(0,0, self.width, self.height, self.game.water)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.groups = self.game.background_plate
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.animation_loop = 0

    def update(self):
        self.animate()

    def animate(self):
        self.image = self.game.ani_get(self.animation_loop, 3, 0, self.width, self.height, self.game.water)
        self.animation_loop += 0.05
        if self.animation_loop >= 4:
            self.animation_loop = 0