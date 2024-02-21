from dataclasses import dataclass
import math
import random as rand


@dataclass(unsafe_hash=True)
class Card:
    value: str
    suit: str
    new: bool = False  # якщо карта отримана після зміни масті восьмірки або використання Джокера


def generate_all_cards():
    """Створення дека карт"""
    deck = []
    for suit in ['hearts', 'diamonds', 'clubs', 'spades']:
        values = list(range(2, 11)) + ['A', 'K', 'Q', 'J']
        for value in values:
            deck.append(Card(str(value), suit))
    deck.append(Card("Jocker", "r"))
    deck.append(Card("Jocker", "b"))  # щоб __eq__ диференціювало обидва Джокера
    return deck


ALL_CARDS = generate_all_cards()


class State:
    """Клас для опису стану гри"""
    def __init__(self, ai_cards: list, played: list, player_n: int,
                 turn: str = None, pos: float = None, is_melee: bool = None):
        """
        Ініціалізація
        :param ai_cards: карти на руках у ШІ
        :param played:  список зіграних карт
        :param player_n: кількість карт на руках у гравця
        :param turn: тип ходу, який привів до стану
        :param pos: ймовірність переходу в даний стан із попереднього
        :param is_melee: чи є стан частиною рукопашки
        """
        self.ai = list(ai_cards)
        self.played = list(played)
        self.player_n = player_n
        self.turn = turn
        self.pos = pos
        self.is_melee = is_melee

    @property
    def f(self):
        """Евристична функція"""
        # виграш ші
        if len(self.ai) <= 0:
            return 3
        # виграв гравець
        if self.player_n <= 0:
            return -3

        # список унікальних мастей
        suits = list(set([x.suit for x in self.ai]))
        suits_n = 4 if len(suits) == 5 else len(suits)

        # перший коефіцієнт, визначає рівень наявності усіх мастей
        alpha = 1 - 0.12 * (4 - suits_n)

        # другий коефіцієнт, залежить від кориисності карт на руках
        beta = 0

        for card in self.ai:
            if card.value == '2':
                # якщо гравець от-от виграє, краще скинути двійку
                if self.player_n <= 3:
                    beta += 0.5
                # якщо можна походити двійкою, змусити противника пропустити хід, і ще раз походити
                elif card.suit in suits:
                    beta += 3
                else:
                    beta += 1.7
            elif card.value == '3':
                beta += 2
            elif card.value == 'J':
                # якщо можна походити. змусити противника пропустити хід, і ще раз походити
                if card.suit in suits:
                    beta += 2
                else:
                    beta += 1.4
            elif card.value == 'Jocker':
                # якщо у противника мало ходів, то краще походити Джокером і можливо змусити взяти карту
                if self.player_n <= 3:
                    beta += 0.85
                else:
                    beta += 2
            elif card.value == '8':
                if self.player_n <= 3:
                    beta += 0.92
                else:
                    beta += 1.8
            elif card.value in ['5', '6', '7']:
                beta += 1.5
            elif card.value == '4':
                beta += 2
            else:
                beta += 1

        beta = beta / len(self.ai)

        return (self.player_n / len(self.ai)) * alpha * beta

    def produce_next_turn(self):
        """Повертає найкращий хід за алгоритмом мінімакс"""
        def minimax(state, depth, is_ai_turn):
            if depth == 0 or len(state.ai) == 0 or state.player_n == 0:
                return state.f

            sum = 0
            value = 0

            if is_ai_turn:
                for child in state.ai_children():
                    # якщо вибирається взяти карту, знаходимо матсподівання
                    if child.turn == "pick":
                        sum += minimax(child, depth-1, False) * child.pos

                    else:
                        value = max(value, minimax(child, depth-1, False))
                return max(value, sum)
            else:
                for child in state.player_children():
                    sum += minimax(child, depth-1, True) * child.pos
                return sum

        # якщо ходів немає то в залежності від того, чи є карти в деку, беремо карту або пропускаємо хід
        if not self.generate_possible(self.ai):
            if len(self.ai) + len(self.played) + self.player_n == 54:
                return "skip", 0
            return "pick", 0

        # якщо є лише один хід після ходу гравця
        if self.turn not in ['pick', 'skip', 'defeat']:
            if self.played[-1].value == '2':
                return "pick", 0
            elif self.played[-1].value == 'J':
                return "skip", 0

        # знаходимо найбільше значення мінімакс для кожних наступних можливих ходів ші, заглиблення на 3 півкроки
        r = max([(child, minimax(child, 2, False)) for child in self.ai_children()], key=lambda x: x[1])[0]

        if r.turn in ["skip", "pick", "defeat"]:
            return r.turn, 0
        elif r.turn == "put 2":
            return r.turn, r.played[-2:]
        else:
            return r.turn, r.played[-1:]

    def generate_possible(self, cards):
        """Із заданих карт вибирає такі, які можна поставити на останню із зіграних"""
        possible = []
        if not self.played:
            return list(self.ai)
        for card in cards:
            # можу ходити на будь-яку
            if card.value in ['8', 'Jocker']:
                possible.append(card)
                continue

            if card.value == self.played[-1].value or card.suit == self.played[-1].suit:
                possible.append(card)

        return possible

    def ai_children(self):
        """Повернути можливі нові стани та ймовірнісні стани після взяття карти зі стопки"""
        # доступні карти для ходу
        possible = self.generate_possible(self.ai)

        # потенціальні карти, що можуть бути отримані зі стопки
        potential = [card for card in ALL_CARDS if card not in self.ai + self.played]

        children = []

        if self.turn in ["put 1", "put 2"]:
            # якщо суперник поставив 2, потрібно взяти 1 карту і пропустити свій хід
            if self.played[-1].value == '2':
                return [State(self.ai + [card], self.played, self.player_n,
                              "pick", 1 / len(potential)) for card in potential]

            # якщо суперник поставив J, пропуск ходу
            if self.played[-1].value == 'J':
                return [State(self.ai, self.played, self.player_n, "skip")]

            # якщо рукопашка, то треба або поставити значення попередньої карти + 1, або взяти кількість карт,
            # що дорівнюють значенню попередньої карти
            if self.is_melee or self.played[-1].value == '4':
                needed = str(int(self.played[-1].value) + 1)
                for card in self.ai:
                    if card.value == needed:
                        ai = list(self.ai)
                        ai.remove(card)
                        children.append(State(ai, self.played + [card], self.player_n, "put 1", is_melee=True))

                # близько 2 млн+ станів може утворитися якщо перераховувати всі можливі взяті 4+ карти зі стопки,
                # треба використати якийсь інший метод, наприклад випадковим чином набрати карти із
                # потенціальних, це не буде дорівнювати математичному сподіванню, але за центральною граничною
                # теоремою, цей результат буде відносно близьким. До того ж, агент max і так намагатиметься
                # уникати різкого збільшення кількості карт на руці, і скоріше за все, самий розподіл карт на
                # руці гратиме меншу роль
                if not children:
                    ai = list(self.ai)
                    for _ in range(int(self.played[-1].value)):
                        f = rand.choice(potential)
                        potential.remove(f)
                        ai += f,
                    children.append(State(ai, self.played, self.player_n, "defeat", is_melee=None))
                return children
        # знаходимо нові стани після ходів картами на руках
        for card in possible:
            # якщо трійка, то нові стани будуть формувати комбінації карт трійки і нової якоїсь обраної карти
            if card.value == '3':
                seconds = list(self.ai)
                seconds.remove(card)
                for second in seconds:
                    ai = list(self.ai)
                    ai.remove(card)
                    ai.remove(second)
                    children.append(State(ai, self.played + [card] + [second], self.player_n, "put 2"))
                ai = list(self.ai)
                ai.remove(card)
                children.append(State(ai, self.played + [card], self.player_n, "put 1"))

            # якщо 8, створюємо нові стани для кожної із можливих обраних мастей
            elif card.value == '8':
                ai = list(self.ai)
                ai.remove(card)
                for suit in ['hearts', 'diamonds', 'clubs', 'spades']:
                    children.append(State(ai, self.played + [Card('8', suit, True)],
                                          self.player_n, "eight"))

            # якщо Jocker, створюємо нові стани для кожної із можливих обраних карток
            elif card.value == 'Jocker':
                for suit in ['hearts', 'diamonds', 'clubs', 'spades']:
                    values = list(range(2, 11)) + ['A', 'K', 'Q', 'J']
                    for value in values:
                        ai = list(self.ai)
                        ai.remove(card)
                        children.append(State(ai, self.played + [Card(str(value), suit, True)],
                                              self.player_n, 'jocker'))
            # інакше просто формуєммо стани із походженою картою
            else:
                ai = list(self.ai)
                ai.remove(card)
                children.append(State(ai, self.played + [card], self.player_n, "put 1"))

        # якщо немає карт в стопці то повертаємо знайдені стани, якщо таких немає, пропускаємо хід
        if len(self.ai) + len(self.played) + self.player_n == 54:
            if children:
                return children
            return [State(self.ai, self.played, self.player_n, "skip")]

        # знаходимо нові стани після взяття карти зі стопки
        for card in potential:
            p = 1 / len(potential)
            children.append(State(self.ai + [card], self.played, self.player_n, "pick", p))

        return children

    def player_children(self):
        """
        Повернути йомвірнісну модель можливих ходів гравця
        Оскільки ми не можемо визначити всі комібнації карт, які можуть бути у суперника,
        бо їх порядку math.comb(44, 8) = 177 232 627, знаходимо приблизні ймовірності тих чи інших ходів,
        по-перше, знаючи ймовірність того, що гравцю доведеться брати карту зі стовпки,
        по-друге, розуміючи, що гравець буде менш схильний ставити сильну карту на початку гри
        і намагатися поставити карту, яка зупинить від виграшу ші, в кінці гри
        """

        # потенціальні карти, що не в руках у ші і не зіграні
        potential = [card for card in ALL_CARDS if card not in self.ai + self.played]

        # ті карти з потенційних, які можуть ходити
        possible = self.generate_possible(potential)

        children = []

        if self.turn in ["put 1", "put 2"]:
            # якщо ші поставив 2, потрібно взяти 1 карту і пропустити свій хід
            if self.played[-1].value == '2':
                return [State(self.ai, self.played, self.player_n + 1, "pick", 1)]

            # якщо ші поставив J, пропуск ходу
            if self.played[-1].value == 'J':
                return [State(self.ai, self.played, self.player_n, "skip", 1)]

            # якщо ші поставив 4, то початок рукопашки, обчислюємо ймовірності того що попадеться 5
            # і яка з п'ятірок, і ймовірність що не попадеться
            if self.played[-1].value == '4':
                n = len(potential)
                m = self.player_n
                k = sum([1 for x in potential if x.value == '5'])
                not_five_p = math.comb(n-k, m) / math.comb(n, m)
                five_p = 1 - not_five_p
                # немає зміни функції в залежності від того, яку п'ятірку ставити, тому просто два стани
                return [State(self.ai, self.played, self.player_n + 1, "put 1", five_p, is_melee=True),
                        State(self.ai, self.played, self.player_n + 4, "defeat", not_five_p, is_melee=None)]

            # якщо рукопашка або ші поставив 4, обчислюємо ймовірності того що не попадеться жадана карта,
            # і що попадеться, на основі цього будуємо ймовірнісну модель і розкриваємо в два стани
            if self.is_melee or self.played[-1].value == '4':
                needed = str(int(self.played[-1].value) + 1)
                n = len(potential)
                m = self.player_n
                k = sum([1 for x in potential if x.value == needed])
                not_needed_p = math.comb(n-k, m) / math.comb(n, m)
                needed_p = 1 - not_needed_p
                # немає зміни функції в залежності від того, яку жадану карту ставити, тому просто два стани
                return [State(self.ai, self.played, self.player_n + 1, "put 1", needed_p, is_melee=True),
                        State(self.ai, self.played, self.player_n + int(self.played[-1].value), "defeat", not_needed_p,
                              is_melee=None)]

        n = len(potential)
        m = self.player_n
        k = len(possible)

        # розберемося із функцією розподілу ймовірностей для тих кард, які можливі для ходу із потенціальних
        weights = {x: 10 for x in possible}

        # фактично обернені значення до використаних у функції оцінки
        for card in possible:
            if card.value == '2':
                if len(self.ai) <= 3:
                    weights[card] *= 2
                else:
                    weights[card] *= 0.6
            elif card.value == '3':
                weights[card] *= 0.5
            elif card.value == 'J':
                weights[card] *= 0.8
            elif card.value == 'Jocker':
                if len(self.ai) <= 3:
                    weights[card] *= 1.3
                else:
                    weights[card] *= 0.5
            elif card.value == '8':
                if self.player_n <= 3:
                    weights[card] *= 1.1
                else:
                    weights[card] *= 0.6
            elif card.value in ['5', '6', '7']:
                weights[card] *= 0.7
            elif card.value == '4':
                weights[card] *= 0.5

        # ймовірність того що на руках у противника не виявиться жодної карти, доступної до ходу
        p_impossible = math.comb(n-k, m) / math.comb(n, m)
        p_possible = 1 - p_impossible
        one_weight_p = p_possible / sum(weights.values())

        # якщо є ненульовий шанс що не виявиться жодної карти, додаємо такий дочірній стан,
        # або брати карту, або пропускати хід
        if p_impossible:
            if len(self.ai) + len(self.played) + self.player_n == 54:
                children.append(State(self.ai, self.played, self.player_n, "skip", p_impossible))
            else:
                children.append(State(self.ai, self.played, self.player_n + 1, "pick", p_impossible))

        # всі інші потенційні ходи також додаємо
        for card in possible:
            # ще може покласти карту
            if card.value == '3':
                p = list(possible)
                p.remove(card)
                for second in p:
                    children.append(State(self.ai, self.played + [card] + [second], self.player_n - 2,
                                          "put 2", weights[card] * one_weight_p / (n + 1)))
                children.append(State(self.ai, self.played + [card], self.player_n - 1,
                                      "put 1", weights[card] * one_weight_p / (n + 1)))
            # може вибрати будь-яку масть
            elif card.value == '8':
                for suit in ['hearts', 'diamonds', 'clubs', 'spades']:
                    children.append(State(self.ai, self.played + [Card('8', suit, True)], self.player_n - 1,
                                          'eight', weights[card] * one_weight_p / 4))
            # може вибрати будь-яку карту
            elif card.value == 'Jocker':
                for suit in ['hearts', 'diamonds', 'clubs', 'spades']:
                    values = list(range(2, 11)) + ['A', 'K', 'Q', 'J']
                    for value in values:
                        children.append(State(self.ai, self.played + [Card(str(value), suit, True)],
                                              self.player_n - 1, 'Jocker', weights[card] * one_weight_p / 52))
            else:
                children.append(State(self.ai, self.played + [card], self.player_n - 1, "put 1",
                                      weights[card] * one_weight_p))

        return children