#!/bin/python

import pygame, sys, random
from displayglobals import *
from cards import *
from statemanager import *
from pygame.locals import *

""" Game Menu Code Based on https://nebelprog.wordpress.com/2013/09/02/create-a-simple-game-menu-with-pygame-pt-4-connecting-it-to-functions/
"""

# Classes (OOP FTW)

class InvalidInput(Exception):
    def __init__(self, problem):
        self.value = problem
    def __str__(self):
        return repr(self.value)

class MissingFunction(Exception):
    def __init__(self, problem):
        self.value = problem
    def __str__(self):
        return repr(self.value)

class MissingState(Exception):
    def __init__(self, problem):
        self.value = problem
    def __str__(self):
        return repr(self.value)

# Game Classes
class Player(object):
    def __init__(self):
        self.hand = []
        self.score = 0
        
class Table(object):
    def __init__(self, numPlayers, team=False):
        self.numPlayers = numPlayers
        if self.numPlayers <= 0 or self.numPlayers > 4:
            raise InvalidInput("Invalid number of Player (1-4)")
        self.team = team

                        
# Display Classes
# # Menu Stuff
class MenuItem(pygame.font.Font):
    def __init__(self, text, font=None, font_size=30, font_color=WHITE, (posX, posY)=(0,0)):
        pygame.font.Font.__init__(self, font, font_size)
        self.text = text
        self.font_size = font_size
        self.font_color = font_color
        self.label = self.render(self.text, 1, self.font_color)
        self.width = self.label.get_rect().width
        self.height = self.label.get_rect().height
        self.posX = posX
        self.posY = posY
        self.position = posX, posY

    def set_position(self, x, y):
        self.position = (x, y)
        self.posX = x
        self.posY = y

    def set_font_color(self, color):
        # Color is a tuple: (R, G, B)
        self.font_color = color
        self.label = self.render(self.text, 1, self.font_color)

    def is_mouse_selection(self, (posx, posy)):
        if (posx >= self.posX and posx <= self.posX + self.width) and (posy >= self.posY and posy <= self.posY + self.height):
            return True
        return False
        
class PreGameMenu(State):
    def __init__(self, screen, clock, items, funcs, bg_color=GREEN, font="TimesNewRoman", font_size=30, font_color=(255, 255, 255)):

        super(PreGameMenu, self).__init__() # Init State Base Class
        self.screen = screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height
        
        self.bg_color = bg_color
        self.clock = clock
        self.font = pygame.font.SysFont(font, font_size)
        self.font_color = font_color

        self.mouse_is_visible = True

        self.funcs = funcs
        
        self.items = []
        self.cur_item = None
        for index, item in enumerate(items):
            menu_item = MenuItem(item)
            label = self.font.render(item, 1, self.font_color)

            # t_h: total height of text block
            t_h = len(items) * menu_item.height
            posx = (self.scr_width / 2) - (menu_item.width / 2)
            posy = (self.scr_height / 2) - (t_h / 2) + ((index * 2) + index * menu_item.height)
            menu_item.set_position(posx, posy)
            self.items.append(menu_item)
    

    def set_mouse_selection(self, item, mpos):
        #Marks the MenuItem the mouse cursor hovers on

        if item.is_mouse_selection(mpos):
            item.set_font_color(GREEN)
            item.set_italic(True)
        else:
            item.set_font_color(WHITE)
            item.set_italic(False)

    def set_keyboard_selection(self, key):
        # Marks the MenuItem chosen via up and down keys

        for item in self.items:
            # Return all to normal
            item.set_italic(False)
            item.set_font_color(WHITE)

        if self.cur_item is None:
            self.cur_item = 0
        else:
            # Find the chosen item
            if key == pygame.K_UP and self.cur_item > 0:
                self.cur_item -= 1
            elif key == pygame.K_UP and self.cur_item == 0:
                self.cur_item = len(self.items) - 1
            elif key == pygame.K_DOWN and self.cur_item < len(self.items) - 1:
                self.cur_item += 1
            elif key == pygame.K_DOWN and self.cur_item == len(self.items) - 1:
                self.cur_item = 0

        self.items[self.cur_item].set_italic(True)
        self.items[self.cur_item].set_font_color(GREEN)
            
            
    def set_mouse_visibility(self):
        if self.mouse_is_visible:
            pygame.mouse.set_visible(True)
        else:
            pygame.mouse.set_visible(False)
            
    def run(self):
        mainloop = True
        while mainloop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainloop = False
                    self.nextState = 0
                if event.type == pygame.KEYDOWN:
                    self.mouse_is_visible = False
                    self.set_keyboard_selection(event.key)

                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        text = self.items[self.cur_item].text
                        self.nextState = funcs[text]
                        mainloop = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mpos = pygame.mouse.get_pos()
                    for item in self.items:
                        if item.is_mouse_selection(mpos):
                            mainloop = False
                            self.nextState = self.funcs[item.text]
                        
                    
                    self.set_mouse_visibility()

            if pygame.mouse.get_rel() != (0, 0):
                self.mouse_is_visible = True
            self.set_mouse_visibility()
            # Redraw Background
            self.screen.fill(self.bg_color)

            for item in self.items:
                if self.mouse_is_visible:
                    mpos = pygame.mouse.get_pos()
                    self.set_mouse_selection(item, mpos)
                self.screen.blit(item.label, item.position)
                
            pygame.display.flip()
            
        return self.nextState


