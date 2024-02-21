from algorithm import Card
import pygame
from constants import *


class GCard:
    """Карти разом із їхніми pygame репрезентаціями"""
    def __init__(self, value, suit, x, y, new=False):
        self.card = Card(value, suit, new)

        self.is_front = False
        self.is_suggest = False

        self.back = pygame.transform.scale(pygame.image.load("img/back.jpg"),
                                           (CARD_WIDTH, CARD_HEIGHT))
        self.s_back = pygame.transform.scale(pygame.image.load("img/back.jpg"),
                                             (CARD_WIDTH, CARD_HEIGHT))
        pygame.draw.rect(self.s_back, "red", [0, 0, CARD_WIDTH, CARD_HEIGHT], 3)

        self.front = pygame.transform.scale(pygame.image.load(f"img/{value.upper()}{suit.upper()[0]}.jpg"),
                                            (CARD_WIDTH, CARD_HEIGHT))
        self.s_front = pygame.transform.scale(pygame.image.load(f"img/{value.upper()}{suit.upper()[0]}.jpg"),
                                              (CARD_WIDTH, CARD_HEIGHT))
        pygame.draw.rect(self.s_front, "red", [0, 0, CARD_WIDTH, CARD_HEIGHT], 3)

        self.image = self.back
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def flip(self):
        """Перевернути карту """
        self.is_front = not self.is_front
        self.update_image()

    def suggest(self):
        """Зробити зображення карти з червоною рамкою"""
        self.is_suggest = True
        self.update_image()

    def unsuggest(self):
        """Зробити зображення карти без червоної рамки"""
        self.is_suggest = False
        self.update_image()

    def update_image(self):
        """Оновити зображення карти в залежності чи з рамкою і чи сорочка"""
        if self.is_front:
            if self.is_suggest:
                self.image = self.s_front
            else:
                self.image = self.front
        else:
            if self.is_suggest:
                self.image = self.s_back
            else:
                self.image = self.back

    def render(self, screen):
        """Рендер карти"""
        screen.blit(self.image, self.rect)

    def update(self, x, y):
        """Оновлення положення карти"""
        self.rect.center = (x, y)

    def move(self, x, y):
        """Оновлення положення карти у відносних вираженнях"""
        self.rect.center = (self.rect.center[0] + x, self.rect.center[1] + y)

    def make_new(self, new_value, new_suit):
        """Зміна масті чи значення якщо вибрана карта була 8 або джокер"""
        self.card = Card(new_value, new_suit, True)

        self.front = pygame.transform.scale(pygame.image.load(f"/img/{new_value.upper()}{new_suit.upper()[0]}.jpg"),
                                            (CARD_WIDTH, CARD_HEIGHT))
        self.s_front = pygame.transform.scale(pygame.image.load(f"/img/{new_value.upper()}{new_suit.upper()[0]}.jpg"),
                                              (CARD_WIDTH, CARD_HEIGHT))
        pygame.draw.rect(self.s_front, "red", [0, 0, CARD_WIDTH, CARD_HEIGHT], 3)

        self.image = self.front


class UserInput:
    """Поле введення інформації про нову карту від гравця"""
    def __init__(self, left, top, width, height):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        pygame.font.init()
        self.font = pygame.font.SysFont('Corbel', 35)
        self.smallfont = pygame.font.SysFont('Corbel', 11)

        self.str = ''

    def render(self, screen, suggest_str):
        """Рендер поля введення"""
        pygame.draw.rect(screen, 'black', [self.left, self.top, self.width, self.height])
        screen.blit(self.font.render(self.str, True, 'white'),
                    (self.left, self.top))
        screen.blit(self.smallfont.render(suggest_str, True, 'black'),
                     (self.left, self.top + 50))