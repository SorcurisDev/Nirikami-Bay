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
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.total_fish_caught = 0
        self.money = 900
        self.name = "Player"

        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'
        self.animation_loop = 0

        self.image = self.game.character_spritesheet.get_sprite(1,1, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = WIN_WIDTH/2 - 32
        self.rect.y = WIN_HEIGHT/2 - 32

        self.last_collided = None
        self.door_switch = True
        self.grace_away = 0


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
        if not self.game.act_inplay:
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
                self.game.currMap = DOOR_NAMES[hits[0].tile_id]

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

class Enemy(pygame.sprite.Sprite):
        fish_population = 0
        def __init__(self, game, x, y, map=None):
            self.game = game
            self._layer = ENEMY_LAYER
            self.map_parent = map
            self.groups = self.game.all_sprites, self.game.enemies
            pygame.sprite.Sprite.__init__(self, self.groups)

            
            self.x = x
            self.y = y
            self.width = TILE_SIZE
            self.height = TILE_SIZE

            self.animation_loop = 0
            self.respawn_loop = 0
            self.caught = False
            self.respawn_interval = random.randint(RESPAWN_INTERVALS[0], RESPAWN_INTERVALS[1])
            self.dontAnimate = False

            self.image = self.game.enemy_spritesheet.get_sprite(0,0, self.width, self.height)
            #self.image.set_colorkey(BLACK)

            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y

            Enemy.fish_population += 1
            self.game.hitFlag = False

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
        
            self.image = self.game.ani_get(self.animation_loop, 15, 0, self.width, self.height, self.game.enemy_spritesheet)
            self.animation_loop += 0.1
            if self.animation_loop >= 16:
                self.animation_loop = 0

class Door(pygame.sprite.Sprite):
    def __init__(self, game, x, y, tile_id, rectWidth, rectHeight, map):
        self.game = game
        self.x = math.floor(x)
        self.y = math.floor(y)
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.tile_id = tile_id
        self.rectWidth = rectWidth
        self.rectHeight = rectHeight
        self.map_parent = map

        self._layer = DOORS_LAYER

        self.groups = self.game.all_sprites, self.game.doors
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.image = self.game.blankCase
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.rect.width = self.rectWidth
        self.rect.height = self.rectHeight

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

class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y, img=None, tile_id=None, rectWidth=None, rectHeight=None, map=None, tag=None, par=None):
        self.game = game
        self.tile_id = tile_id
        self._layer = GROUND_LAYER
        self.rectWidth = rectWidth
        self.rectHeight = rectHeight
        self.map_parent = map
        self.backup_img = img
        self.image = img
        self.tag = tag
        self.parent = par

        if self.image == None:
            self.image = self.game.blankCase
        self.image.set_colorkey(BLACK)

        if self.tile_id == "collision":
            self.groups = self.game.all_sprites, self.game.blocks
        else: 
            self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x 
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        if self.tile_id == "collision":
            self.rect.width = math.floor(self.rectWidth)
            self.rect.height = math.floor(self.rectHeight)
    def update(self):
        if self.tile_id == "collision":
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

class Button:
    def __init__(self, game, x, y, width, height, fg, bg, content, itemContent=None, itemPrice=None):
        self.font = pygame.font.Font('img/sdv.ttf', 25)

        self.game = game
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.content = content
        self.itemContent = itemContent
        self.itemPrice = itemPrice

        self.atClicked = False
        self.diaSwitch = False
        self.diaSwitchPressed = False

        self.fg = BLACK

        wH = 25 * len(self.content) 
        if wH >= WIN_WIDTH+10:
            wH -= WIN_WIDTH/2
        self.imgBended = pygame.transform.scale(self.game.dialog_box, (wH+11, 35))

        self.image = self.imgBended
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y

        self.text = self.font.render(self.content, True, self.fg)
        if self.content == "Play" or self.content == "Close":
            TempCo = wH/2-15
        else:
            TempCo = 10
        self.text_rect = self.text.get_rect(x=TempCo, y=5)
        self.image.blit(self.text, self.text_rect)

        Buttons_Temp.append(self)
    
    def is_pressed(self, pos, pressed):
        if not self.itemContent == None:
            if not self.diaSwitchPressed:
                if self.rect.collidepoint(pos):
                    self.diaSwitch = True
                    self.game.saying_cont = ITEM_SELL[self.itemContent][1]
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
                if not self.itemContent == None:
                    self.game.itemAccess.switch = True
            return False
        return False
    

class Text(pygame.sprite.Sprite):
    def __init__(self, game, x, y, content, content_chg=None):
        self.game = game
        self.content_chg = content_chg
        self.x = x
        self.y = y
        self._layer = TEXTS_LAYER
        self.content = content

        self.groups = self.game.textOthers
        pygame.sprite.Sprite.__init__(self, self.groups)

    def update(self):

        self.image = self.game.font.render(self.content, True, BLACK)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y
        
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
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.animation_loop = 0
        self.image = self.game.attack_spritesheet.get_sprite(0,0, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.animate()
        self.collide()

    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            hits[0].caught = True
            self.game.fishout.play()
            self.game.player.total_fish_caught += self.game.fishCaught
            self.game.enemies.remove(hits[0])
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

class Npc(pygame.sprite.Sprite):
    def __init__(self, game, x, y, nameOf, width, height, layerGet=None, map=None):
        self.game = game
        self.x = x
        self.y = y
        self._layer = NPC_LAYER
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.rectWidth = width
        self.rectHeight = height
        self.nameOf = nameOf
        self.layerGet = layerGet
        self.map_parent = map

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

        if self.layerGet == "SIGNS_":
            self.image = self.game.blankCase

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.rect.width = TILE_SIZE 
        self.rect.height = TILE_SIZE

        if self.nameOf == "serafina":
            self.object_created = Serafina(self)
        if self.nameOf == "taiya":
            self.object_created = Taiya(self)
        if self.nameOf == "reno":
            self.object_created = Reno(self)
        if self.layerGet == "SIGNS_":
            self.object_created = Sign(self)

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
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.map_parent = self.game.currMap
        self._layer = SEA_LAYER

        self.image = self.game.get_idle(0,0, self.width, self.height, self.game.water)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.animation_loop = 0

        self.groups = self.game.background_plate
        pygame.sprite.Sprite.__init__(self, self.groups)

    def update(self):
        self.animate()

    def animate(self):
        self.image = self.game.ani_get(self.animation_loop, 3, 0, self.width, self.height, self.game.water)
        self.animation_loop += 0.05
        if self.animation_loop >= 4:
            self.animation_loop = 0