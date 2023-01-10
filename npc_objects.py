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
        self.fishprice = FISH_PRICE

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
            self.fishprice = FISH_PRICE

            if not self.atts.game.player.total_fish_caught:
                self.atts.game.saying_cont = "You don't have fish to sell!"
            else:
                allfish = self.atts.game.player.total_fish_caught
                earnings = allfish * self.fishprice
                self.atts.game.saying_cont = "Thank you! you've sold your fish for: "+str(earnings)+" gold."

                #Play coin sound as per how many fish were sold
                #self.atts.game.channel3.play(self.atts.game.cashout, allfish-1)

                #Play coin sound once per sell
                self.atts.game.channel3.play(self.atts.game.cashout)

                self.atts.game.player.total_fish_caught = 0
                self.atts.game.player.money += earnings

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
        self.atts.game.shop_on = True

class Sign():
    def __init__(self, all_props):
        self.atts = all_props
        self.atts.update = self.update
    def update(self):
        self.atts.image = self.atts.game.blankCase
    def interact(self):
        if not self.atts.game.saying:
            self.atts.game.saying = True
            self.atts.game.saying_cont = SIGN_CONTS[self.atts.nameOf]

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
        global FISH_PRICE
        FISH_PRICE += 10
        self.game.player.money -= 200
        self.game.saying_cont = "The prices of fish went up by 10!"
        self.game.saying = True