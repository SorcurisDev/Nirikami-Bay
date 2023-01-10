import pygame
from pygame import mixer
from sprites import *
from config import *
from pytmx.util_pygame import load_pygame
import sys
from npc_objects import *

class Game:
    def __init__(self):
        pygame.init()
        mixer.init()
        self.channel1 = pygame.mixer.Channel(0)
        self.channel2 = pygame.mixer.Channel(1)
        self.channel3 = pygame.mixer.Channel(2)
        self.bg_music = pygame.mixer.Sound("img/ambi.mp3")
        self.fishout = pygame.mixer.Sound("img/fish.mp3")
        self.cashout = pygame.mixer.Sound("img/coin.mp3")
        self.footsteps = pygame.mixer.Sound("img/footstep.mp3")

        self.introBGM = pygame.mixer.Sound("img/intro_bgm.mp3")

        #play bg music
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

        self.fish_exeLogo = pygame.image.load('img/fish_icon.png').convert()
        pygame.display.set_icon(self.fish_exeLogo)
        pygame.display.set_caption("Nirikami Bay")
        self.clock = pygame.time.Clock()
        self.running = True
        self.act_inplay = False
        self.ln = 0

        self.saying = False
        self.saying_cont = ""
        self.speech_loop = 0
        self.currMap = None

        #shop properties
        self.shop_on = False
        self.fishCaught = 1

        self.buttonPress = False

        self.tmxdata = load_pygame("img/tile_maps/terrain.tmx")
        MAP_DATAS[self.tmxdata.filename] = self.tmxdata
        self.tmxdata0 = load_pygame("img/tile_maps/terrain0.tmx")
        MAP_DATAS[self.tmxdata0.filename] = self.tmxdata0

        self.blankCase = pygame.image.load('img/blank.png').convert()

        self.font = pygame.font.Font('img/sdv.ttf', FONT_SIZE)

        self.character_spritesheet = spriteSheet('img/Col.png')

        self.lastButtonPressed = None

        #NPCS
        self.serafina = spriteSheet('img/serafina.png')
        self.taiya = spriteSheet('img/taiya.png')
        self.reno = spriteSheet('img/reno.png')

        self.enemy_spritesheet = spriteSheet('img/rolfish.png')
        self.intro_background = pygame.image.load('img/introbg.png')
        self.dialog_box = pygame.image.load('img/dialog.png').convert()
        self.attack_spritesheet = spriteSheet('img/fishing_animation.png')

        self.water = spriteSheet('img/wateranimation.png')

    def ani_get(self, startPosX, xEnd, yGuide, width, height,sheet):
        startPosX = TILE_SIZE * math.floor(startPosX)
        xEnd = TILE_SIZE * xEnd
        yGuide = TILE_SIZE * yGuide
        if startPosX >= xEnd:
            startPosX = 0
        imageOn = sheet.get_sprite(startPosX,yGuide, width, height)
        return imageOn
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
            if layers.name == "PLAYER_":
                for objects in layers:
                    self.player = Player(self, objects.x, objects.y) 
            elif layers.name == "COLLISIONS_":
              for colls in layers:
                    Ground(self, colls.x, colls.y, self.blankCase, "collision", colls.width, colls.height, map=mapOwn, tag=colls.name, par=colls.parent)
            elif layers.name == "NPC_":
                for npcs in layers:
                    npcx = math.floor(npcs.x)
                    npcy = math.floor(npcs.y)
                    rcW = math.floor(npcs.width)
                    rcH = math.floor(npcs.height)
                    nameToGet = npcs.name
                    Npc(self, npcx, npcy, nameToGet, rcW, rcH, map=mapOwn)
            elif layers.name == "SIGNS_":
                for npcs in layers:
                    npcx = math.floor(npcs.x)
                    npcy = math.floor(npcs.y)
                    rcW = math.floor(npcs.width)
                    rcH = math.floor(npcs.height)
                    nameToGet = npcs.name
                    Npc(self, npcx, npcy, nameToGet, rcW, rcH, "SIGNS_", map=mapOwn)
            elif layers.name == "FISHPOINTS_":
                for points in layers:
                    xpoint = math.floor(points.x)
                    ypoint = math.floor(points.y)
                    Enemy(self, xpoint, ypoint, map=mapOwn)
            elif layers.name == "DOORS_FI":
                for doors in layers:
                    nameToGet = doors.name
                    Door(self, doors.x, doors.y, nameToGet, doors.width, doors.height, mapOwn)
            elif layers.name == "GROUND_":
                for x, y, gid in layers.tiles():
                        xT = x * TILE_SIZE
                        yT = y * TILE_SIZE
                        lay_name = layers.name
                        Ground(self, xT, yT, gid, lay_name, map=mapOwn)
            elif layers.name == "WATER_":
                for x, y, gid in layers.tiles():
                        xT = x * TILE_SIZE
                        yT = y * TILE_SIZE
                        lay_name = layers.name
                        Ground(self, xT, yT, gid, lay_name, map=mapOwn)
            elif layers.name == "OBJECTS_WORLD":
                for x, y, gid in layers.tiles():
                        xT = x * TILE_SIZE
                        yT = y * TILE_SIZE
                        lay_name = layers.name
                        Ground(self, xT, yT, gid, lay_name, map=mapOwn)


    def new(self):

        #sets first map
        self.currMap = MAPS[0]

        # new game starts here
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.textOthers = pygame.sprite.LayeredUpdates()
        self.doors = pygame.sprite.LayeredUpdates()
        self.background_plate = pygame.sprite.LayeredUpdates()

        self.generateMaps()

        Text(self, 10, 10, "Fish Caught: "+str(self.player.total_fish_caught), "Fishpoints")
        Text(self, 10, 10+FONT_SIZE, "Money: "+str(self.player.total_fish_caught), "Money")

        self.sfa = pygame.Surface((WIN_WIDTH,100))  # the size of your rect
        self.sfa.set_alpha(128)                # alpha level
        self.sfa.fill((255,255,255))           # this fills the entire surface

        #shop parts
        self.close_shop = Button(self, WIN_WIDTH-200, WIN_HEIGHT/2, 100, 50, WHITE, BLACK, 'Close')
        for items in ITEM_SELL:
            Button(self, 0, 20, WIN_WIDTH-65, 40, WHITE, BLACK, items+" : "+ITEM_SELL[items][1]+" : "+str(ITEM_SELL[items][0])+"g", itemContent=items, itemPrice=ITEM_SELL[items][0])

        self.itemAccess = item_Functions(self)

        for i in range((WIN_HEIGHT % TILE_SIZE)):
            for x in range((WIN_WIDTH % TILE_SIZE)):
                Backdrop(self, x * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE)

    def events(self):
        # game loop events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
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
                    if event.key == pygame.K_q:
                        try:
                            self.player.last_collided.object_created.interact()
                        except:
                            print('NON INTERACTABLE')

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

    def draw(self):
        self.screen.fill(BLACK)
        self.background_plate.draw(self.screen)
        self.all_sprites.draw(self.screen)

        trDB = pygame.transform.scale(self.dialog_box, (300, 200))
        self.screen.blit(trDB, (0,5))    # (0,0) are the top-left coordinates
        self.textOthers.draw(self.screen)
        self.dialog_plot()


        #SHOP MENU FUNCTION
        if self.shop_on:
            tr = pygame.transform.scale(self.dialog_box, (WIN_WIDTH-10, WIN_HEIGHT-200))
            y_offset = 0
            self.screen.blit(tr, (5,10))
            self.screen.blit(self.close_shop.image, self.close_shop.rect)
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            if self.close_shop.is_pressed(mouse_pos, mouse_pressed):
                self.shop_on = False

            y_offset = 0
            for buttons in Buttons_Temp:
                ty = y_offset

                if not buttons.content == "Close":
                    buttons.rect.x = 15
                    buttons.rect.y = ty
                    self.screen.blit(buttons.image, buttons.rect)
                    mouse_pos = pygame.mouse.get_pos()
                    mouse_pressed = pygame.mouse.get_pressed()
                    if not self.buttonPress:
                        if buttons.is_pressed(mouse_pos, mouse_pressed):
                            self.buttonPress = True
                            print("kiil")
                            self.itemAccess.fetchFunc(buttons.itemContent, self.player.money, buttons.itemPrice)
                y_offset += 55
            y_offset = 0


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
    
    def dialog_plot(self):

        if self.saying:
            tf_dia = pygame.transform.scale(self.dialog_box,(WIN_WIDTH, 128))
            self.screen.blit(tf_dia, (DIA_XY[0], DIA_XY[1]))
            self.renderTextCenteredAt(self.saying_cont)
            if self.speech_loop >= SPEECH_AIRTIME:
                self.saying = False
                self.buttonPress = False
                self.speech_loop = 0
            else:
                self.speech_loop += 0.1
            

    def intro_screen(self):
        intro = True
        self.channel1.play(self.introBGM, -1)

        play_button = Button(self, WIN_WIDTH/2.4, WIN_HEIGHT/2+100, 100, 50, WHITE, BLACK, 'Play')

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
g.intro_screen()
g.new()
while g.running:
    g.main()
    g.game_over()
sys.exit()