import unittest
from hangman import Hangman
from hangman import HangmanGUI
import tkinter as tk
import time

class TestHangman(unittest.TestCase):
    def test_initial_underscores(self):
        game = Hangman(answer="apple")
        self.assertEqual(game.display_word(), "_ _ _ _ _")

    def test_correct_guess(self):
        game = Hangman(answer="apple")
        game.guess('a')
        self.assertEqual(game.display_word(), "a _ _ _ _")

    def test_wrong_guess_deducts_life(self):
        game = Hangman(answer="apple", lives= 5)
        game.guess('x')
        self.assertEqual(game.lives, 4)   # life should be deducted
        self.assertEqual(game.display_word(), "_ _ _ _ _")  # still all underscores

    def test_win_condition(self):
        game = Hangman(answer="apple")
        for letter in set("apple"):
            game.guess(letter)
        self.assertTrue(game.is_won())
        self.assertFalse(game.is_lost())

    def test_lose_condition(self):
        game = Hangman(answer="apple", lives=2)
        game.guess('b') 
        game.guess('c') 
        self.assertFalse(game.is_won())
        self.assertTrue(game.is_lost())
        self.assertEqual(game.game_over_message(), "Game Over! You lost.")

    def test_phrase_support(self):
        game = Hangman(answer="hello world")
        self.assertEqual(game.display_word(), "_ _ _ _ _   _ _ _ _ _")
        game.guess('h')
        game.guess('e')
        game.guess('l')
        game.guess('o')
        game.guess('w')
        game.guess('r')
        game.guess('d')
        self.assertEqual(game.display_word(), "h e l l o   w o r l d")
        self.assertTrue(game.is_won())

    def test_show_guessed_letters(self):
        game = Hangman(answer="apple")
        game.guess('a')
        game.guess('e')
        game.guess('x')
        guessed = game.get_guessed_letters()
        self.assertEqual(set(guessed), {'a', 'e', 'x'})
    
    def test_basic_level(self):
        game = Hangman(level='basic')
        self.assertIn(game.answer, game.word_list)

    def test_intermediate_level(self):
        game = Hangman(level='intermediate')
        self.assertIn(game.answer, game.phrase_list)

    def test_answer_in_dictionary(self):
        dictionary = {'apple', 'banana', 'orange', 'ice cream', 'hot dog', 'green tea'}
        game = Hangman(answer='banana', dictionary=dictionary)
        self.assertTrue(game.is_valid_answer(game.answer))
        with self.assertRaises(ValueError):
            Hangman(answer='notaword', dictionary=dictionary)

    def test_guess_timeout_deducts_life(self):
        game = Hangman(answer="apple", lives=2)

        start_time = time.time()
        time.sleep(0.1)  
        # Set timeout to 0.05 seconds to ensure life is deducted
        game.check_timeout(start_time, timeout=0.05)
        self.assertEqual(game.lives, 1)  
            
        # Trigger timeout again
        game.check_timeout(start_time, timeout=0.05)
        self.assertEqual(game.lives, 0)
        self.assertTrue(game.is_lost())

class TestHangmanGUI(unittest.TestCase):
    def test_gui_launch(self):
        try:
            from hangman import HangmanGUI
        except ImportError:
            self.fail("HangmanGUI class does not exist in hangman.py")

        root = tk.Tk()
        try:
            app = HangmanGUI(root)
            self.assertIsNotNone(app)  
        finally:
            root.destroy() 

if __name__ == "__main__":
    unittest.main()

    