class MainMenu(State):
    def __init__(self, screen, clock, items, funcs, bg_color=(0,0,200), font="TimesNewRoman", font_size=30, font_color=(255, 255, 255)):

        super(MainMenu, self).__init__() # Init State Base Class
        self.screen = screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height
        
        self.bg_color = bg_color
        self.clock = clock
        self.font = pygame.font.SysFont(font, font_size)
        self.font_color = font_color

        self.mouse_is_visible = True

        self.funcs = funcs
        
        self.items = []
        self.cur_item = None
        for index, item in enumerate(items):
            menu_item = MenuItem(item)
            label = self.font.render(item, 1, self.font_color)

            # t_h: total height of text block
            t_h = len(items) * menu_item.height
            posx = (self.scr_width / 2) - (menu_item.width / 2)
            posy = (self.scr_height / 2) - (t_h / 2) + ((index * 2) + index * menu_item.height)
            menu_item.set_position(posx, posy)
            self.items.append(menu_item)
    

    def set_mouse_selection(self, item, mpos):
        #Marks the MenuItem the mouse cursor hovers on

        if item.is_mouse_selection(mpos):
            item.set_font_color(GREEN)
            item.set_italic(True)
        else:
            item.set_font_color(WHITE)
            item.set_italic(False)

    def set_keyboard_selection(self, key):
        # Marks the MenuItem chosen via up and down keys

        for item in self.items:
            # Return all to normal
            item.set_italic(False)
            item.set_font_color(WHITE)

        if self.cur_item is None:
            self.cur_item = 0
        else:
            # Find the chosen item
            if key == pygame.K_UP and self.cur_item > 0:
                self.cur_item -= 1
            elif key == pygame.K_UP and self.cur_item == 0:
                self.cur_item = len(self.items) - 1
            elif key == pygame.K_DOWN and self.cur_item < len(self.items) - 1:
                self.cur_item += 1
            elif key == pygame.K_DOWN and self.cur_item == len(self.items) - 1:
                self.cur_item = 0

        self.items[self.cur_item].set_italic(True)
        self.items[self.cur_item].set_font_color(GREEN)
            
            
    def set_mouse_visibility(self):
        if self.mouse_is_visible:
            pygame.mouse.set_visible(True)
        else:
            pygame.mouse.set_visible(False)
            
    def run(self):
        mainloop = True
        while mainloop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainloop = False
                    self.nextState = 0
                if event.type == pygame.KEYDOWN:
                    self.mouse_is_visible = False
                    self.set_keyboard_selection(event.key)

                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        text = self.items[self.cur_item].text
                        self.nextState = funcs[text]
                        mainloop = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mpos = pygame.mouse.get_pos()
                    for item in self.items:
                        if item.is_mouse_selection(mpos):
                            mainloop = False
                            self.nextState = self.funcs[item.text]
                        
                    
                    self.set_mouse_visibility()

            if pygame.mouse.get_rel() != (0, 0):
                self.mouse_is_visible = True
            self.set_mouse_visibility()
            # Redraw Background
            self.screen.fill(self.bg_color)

            for item in self.items:
                if self.mouse_is_visible:
                    mpos = pygame.mouse.get_pos()
                    self.set_mouse_selection(item, mpos)
                self.screen.blit(item.label, item.position)
                
            pygame.display.flip()
            
        return self.nextState
if __name__ == "__main__":
    
    # Init
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption('Pitch')
    screen = pygame.display.set_mode(SIZE, 0, 32)
    funcs = {'Start': 2,
             'Quit': 0}    
    states = {1: MainMenu(screen, clock, funcs.keys(), funcs),
              2: PreGameMenu(screen, clock, funcs.keys(), funcs),
              }

    
    # Initiate Game
    ## 
    
    # Main Loop
    #while True:
    #    deltat = clock.tick(FRAMES_PER_SECOND)
    #    for event in pygame.event.get():
    #        if event.type == pygame.QUIT:
    #            sys.exit()
    #
    #    screen.fill(GREEN)
    #    pygame.display.flip()
    
    # Start with Game Menu
    sm = StateManager(states)
    sm.start()
    
