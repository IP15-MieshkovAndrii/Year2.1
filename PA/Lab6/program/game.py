import pygame
import random as rand
from constants import *
from algorithm import State
from gcard import GCard, UserInput


class Game:
    """Pygame class"""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Last one")
        self.font = pygame.font.SysFont('Corbel',35)
        self.deck = []
        self.played = []
        self.player = []
        self.ai = []
        self.possible = []

        self.mode = 'start'
        self.melee = False
        self.turn = 'put 1'
        self.player_turn = True

        self.skip_button = False
        self.input = UserInput(INPUT_X, INPUT_Y, INPUT_WIDTH, INPUT_HEIGHT)

        self.create_deck()

    def create_deck(self):
        """Створити дек карт"""
        i = 0
        for suit in ['hearts', 'diamonds', 'clubs', 'spades']:
            values = list(range(2, 11)) + ['A', 'K', 'Q', 'J']
            for value in values:
                i += 1
                self.deck.append(GCard(str(value), suit, DECK_X, DECK_Y))
        self.deck.append(GCard('Jocker', 'r', DECK_X, DECK_Y))
        self.deck.append(GCard('Jocker', 'b', DECK_X, DECK_Y))
        rand.shuffle(self.deck)
        for i, card in enumerate(self.deck):
            card.move(i // 6, - i // 4)

    def center_player(self):
        """Відцентруємо усі карти гравця на екрані"""
        for i, card in enumerate(self.player):
            card.update(WIDTH // 2 - CARD_WIDTH * len(self.player) // 4 + i * CARD_WIDTH // 2, HEIGHT - CARD_HEIGHT // 2)

    def center_ai(self):
        """Відцентруємо усі карти ші на екрані"""
        for i, card in enumerate(self.ai):
            card.update(WIDTH // 2 - CARD_WIDTH * len(self.ai) // 4 + i * CARD_WIDTH // 2, CARD_HEIGHT // 2)

    def hand_cards(self):
        """Роздамо карти ші та гравцю"""
        for _ in range(8):
            current = self.deck.pop()
            current.flip()
            self.player.append(current)
            current = self.deck.pop()
            self.ai.append(current)

        self.center_player()
        self.center_ai()

    def suggest_cards(self):
        """Виділемо карти, можливі для ходу гравцем"""
        self.possible = []
        if not self.played or (self.played[-1].card.value == '3' and self.player_turn):
            for card in self.player:
                card.suggest()
                self.possible.append(card)
            self.deck[-1].suggest()
            self.possible.append(self.deck[-1])
            self.player_turn = False
            return
        if self.deck:
            self.deck[-1].suggest()
            self.possible.append(self.deck[-1])
        if self.played[-1].card.value == '2' and self.turn not in ['pick', 'skip', 'defeat']:
            return
        if self.played[-1].card.value == '4' and self.turn not in ['pick', 'skip', 'defeat']:
            self.melee = True
        if self.played[-1].card.value == 'J' and self.turn not in ['pick', 'skip', 'defeat']:
            self.skip_button = True
            self.unsuggest_cards()
            self.draw_window()
            return
        for card in self.player:
            if self.melee:
                if card.card.value == str(int(self.played[-1].card.value) + 1):
                    card.suggest()
                    self.possible.append(card)
            else:
                if card.card.value in ['8', 'Jocker']:
                    card.suggest()
                    self.possible.append(card)
                elif card.card.value == self.played[-1].card.value or card.card.suit == self.played[-1].card.suit:
                    card.suggest()
                    self.possible.append(card)
        if not self.possible:
            self.skip_button = True

    def unsuggest_cards(self):
        """Скасуємо виділення карт, можливих для ходу"""
        for card in self.player + self.played + self.deck:
            card.unsuggest()

    def ai_turn(self):
        """Хід ші"""
        turn, cards = State([card.card for card in self.ai], [card.card for card in self.played],
                            len(self.player), turn=self.turn, is_melee=self.melee).produce_next_turn()
        self.turn = turn
        if turn == 'put 1':
            card = cards[0]
            for c in self.ai:
                if c.card.value == card.value and c.card.suit == card.suit:
                    c.flip()
                    c.update(WIDTH // 2 + rand.randint(-15, 15), HEIGHT // 2 + rand.randint(-20, 20))
                    self.ai.remove(c)
                    self.played.append(c)
                    self.center_ai()
        elif turn == 'eight':
            new_value, new_suit = cards[0].value, cards[0].suit
            for c in self.ai:
                if c.card.value == '8':
                    c.flip()
                    c.make_new(new_value=new_value, new_suit=new_suit)
                    c.update(WIDTH // 2 + rand.randint(-15, 15), HEIGHT // 2 + rand.randint(-20, 20))
                    self.ai.remove(c)
                    self.played.append(c)
                    self.center_ai()
                    break
        elif turn == 'jocker':
            new_value, new_suit = cards[0].value, cards[0].suit
            for c in self.ai:
                if c.card.value == 'Jocker':
                    c.flip()
                    c.make_new(new_value=new_value, new_suit=new_suit)
                    c.update(WIDTH // 2 + rand.randint(-15, 15), HEIGHT // 2 + rand.randint(-20, 20))
                    self.ai.remove(c)
                    self.played.append(c)
                    self.center_ai()
                    break
        elif turn == 'pick':
            self.ai.append(self.deck.pop())
            self.center_ai()
        elif turn == 'put 2':
            first, second = cards
            for c in self.ai:
                if c.card.value == first.value and c.card.suit == first.suit:
                    c.flip()
                    c.update(WIDTH // 2 + rand.randint(-15, 15), HEIGHT // 2 + rand.randint(-20, 20))
                    self.ai.remove(c)
                    self.played.append(c)
                    self.center_ai()
            for c in self.ai:
                if c.card.value == second.value and c.card.suit == second.suit:
                    c.flip()
                    c.update(WIDTH // 2 + rand.randint(-15, 15), HEIGHT // 2 + rand.randint(-20, 20))
                    self.ai.remove(c)
                    self.played.append(c)
                    self.center_ai()
        elif turn == 'defeat':
            for _ in range(int(self.played[-1].card.value)):
                self.ai.append(self.deck.pop())
            self.center_ai()
            self.melee = False

    def process_click(self):
        """Обробка нажаття кнопки миші"""
        x, y = pygame.mouse.get_pos()
        # на кнопку скіп
        if self.skip_button and 0 <= x - SKIP_X <= WIDTH and 0 <= y - SKIP_Y <= HEIGHT:
            self.skip_button = False
            self.turn = 'skip'
            self.draw_window()
            self.ai_turn()
            self.suggest_cards()
            return
        if self.mode == 'start':
            if self.deck[-1].rect.collidepoint(pygame.mouse.get_pos()):
                self.hand_cards()
                self.mode = 'play'
                self.suggest_cards()
        else:
            # на стопку
            if self.deck[-1].rect.collidepoint(pygame.mouse.get_pos()):
                if self.melee:
                    for _ in range(int(self.played[-1].card.value)):
                        card = self.deck.pop()
                        card.flip()
                        self.player.append(card)
                    self.center_player()
                    self.unsuggest_cards()
                    self.draw_window()
                    self.turn = 'defeat'
                    self.melee = False
                    self.ai_turn()
                    self.suggest_cards()
                else:
                    card = self.deck.pop()
                    card.flip()
                    self.player.append(card)
                    self.center_player()
                    self.unsuggest_cards()
                    self.draw_window()
                    self.turn = 'pick'
                    self.ai_turn()
                    self.suggest_cards()

            else:
                # на карти гравця
                for card in self.player:
                    if 0 <= x - card.rect.left <= CARD_WIDTH // 2 and 0 <= y - card.rect.top <= CARD_HEIGHT:
                        if card in self.possible:
                            if card.card.value == '8':
                                self.turn = 'eight'
                                card.update(WIDTH // 2 + rand.randint(-15, 15), HEIGHT // 2 + rand.randint(-20, 20))
                                self.played.append(card)
                                self.player.remove(card)
                                self.center_player()
                                self.unsuggest_cards()
                                self.player_turn = True
                                break
                            elif card.card.value == 'Jocker':
                                self.turn = 'jocker'
                                card.update(WIDTH // 2 + rand.randint(-15, 15), HEIGHT // 2 + rand.randint(-20, 20))
                                self.played.append(card)
                                self.player.remove(card)
                                self.center_player()
                                self.unsuggest_cards()
                                self.player_turn = True
                                break
                            elif card.card.value == '3':
                                card.update(WIDTH // 2 + rand.randint(-15, 15), HEIGHT // 2 + rand.randint(-20, 20))
                                self.played.append(card)
                                self.player.remove(card)
                                self.center_player()
                                self.player_turn = True
                                self.suggest_cards()
                                break
                            elif card.card.value == '4':
                                self.melee = True

                            card.update(WIDTH // 2 + rand.randint(-15, 15), HEIGHT // 2 + rand.randint(-20, 20))
                            self.played.append(card)
                            self.player.remove(card)
                            self.center_player()
                            self.unsuggest_cards()
                            self.turn = 'put 1'
                            self.draw_window()
                            self.ai_turn()
                            self.suggest_cards()
                            break

    def process_input(self, event):
        """Обробка введень значень з клавіатури"""
        if event.key == pygame.K_BACKSPACE:
            self.input.str = self.input.str[:-1]
        elif event.key == pygame.K_RETURN:
            if self.turn == 'jocker':
                if self.input.str[:2] == '10':
                    value = '10'
                    suit = self.input.str[2:]
                else:
                    value = self.input.str[:1]
                    suit = self.input.str[1:]
            else:
                value = '8'
                suit = self.input.str
            if value in [str(x) for x in list(range(2, 11))] + ['A', 'K', 'Q', 'J'] and suit in ['hearts', 'diamonds', 'clubs', 'spades']:
                self.input.str = ''
                self.played[-1].make_new(value, suit)
                self.turn = 'put 1'
                self.draw_window()
                self.ai_turn()
                self.suggest_cards()
                self.player_turn = False
        else:
            self.input.str += event.unicode

    def draw_window(self):
        """Оновлення вікна гри"""
        self.screen.fill('darkgreen')
        for card in self.deck + self.played + self.player + self.ai:
            card.render(self.screen)
        if self.skip_button:
            pygame.draw.rect(self.screen, 'black', [SKIP_X, SKIP_Y, SKIP_WIDTH, SKIP_HEIGHT])
            text = self.font.render('skip', True, 'white')
            self.screen.blit(text, (SKIP_X+30, SKIP_Y))
        if self.turn == 'eight' and self.player_turn:
            self.input.render(self.screen, "hearts, diamonds, clubs, spades")
        elif self.turn == 'jocker' and self.player_turn:
            self.input.render(self.screen, "hearts, diamonds, clubs, spades")
        pygame.display.update()

    def main(self):
        """Початок роботи програми"""
        clock = pygame.time.Clock()
        run = True

        while run:
            clock.tick(FPS)
            self.draw_window()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                elif event.type == pygame.MOUSEBUTTONUP:
                    self.process_click()

                elif event.type == pygame.KEYDOWN and self.player_turn and self.turn in ['eight', 'jocker']:
                    self.process_input(event)