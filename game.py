import random
from words import WORDS, HINTS
from stats import SessionStats


DIFFICULTIES = {
    "easy": {"lives": 8, "multiplier": 1},
    "medium": {"lives": 6, "multiplier": 2},
    "hard": {"lives": 4, "multiplier": 3},
}


class HangmanGame:
    def __init__(self):
        # Session state
        self.score = 0
        self.streak = 0
        self.stats = SessionStats()

        self.category = "technology"
        self.difficulty = "medium"

        # Round state
        self.secret = ""
        self.guessed = set()
        self.wrong = set()
        self.lives = 6
        self.hint_used = False

    def start_round(self):
        self.secret = random.choice(WORDS[self.category])
        self.guessed.clear()
        self.wrong.clear()
        self.lives = DIFFICULTIES[self.difficulty]["lives"]
        self.hint_used = False

    def masked(self):
        return " ".join(
            ch if ch in self.guessed else "_"
            for ch in self.secret
        )

    # FIX: Restore the missing win-checking method.
    def won(self):
        return all(
            ch in self.guessed
            for ch in set(self.secret)
        )

    def guess(self, letter):
        if len(letter) != 1 or not letter.isalpha():
            return "Enter one letter."

        # Task 1: prevent repeated correct and wrong guesses.
        if letter in self.guessed or letter in self.wrong:
            return "Already guessed."

        if letter in self.secret:
            self.guessed.add(letter)
            return "Correct."

        self.wrong.add(letter)
        self.lives -= 1
        return "Wrong."

    def use_hint(self):
        if self.hint_used:
            return None

        hint = HINTS.get(self.secret)

        if hint is None:
            return "No hint available."

        self.hint_used = True
        return hint

    def play_round(self):
        self.start_round()
        difficulty = DIFFICULTIES[self.difficulty]

        print(
            f"\nDifficulty: {self.difficulty.title()} "
            f"| Lives: {self.lives} "
            f"| Multiplier: x{difficulty['multiplier']}"
        )

        while self.lives > 0 and not self.won():
            print("\nWord:", self.masked())
            print("Wrong:", " ".join(sorted(self.wrong)) or "-")
            print(
                "Lives:", self.lives,
                "Score:", self.score,
                "Streak:", self.streak
            )

            raw = input("Letter, /hint, or /quit: ").strip().lower()

            if raw == "/quit":
                print("Quitting session.")
                return False

            if raw == "/hint":
                hint = self.use_hint()

                if hint is None:
                    print("Hint already used.")
                else:
                    print(hint)

                continue

            if raw.startswith("/"):
                print("Unknown command.")
                continue

            print(self.guess(raw))

        if self.won():
            self.streak += 1
            self.stats.record(True, self.streak)

            round_score = (
                (5 + self.streak) * difficulty["multiplier"]
            )

            if self.hint_used:
                round_score -= difficulty["multiplier"]

            round_score = max(0, round_score)
            self.score += round_score

            print("Solved:", self.secret)
            print("Round score:", round_score)
            return True

        self.streak = 0
        self.stats.record(False, self.streak)

        print("Out of lives. The word was:", self.secret)
        print("Round score: 0")
        return True

    def run(self):
        print("Hangman Challenge")
        print("A session consists of multiple rounds.")

        while True:
            print("\nCategories:", ", ".join(WORDS))
            raw = input("Choose category or q: ").strip().lower()

            if raw == "q":
                break

            if raw not in WORDS:
                print("Unknown category.")
                continue

            self.category = raw

            while True:
                raw = input(
                    "Choose difficulty [easy/medium/hard]: "
                ).strip().lower()

                if raw in DIFFICULTIES:
                    self.difficulty = raw
                    break

                print("Unknown difficulty.")

            if not self.play_round():
                break

            again = input("Another round? [y/n]: ").strip().lower()

            if again != "y":
                break

        print("\nFinal score:", self.score)
        print("Final streak:", self.streak)
        print("Rounds played:", self.stats.rounds)
        print("Rounds won:", self.stats.wins)
        print("Best streak:", self.stats.best_streak)


if __name__ == "__main__":
    HangmanGame().run()
