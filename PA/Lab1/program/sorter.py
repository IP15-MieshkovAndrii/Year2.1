from random import randint
import shutil


class Reader:
    """Клас, що представляє бінарний файл - два покажчики читання: поточний і наступний"""

    def __init__(self, path: str):
        self.path = path
        self.f = open(path, "rb")
        self.curr = self.f.read(16)
        self.next = self.f.read(16)

    def close(self):
        self.f.close()

    def __iter__(self):
        return self

    def __next__(self):
        """Повертає поточний покажчик і переміщує покажчики вперед на 1"""
        tmp = self.curr
        self.curr = self.next
        self.next = self.f.read(16)
        return tmp


class Sorter:
    def __init__(self, path_a: str, path_b: str, path_c: str):
        """Файл B і C очищено, файл A – ні"""
        self.path_a = path_a
        self.path_b = path_b
        self.path_c = path_c
        self.clear(path_b)
        self.clear(path_c)

    def generate_file(self, n: int, max_n: int):
        with open(self.path_a, "wb") as a:
            for i in range(n):
                a.write(randint(1, max_n).to_bytes(16, byteorder="big"))

    def copy_file(self, path: str):
        shutil.copy(path, self.path_a)

    def sort(self):
        while not self.is_sorted():
            self.distribute()
            self.merge()

    def __str__(self):
        a, b, c = "A: " + self.read(self.path_a), "B: " + self.read(self.path_b), "C: " + self.read(self.path_c)
        return "\n".join([x for x in [a, b, c] if x])

    def distribute(self):
        a = Reader(self.path_a)
        b = open(self.path_b, "wb")
        c = open(self.path_c, "wb")

        i = True
        while a.curr:
            b.write(a.curr) if i else c.write(a.curr)
            if a.curr > a.next:
                i = not i
            next(a)

        a.close(), b.close(), c.close()

    def merge(self):
        """
        Злиття відповідних серій.
            Якщо обидва дані числа не в кінці серії, ми знаходимо менше та дописуємо його, далі посуваємо
            покажчик - таким чином зливаючи ці дві серії.
            Тобто якщо число файлу В в кінці серії, то ми зливаємо актуальну серію файла В і залишки
            серії файла С. Якщо число із файла С менше, ми його дописуємо, а як тільки меншим
            виявиться останнє число серії із файла В, то ми це число дописуємо, і всі інші
            числа із серії із файла С так само дописуємо аж до кінця серії. Після цієї операції обидва
            покажчика будуть на початку нової серії.
            Аналогічно робимо якщо число файлу С в кінці серії.
            Якщо ж обидва числа в кінці серії, дописуємо їх по зростанню і зсуваємо покажчик на крок уперед,
            в результаті обидва покажчики на початку серії.
            Якщо покажчик в кінці файлу, дописуємо залишок іншого файлу.
        """
        a = open(self.path_a, "wb")
        b = Reader(self.path_b)
        c = Reader(self.path_c)
        while b.curr and c.curr:
            if b.curr <= b.next and c.curr <= c.next:
                if b.curr <= c.curr:
                    a.write(next(b))
                else:
                    a.write(next(c))
            elif b.curr >= b.next and c.curr <= c.next:
                while c.curr <= c.next:
                    if b.curr <= c.curr:
                        a.write(next(b))
                        while c.curr <= c.next:
                            a.write(next(c))
                        a.write(next(c))
                        break
                    else:
                        a.write(next(c))
            elif c.curr >= c.next and b.curr <= b.next:
                while b.curr <= b.next:
                    if c.curr <= b.curr:
                        a.write(next(c))
                        while b.curr <= b.next:
                            a.write(next(b))
                        a.write(next(b))
                        break
                    else:
                        a.write(next(b))
            else:
                if c.curr <= b.curr:
                    a.write(c.curr)
                    a.write(b.curr)
                else:
                    a.write(b.curr)
                    a.write(c.curr)
                next(c), next(b)

        if not b.curr and c.curr:
            while c.curr:
                a.write(next(c))
        elif not c.curr and b.curr:
            while b.curr:
                a.write(next(b))

        a.close(), b.close(), c.close()

    def is_sorted(self):
        """Перевірити, чи файл А вже відсортовано"""
        a = Reader(self.path_a)
        while a.next:
            if a.curr > a.next:
                a.close()
                return False
            next(a)
        a.close()
        return True

    @staticmethod
    def read(path: str) -> str:
        """Прочитати перші 30 чисел із файлу, поставивши «|» в кінці кожної серії"""
        s = ""
        f = Reader(path)

        for i in range(30):
            if not f.curr:
                break
            s += str(int.from_bytes(f.curr, byteorder="big")) + " "
            if f.curr > f.next:
                s += "| "
            next(f)

        f.close()
        return s

    @staticmethod
    def clear(path: str):
        with open(path, "wb"):
            pass
