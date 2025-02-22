import random

class Slot:
    """
    Simulasi game slot dengan implementasian pola gacor.
    """
    def __init__(self, bet_amount: int, t_pattern: int) -> None:
        self.bet_amount = bet_amount
        self.multi = {
            "🍒": 0.0075,
            "🍓": 0.0075,
            "🫐": 0.0075,
            "🥭": 0.0075,
            "🍍": 0.0075,
            "🍋": 0.0075,
            "🍌": 0.0075,
            "🍉": 0.0075,
            "🍇": 0.0075,
            "🥝": 0.0075,
            "♠️": 0.0175,
            "♣️": 0.0175,
            "♥️": 0.0175,
            "♦️": 0.0175,
            "💵": 0.275,
            "💰": 0.275,
            "🏆": 0.275,
            "7️⃣": 5.625,
        }
        self.emotes = self.build_emotes()
        self.triggered_pattern = 0
        self.t_pattern = t_pattern

    def get_random_index(self, max_val):
        return random.randint(0, max_val - 1)

    def build_emotes(self):
        kategori_buah = ["🍒", "🍓", "🫐", "🥭", "🍍", "🍋", "🍌", "🍉", "🍇", "🥝"]
        kategori_simbol = ["♠️", "♣️", "♥️", "♦️"]
        kategori_benda = ["💵", "💰", "🏆"]
        kategori_angka = ["7️⃣"]

        probabilitas_buah = 0.70
        probabilitas_simbol = 0.2
        probabilitas_benda = 0.099
        probabilitas_angka = 0.001

        jumlah_item = 100
        array_item = []

        for i in range(int(jumlah_item * probabilitas_buah)):
            array_item.append(random.choice(kategori_buah))

        for i in range(int(jumlah_item * probabilitas_simbol)):
            array_item.append(random.choice(kategori_simbol))

        for i in range(int(jumlah_item * probabilitas_benda)):
            rand = random.random()
            if rand <= 0.5:
                array_item.append(kategori_benda[0])
            elif rand <= 0.85:
                array_item.append(kategori_benda[1])
            else:
                array_item.append(kategori_benda[2])

        for i in range(int(jumlah_item * probabilitas_angka)):
            array_item.append(kategori_angka[0])

        random.shuffle(array_item)

        return array_item

    def calculate_multiplier(self, numX):
        if numX == 3:
            return 1
        elif numX == 2:
            return 1.25
        elif numX == 1:
            return 2.5
        else:
            return 5

    def calculate_win(self, emo, pattern):
        is_pattern_matching = True
        multiplier = 0
        numX = 0

        for i, rowIndex in enumerate(pattern):
            if rowIndex == "x":
                numX += 1
            elif emo[i][rowIndex] != emo[0][pattern[0]]:
                is_pattern_matching = False
                break

        if is_pattern_matching:
            for i, rowIndex in enumerate(pattern):
                if rowIndex != "x":
                    emoji = emo[i][rowIndex]
                    multiplier += self.multi[emoji]
            multiplier *= self.calculate_multiplier(numX)

        win = self.bet_amount * multiplier if is_pattern_matching else 0
        if win != 0:
            self.triggered_pattern += 1

        return win

    def generate_patterns(self, num_patterns, rows, columns):
        patterns = []

        for _ in range(num_patterns):
            pattern = []
            xnum = 0
            for _ in range(columns):
                if random.random() < 0.3 and xnum < 3:
                    pattern.append("x")
                    xnum += 1
                else:
                    pattern.append(self.get_random_index(rows))
            patterns.append(pattern)

        return patterns

    def play_game(self):
        u = [self.emotes[random.randint(0, len(self.emotes) - 1)] for _ in range(5)]
        v = [self.emotes[random.randint(0, len(self.emotes) - 1)] for _ in range(5)]
        w = [self.emotes[random.randint(0, len(self.emotes) - 1)] for _ in range(5)]
        x = [self.emotes[random.randint(0, len(self.emotes) - 1)] for _ in range(5)]
        y = [self.emotes[random.randint(0, len(self.emotes) - 1)] for _ in range(5)]
        z = [self.emotes[random.randint(0, len(self.emotes) - 1)] for _ in range(5)]

        emo = [
            [u[0], v[0], w[0], x[0], y[0], z[0]],
            [u[1], v[1], w[1], x[1], y[1], z[1]],
            [u[2], v[2], w[2], x[2], y[2], z[2]],
            [u[3], v[3], w[3], x[3], y[3], z[3]]
        ]

        total_rewards = 0
        emotes = f"{u[0]} : {v[0]} : {w[0]} : {x[0]} : {y[0]} : {z[0]}\n{u[1]} : {v[1]} : {w[1]} : {x[1]} : {y[1]} : {z[1]}\n{u[2]} : {v[2]} : {w[2]} : {x[2]} : {y[2]} : {z[2]}\n{u[3]} : {v[3]} : {w[3]} : {x[3]} : {y[3]} : {z[3]}\n"

        numRows = 4
        numColumns = 6
        numPatternsToGenerate = self.t_pattern

        patterns = self.generate_patterns(numPatternsToGenerate, numRows, numColumns)
        patterns_error = 0

        for pattern in patterns:
            try:
                total_rewards += self.calculate_win(emo, pattern)
            except:
                patterns_error += 1
                continue

        return {
            "rewards": round(total_rewards),
            "emotes": emotes,
            "patterns_error": patterns_error,
            "triggered_pattern": self.triggered_pattern
        }