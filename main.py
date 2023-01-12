import pygame
from pygame import mixer
from sprites import *
from config import *
from pytmx.util_pygame import load_pygame
import sys
from npc_objects import *

class Game:
    def __init__(self):

        #important initializations
        pygame.init()

        mixer.init()

        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

        self.fish_exeLogo = pygame.image.load('img/fish_icon.png').convert()

        pygame.display.set_icon(self.fish_exeLogo)
         
        pygame.display.set_caption("Nirikami Bay")
        
        self.clock = pygame.time.Clock()

        #game process flags
        self.running = True

        #attacking flag
        self.act_inplay = False

        #speech dialog variables
        self.saying = False
        self.saying_cont = ""
        self.speak_loop = 0

        #menu square prop
        self.menu_box_on = False
        self.menu_to_list = None

        #set current map for entire game
        self.currMap = None

        #shop properties
        self.fishCaught = 1

        #button flag
        self.buttonPress = False
        self.prevClicked = None
        self.on_interacting = False

        #main font of the game
        self.font = pygame.font.Font('img/sdv.ttf', FONT_SIZE)

        #All item actions/functions initializer
        self.itemAccess = item_Functions(self)

        #Reeling bar progress holder
        ps1 = [WIN_WIDTH-100, WIN_HEIGHT-210]
        ps2 = [WIN_WIDTH-75, WIN_HEIGHT-210]
        ps3 = [WIN_WIDTH-75, WIN_HEIGHT-105]
        ps4 = [WIN_WIDTH-75, WIN_HEIGHT-10]
        ps5 = [WIN_WIDTH-100, WIN_HEIGHT-10]
        ps6 = [WIN_WIDTH-100, WIN_HEIGHT-105]
        self.bar_height = [ps1,ps2,ps3,ps4,ps5,ps6]
        self.barReelSwitch = True
        self.catch_fish = False
        self.fish_on_line = None

    #gets the animation sprite position of given sprite sheet
    def ani_get(self, startPosX, xEnd, yGuide, width, height,sheet):
        startPosX = TILE_SIZE * math.floor(startPosX)
        xEnd = TILE_SIZE * xEnd
        yGuide = TILE_SIZE * yGuide
        if startPosX >= xEnd:
            startPosX = 0
        imageOn = sheet.get_sprite(startPosX,yGuide, width, height)
        return imageOn

    #gets the idle position of a given spritesheet
    def get_idle(self, x, y, width, height, sheet):
        x = TILE_SIZE * x
        y = TILE_SIZE * y
        imageIdleGet = sheet.get_sprite(x,y, width, height)
        return imageIdleGet

    def generateMaps(self):
        for i in MAP_DATAS:
            vis_layers = MAP_DATAS[i].visible_layers
            self.createTilemap(vis_layers, MAPS_RELAY[MAP_DATAS[i].filename])

    def createTilemap(self, visiblelayers, mapOwn):
        for layers in visiblelayers:

            #The following if series is for OBJECTS
            #New OBJECTS created in TILED needs to be specified and included into the below IF SERIES
            if layers.name == "COLLISIONS_":
              for colls in layers:
                    Collision_Boxes(self, colls.x, colls.y, self.blankCase, colls.width, colls.height, mapOwn)
            elif layers.name == "NPC_":
                for npc in layers:
                    Npc(self, npc.x, npc.y, npc.name, mapOwn)
            elif layers.name == "SIGNS_":
                for npcs in layers:
                    Sign(self, npcs.x, npcs.y, self.blankCase, npcs.width, npcs.height, npcs.name, mapOwn)
            elif layers.name == "FISHPOINTS_":
                for points in layers:
                    Fish(self, points.x, points.y, mapOwn)
            elif layers.name == "DOORS_FI":
                for doors in layers:
                    Door(self, doors.x, doors.y, doors.name, doors.width, doors.height, mapOwn)

            #Else statement below is for every layer that is not an OBJECT, and needed to be displayed as a tile only
            else:
                for x, y, gid in layers.tiles():
                        Ground(self, x, y, gid, mapOwn)


    def new_load_sounds(self):
        #channels
        self.channel1 = pygame.mixer.Channel(0)
        self.channel2 = pygame.mixer.Channel(1)
        self.channel3 = pygame.mixer.Channel(2)
        
        #load the sounds
        self.bg_music = pygame.mixer.Sound("img/ambi.mp3")
        self.fishout = pygame.mixer.Sound("img/fish.mp3")
        self.cashout = pygame.mixer.Sound("img/coin.mp3")
        self.footsteps = pygame.mixer.Sound("img/footstep.mp3")
        self.introBGM = pygame.mixer.Sound("img/intro_bgm.mp3")

    def new_load_tmx_maps(self):

        self.tmxdata = load_pygame("img/tile_maps/terrain.tmx")
        MAP_DATAS[self.tmxdata.filename] = self.tmxdata
        self.tmxdata0 = load_pygame("img/tile_maps/terrain0.tmx")
        MAP_DATAS[self.tmxdata0.filename] = self.tmxdata0
    
    def new_load_images(self):

        self.blankCase = pygame.image.load('img/blank.png').convert_alpha()
        self.intro_background = pygame.image.load('img/introbg.png').convert_alpha()
        self.dialog_box = pygame.image.load('img/dialog.png').convert_alpha()
        self.framebar = pygame.image.load('img/frame_bar.png').convert_alpha()
        self.framebar_fg = pygame.image.load('img/frame_bar_fg.png').convert_alpha()

    def new_load_spritesheets(self):

        #Player
        self.character_spritesheet = spriteSheet('img/Col.png')

        #NPCS
        self.serafina = spriteSheet('img/serafina.png')
        self.taiya = spriteSheet('img/taiya.png')
        self.reno = spriteSheet('img/reno.png')

        #Others
        self.fish_spritesheet = spriteSheet('img/rolfish.png')
        self.attack_spritesheet = spriteSheet('img/fishing_animation.png')
        self.water = spriteSheet('img/wateranimation.png')

    def new_generateGroups(self):

        #creates all groups
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.textOthers = pygame.sprite.LayeredUpdates()
        self.doors = pygame.sprite.LayeredUpdates()
        self.background_plate = pygame.sprite.LayeredUpdates()
    
    def new_load_ui_objects(self):

        #Makes UI text for graphics
        Text(self, 15, 15, "Fish Caught: "+str(self.player.total_fish_caught), "Fishpoints")
        Text(self, 15, 40, "Money: "+str(self.player.total_fish_caught), "Money")
        
    def on_screen_ui_updates(self):

        #Status Background Image
        stats_bg = pygame.transform.scale(self.dialog_box, (250, 100))
        self.screen.blit(stats_bg, (0,5)) 

        #UI Status texts and other
        self.textOthers.draw(self.screen)

        #Menu button display
        self.screen.blit(self.menu.image, self.menu.rect)

        #Inventory button display
        self.screen.blit(self.inv.image, self.inv.rect)

        #Dialog shows up if something is to be said by either NPC or any interactable with speech.
        if self.saying:
            tf_dia = pygame.transform.scale(self.dialog_box,(WIN_WIDTH, 128))
            self.screen.blit(tf_dia, (DIA_XY[0], DIA_XY[1]))
            self.renderTextCenteredAt(self.saying_cont)
            if self.speak_loop >= SPEECH_AIRTIME:
                self.saying = False
                self.buttonPress = False
            else:
                self.speak_loop += 0.1
        else:
            self.speak_loop = 0
            self.buttonPress = False

        #Reeling animation
        if self.catch_fish:
            self.screen.blit(self.framebar_fg, (WIN_WIDTH-103, WIN_HEIGHT-220))
            pygame.draw.polygon(self.screen, RED, [self.bar_height[0], self.bar_height[1], self.bar_height[2], self.bar_height[3], self.bar_height[4], self.bar_height[5]])
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                if self.barReelSwitch:
                    if self.bar_height[0][1] < WIN_HEIGHT-200:
                        self.fish_on_line.caught = True
                        self.catch_fish = False
                        self.fishout.play()
                        for i in range(self.fishCaught):
                            Inventory(self, "Normal Fish")
                            self.player.total_fish_caught += 1
                        self.enemies.remove(self.fish_on_line)
                        self.saying_cont = "You caught the fish!"
                        self.saying = True
                        self.bar_height[0][1] = WIN_HEIGHT-210
                        self.bar_height[1][1] = WIN_HEIGHT-210
                    
                    #must be rescaled both at the same time since it's a polygon
                    self.bar_height[0][1] -= self.player.rod_power
                    self.bar_height[1][1] -= self.player.rod_power
                    self.barReelSwitch = False
            else:
                self.barReelSwitch = True
            if self.bar_height[0][1] >= WIN_HEIGHT-8:
                self.catch_fish = False
                self.fish_on_line.caught = True
                self.enemies.remove(self.fish_on_line)
                self.saying_cont = "The fish got away!"
                self.saying = True
                self.bar_height[0][1] = WIN_HEIGHT-210
                self.bar_height[1][1] = WIN_HEIGHT-210
            self.bar_height[0][1] += 1#can later be specified for fish strength
            self.bar_height[1][1] += 1
            self.screen.blit(self.framebar, (WIN_WIDTH-103, WIN_HEIGHT-220))
        
        if self.menu_box_on:
            self.menu_box_open(self.menu_to_list)
            

    def menu_box_open(self, buttons_to_list):

        tr = pygame.transform.scale(self.dialog_box, (WIN_WIDTH-10, WIN_HEIGHT-200))
        self.screen.blit(tr, (5,10))

        self.screen.blit(self.close_shop.image, self.close_shop.rect)

        y_offset = 0
        for btn in buttons_to_list:
            btn.rect.x = 50
            btn.rect.y = 50 + y_offset

            self.screen.blit(btn.image, btn.rect)

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()


            if not self.buttonPress:
                if btn.is_pressed(mouse_pos, mouse_pressed):
                    self.buttonPress = True
                    btn.function()
                    self.prevClicked = btn
            if btn.is_pressed(mouse_pos, mouse_pressed):
                if not self.prevClicked == btn:
                    self.buttonPress = False
        
            y_offset += 45
        y_offset = 0

    def new(self):

        #sets first map
        self.currMap = MAPS[0]

        # new game starts here
        self.playing = True

        #load all game datas
        self.new_load_sounds()
        self.new_load_tmx_maps()
        self.new_load_images()
        self.new_load_spritesheets()
        self.new_generateGroups()

        #Makes all the maps in the game
        self.generateMaps()

        #Creates the PLAYER
        self.player = Player(self)
        Inventory(self, self.player.rod_using)

        #ScreenUI Generate
        self.new_load_ui_objects()

        #Generates Shop List
        self.close_shop = Button(self, WIN_WIDTH-200, WIN_HEIGHT/2, 'Close')

        #menu button
        self.menu = Button(self, WIN_WIDTH-120, 20, 'Menu')

        #Inventory button
        self.inv = Button(self, WIN_WIDTH-120, 70, 'Inventory')

        for items in ITEM_SELL:
            ShopList(self, items+" : "+ITEM_SELL[items][1]+" : "+str(ITEM_SELL[items][0])+"g", items, ITEM_SELL[items][0])

        for items in OPTIONS:
            Option(self, items)
        #Background for void and parallax
        for i in range((WIN_HEIGHT % TILE_SIZE)):
            for x in range((WIN_WIDTH % TILE_SIZE)):
                Backdrop(self, x * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE)

    def events(self):
        # game loop events
        for event in pygame.event.get():

            #Quitz Game
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

            #Handles attacks from player
            if event.type == pygame.KEYDOWN:
                if not self.act_inplay: 
                    if event.key == pygame.K_SPACE:
                        if self.player.facing == 'up':
                            Attack(self, self.player.rect.x, self.player.rect.y - TILE_SIZE)
                        if self.player.facing == 'down':
                            Attack(self, self.player.rect.x, self.player.rect.y + TILE_SIZE)
                        if self.player.facing == 'left':
                            Attack(self, self.player.rect.x - TILE_SIZE, self.player.rect.y)
                        if self.player.facing == 'right':
                            Attack(self, self.player.rect.x + TILE_SIZE, self.player.rect.y)

                    #Handles interaction with NPC and other interactables
                    if event.key == pygame.K_q:
                        self.on_interacting = True
                        try:
                            self.player.last_collided.interact()
                        except:
                            try:
                                self.player.last_collided.object_created.interact()
                            except Exception as e:
                                print(e)
                    else:
                        self.on_interacting = False 

    def update(self):
        # game loop updates

        self.background_plate.update()

        for i in self.all_sprites:
            try:
                if not i.map_parent == None:
                    if i.map_parent == self.currMap:
                        if not i.backup_img == None:
                            i.image = i.backup_img
                        i.update()
                    else:
                        i.image = self.blankCase
                        i.update()
            except:
                i.update()
        self.textOthers.update()

        for button in Buttons_Temp:
            button.update()

    def draw(self):

        #Black filler for preventing leftovers from sprite updates
        self.screen.fill(BLACK)

        #Void/Parallax
        self.background_plate.draw(self.screen)

        #main display for each with graphics
        self.all_sprites.draw(self.screen)

        #Draw UI properties
        self.on_screen_ui_updates()

        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        # game loop
        while self.playing:
            self.events()
            self.update()
            self.draw()
        self.running = False

    def game_over(self):
        pass

    def renderTextCenteredAt(self, text):
        allowed_width = WIN_WIDTH-10
        x = DIATXT_XY[0]
        y = DIATXT_XY[1]
        words = text.split()

        lines = []
        while len(words) > 0:
            line_words = []
            while len(words) > 0:
                line_words.append(words.pop(0))
                fw, fh = self.font.size(' '.join(line_words + words[:1]))
                if fw > allowed_width:
                    break

            line = ' '.join(line_words)
            lines.append(line)

        y_offset = 0
        for line in lines:
            fw, fh = self.font.size(line)

            # (tx, ty) is the top-left of the font surface
            tx = x
            ty = y + y_offset

            font_surface = self.font.render(line, True, BLACK)
            self.screen.blit(font_surface, (tx, ty))

            y_offset += fh

    def intro_screen(self):
        intro = True
        self.channel1.play(self.introBGM, -1)

        play_button = Button(self, WIN_WIDTH/2.4, WIN_HEIGHT/2+100, 'Play')

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False
                Buttons_Temp.remove(play_button)
                self.channel1.stop
                self.channel1.play(self.bg_music, -1)

            self.screen.blit(self.intro_background, (0,0))
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

g = Game()
#g.intro_screen()
g.new()
while g.running:
    g.main()
    g.game_over()
sys.exit()