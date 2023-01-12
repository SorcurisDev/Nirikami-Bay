WIN_WIDTH = 850
WIN_HEIGHT = 600
FPS = 60

PLAYER_LAYER = 4
TEXTS_LAYER = 4
DOORS_LAYER = 3
NPC_LAYER = 3
ENEMY_LAYER = 3
GROUND_LAYER = 2
SEA_LAYER = 1

MAP_DATAS = {}

MAP_LOCATE = {}

SIGN_CONTS = {
    "sign1": "SeraStore: I Buy Fishes!",
    "sign2": "Varibay Fishing Spot",
    "sign3": "Flowerbay Fishing Spot",
    "sign4": "Reno: Buy fish'ments here!"
}

MAPS = [
    "FheirstIsland",
    "SerafinaHouse"
]

MAPS_RELAY = {
    "img/tile_maps/terrain.tmx" : MAPS[0],
    "img/tile_maps/terrain0.tmx" : MAPS[1]
}

DOOR_NAMES = {
    "door_serafina_house": MAPS[1],
    "door_island": MAPS[0]
}

ITEM_SELL = {
    "Fishrusher": (800,"Doubles your fish catch!"),
    "High Up": (200,"Make your fish sell better!")
}

OPTIONS = [
    "Help",
    "Credits",
    "Dev Website"
]

#Name, Power, Classification
RODS = {
    "Woodenpoli": ("Woodenpoli",50,"Rod")
}
FISHES = {
    "Normal Fish": ("Normal Fish",10,"Fish")
}

#FISH SELLING MECHANISM AND PROPERTIES
FISH_MULTIPLIER = 1

Buttons_Temp = []

Shop_Items = []
Option_Items = []
Inv_Items = []

DIA_XY = (0, 415)
DIATXT_XY = (DIA_XY[0]+15, DIA_XY[1]+10)
SPEECH_AIRTIME = 30

FONT_SIZE = 45

MAX_FISHPOP = 4
RESPAWN_INTERVALS = (20, 40)

WATERLAYER_LN = 0
GROUNDLAYER_LN = 1
SOLIDLAYER_LN = 2

PLAYER_SPEED = 3
ENEMY_SPEED = 2

TILE_SIZE = 64

RED = (255,0,0)
BLACK = (0,0,0)
BLUE = (0,0,255)
WHITE = (255,255,255)