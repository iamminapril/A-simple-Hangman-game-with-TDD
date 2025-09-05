import random
import time
import tkinter as tk
from tkinter import messagebox


def load_words_from_file(file_path):
    """Load words or phrases from a given file."""
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]


class Hangman:
    """Core Hangman game logic."""
    def __init__(self, answer=None, level='basic', lives=6, word_file='words.txt',
                 phrase_file='phrases.txt', dictionary=None):
        self.level = level
        self.lives = lives
        self.word_list = load_words_from_file(word_file)
        self.phrase_list = load_words_from_file(phrase_file)
        self.dictionary = dictionary if dictionary else set(self.word_list + self.phrase_list)
        self.answer = answer if answer is not None else self.generate_answer()
        if dictionary and not self.is_valid_answer(self.answer):
            raise ValueError("Answer not in dictionary")
        self.guessed = set()
        self.last_guess_time = None

    def is_valid_answer(self, answer):
        """Check if the answer is valid."""
        return answer in self.dictionary

    def generate_answer(self):
        """Generate a random answer based on difficulty level."""
        if self.level == 'basic':
            return random.choice(self.word_list)
        elif self.level == 'intermediate':
            return random.choice(self.phrase_list)
        else:
            raise ValueError("Invalid level")

    def display_word(self):
        """Return the current word display with guessed letters."""
        return ' '.join([c if (c in self.guessed or not c.isalpha()) else '_' for c in self.answer])

    def guess(self, letter):
        """Process a player's guess and update lives."""
        letter = letter.lower()
        if letter in self.guessed:
            return "already_guessed"
        self.guessed.add(letter)
        if letter not in self.answer.lower():
            self.lives -= 1
            return "wrong"
        return "correct"

    def check_timeout(self, start_time, timeout=15):
        """Deduct a life if guess exceeds timeout."""
        if time.time() - start_time > timeout:
            self.lives -= 1
            self.last_guess_time = time.time()

    def is_won(self):
        """Check if the game is won."""
        return all(c in self.guessed or not c.isalpha() for c in self.answer)

    def is_lost(self):
        """Check if the game is lost."""
        return self.lives <= 0

    def game_over_message(self):
        """Return a message when the game is over."""
        if self.is_lost():
            return "Game Over! You lost."
        return ""

    def get_guessed_letters(self):
        """Return a list of guessed letters."""
        return list(self.guessed)


class HangmanGUI:
    """GUI for Hangman game using Tkinter."""
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game")
        self.root.geometry("400x400")
        self.time_left = 15
        self.timer_id = None
        self.timer_running = None
        self.hangman = None
        self.level = None

        self.welcome_frame = tk.Frame(root)
        self.game_frame = tk.Frame(root)
        self.show_welcome()

    def show_welcome(self):
        """Display welcome screen with difficulty selection."""
        self.welcome_frame.pack(fill="both", expand=True)

        welcome_label = tk.Label(self.welcome_frame, text="Welcome to Hangman!", font=("Arial", 18))
        welcome_label.pack(pady=20)

        basic_button = tk.Button(self.welcome_frame, text="Basic", font=("Arial", 14),
                                 command=lambda: self.start_game(level='basic'))
        basic_button.pack(pady=5)

        intermediate_button = tk.Button(self.welcome_frame, text="Intermediate", font=("Arial", 14),
                                        command=lambda: self.start_game(level='intermediate'))
        intermediate_button.pack(pady=5)

        instruction_label = tk.Label(self.welcome_frame, text="Please select a level to start.", font=("Arial", 12))
        instruction_label.pack(pady=20)

    def start_game(self, level):
        """Start the game with selected difficulty level."""
        self.level = level
        self.welcome_frame.pack_forget()
        self.hangman = Hangman(level=self.level)
        self.build_game_ui()
        self.game_frame.update_idletasks()
        self.update_display()
        self.reset_timer()

    def build_game_ui(self):
        """Build the main game UI."""
        self.game_frame.pack(fill="both", expand=True)

        self.word_label = tk.Label(self.game_frame, text="", font=("Arial", 20))
        self.word_label.pack(pady=10)

        self.lives_label = tk.Label(self.game_frame, text="", font=("Arial", 14))
        self.lives_label.pack()

        self.timer_label = tk.Label(self.game_frame, text="Time left: 15", font=("Arial", 14))
        self.timer_label.pack()

        self.ascii_label = tk.Label(self.game_frame, text="", font=("Courier", 12), justify="left")
        self.ascii_label.pack(pady=10)

        self.entry = tk.Entry(self.game_frame, font=("Arial", 14))
        self.entry.pack(pady=10)
        self.entry.bind("<Return>", lambda event: self.make_guess())

        guess_button = tk.Button(self.game_frame, text="Guess", font=("Arial", 14), command=self.make_guess)
        guess_button.pack()

    def make_guess(self):
        """Handle player's guess input."""
        letter = self.entry.get().strip().lower()
        self.entry.delete(0, tk.END)

        if not letter or len(letter) != 1 or not letter.isalpha():
            messagebox.showwarning("Invalid", "Please enter a single letter.")
            return

        result = self.hangman.guess(letter)
        if result == "wrong":
            messagebox.showinfo("Wrong", f"'{letter}' is not in the word! Life lost.")
        elif result == "already_guessed":
            messagebox.showinfo("Oops", f"Oops! You already guessed '{letter}'.")

        self.update_display()

        if self.hangman.is_won():
            self.end_game(won=True)
        elif self.hangman.is_lost():
            self.end_game(won=False)

        self.reset_timer()

    def update_display(self):
        """Update displayed word, lives, and hangman ASCII art."""
        self.word_label.config(text=self.hangman.display_word())
        self.lives_label.config(text=f"Lives remaining: {self.hangman.lives}")

        # Hangman ASCII art stages
        stages = [
            """
  _______
 |/      |
 |       
 |      
 |       
 |      
 |
_|___
""",
            """
  _______
 |/      |
 |      (_)
 |      
 |       
 |      
 |
_|___
""",
            """
  _______
 |/      |
 |      (_)
 |      \|
 |       
 |      
 |
_|___
""",
            """
  _______
 |/      |
 |      (_)
 |      \|/
 |       
 |      
 |
_|___
""",
            """
  _______
 |/      |
 |      (_)
 |      \|/
 |       |
 |      
 |
_|___
""",
            """
  _______
 |/      |
 |      (_)
 |      \|/
 |       |
 |      / 
 |
_|___
""",
            """
  _______
 |/      |
 |      (_)
 |      \|/
 |       |
 |      / \\
 |
_|___
"""
        ]
        lives_index = 6 - self.hangman.lives
        if lives_index >= len(stages):
            lives_index = len(stages) - 1
        self.ascii_label.config(text=stages[lives_index])

        self.root.update_idletasks()

    def reset_timer(self):
        """Reset the countdown timer."""
        self.time_left = 15
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
        self.update_timer()

    def update_timer(self):
        """Update the timer each second."""
        if self.time_left > 0:
            self.timer_label.config(text=f"Time left: {self.time_left}")
            self.time_left -= 1
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            self.hangman.lives -= 1
            self.update_display()
            if self.hangman.is_lost():
                self.end_game(won=False)
            else:
                messagebox.showwarning("Timeout", "You ran out of time! Life lost.")
                self.reset_timer()

    def end_game(self, won):
        """Show game over message and close the window."""
        self.update_display()
        self.timer_running = False
        msg = "You Won!" if won else f"You Lost! The word was '{self.hangman.answer}'."
        messagebox.showinfo("Game Over", msg)
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = HangmanGUI(root)
    root.mainloop()

