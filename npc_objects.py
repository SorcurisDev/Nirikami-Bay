import pygame
from config import *
import math
import random
from pytmx.util_pygame import load_pygame
from sprites import *

class Serafina():
    def __init__(self, all_props):
        self.atts = all_props
        self.atts.update = self.update
        self.atts.animate = self.animate

    def update(self):
        if not self.atts.dontAnimate:
            self.animate()
        self.atts.checkIfExists()

    def animate(self):

        self.atts.animation_loop += 0.1
        self.atts.image = self.atts.game.ani_get(self.atts.animation_loop, 2,0, self.atts.width, self.atts.height, self.atts.object_sheet)
        if self.atts.animation_loop >= 3:
            self.atts.animation_loop = 0

    def interact(self):
        if not self.atts.game.saying:
            self.fishtosell = 0
            self.fishEarnings = 0

            if self.atts.game.player.total_fish_caught == 0:
                self.atts.game.saying_cont = "You don't have fish to sell!"
                self.atts.game.saying = True
            else:
                for i in range(self.atts.game.player.total_fish_caught):
                    for items in self.atts.game.player.inventory:
                        toRem = None
                        if items[2] == "Fish":
                            for itm in Inv_Items:
                                if itm.text == items[0]:
                                    toRem = itm
                                    break

                            mx = FISH_MULTIPLIER * items[1]
                            self.fishEarnings += mx
                            self.atts.game.player.inventory.remove(items)
                            Inv_Items.remove(toRem)
                            break

                #Play coin sound as per how many fish were sold
                #self.atts.game.channel3.play(self.atts.game.cashout, allfish-1)

                #Play coin sound once per sell

                self.atts.game.channel3.play(self.atts.game.cashout)
                self.atts.game.player.total_fish_caught = 0
                self.atts.game.player.money += self.fishEarnings

                self.atts.game.saying_cont = "Thank you! you've sold your fish for: "+str(self.fishEarnings)+" gold."
                self.atts.game.saying = True

                self.fishEarnings = 0
                self.fishtosell = 0

class Taiya():
    def __init__(self, all_props):
        self.atts = all_props
        self.atts.update = self.update
        self.atts.animate = self.animate
    def update(self):
        if not self.atts.dontAnimate:
            self.animate()
        self.atts.checkIfExists()

    def animate(self):

        self.atts.animation_loop += 0.1
        self.atts.image = self.atts.game.ani_get(self.atts.animation_loop, 2,0, self.atts.width, self.atts.height, self.atts.object_sheet)
        if self.atts.animation_loop >= 3:
            self.atts.animation_loop = 0
    def interact(self):
        if not self.atts.game.saying:
            self.atts.game.saying = True
            self.atts.game.saying_cont = "The fishes here are chubbier!"

class Reno():
    def __init__(self, all_props):
        self.atts = all_props
        self.atts.update = self.update
        self.atts.animate = self.animate
    def update(self):

        if not self.atts.dontAnimate:
            self.animate()
        self.atts.checkIfExists()

    def animate(self):

        self.atts.animation_loop += 0.1
        self.atts.image = self.atts.game.ani_get(self.atts.animation_loop, 2,0, self.atts.width, self.atts.height, self.atts.object_sheet)
        if self.atts.animation_loop >= 3:
            self.atts.animation_loop = 0
            
    def interact(self):
        self.atts.game.menu_box_on = True
        self.atts.game.menu_to_list = Shop_Items

class item_Functions():
    def __init__(self, game):
        self.game = game
        self.switch = True

    def fetchFunc(self, func, money, price):

        if money >= price:
            if self.switch:
                if func == "Fishrusher":
                    self.fishrusher()
                if func == "High Up":
                    self.highup()
                self.switch = False
        else:
            self.game.saying_cont = "You cannot afford this."
            self.game.saying = True

    def fishrusher(self):
        self.game.fishCaught += 1
        self.game.player.money -= 800
        self.game.saying_cont = "Fishes gained when caught is now 2x!"
        self.game.saying = True

    def highup(self):
        global FISH_MULTIPLIER
        FISH_MULTIPLIER = 2
        self.game.player.money -= 200
        self.game.saying_cont = "The prices of fish went up!"
        self.game.saying = True