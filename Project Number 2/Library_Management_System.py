# Author: UMERJAMSHIAD
# Roll Number: ?
# Email: Umerjamshaid481@gmail.com

"""
Creating a Number Guessing Game in Python.
"""

import random

def start_game():
    """
    code to start the Game.
    """
    print("Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100. guess it?")
    
    secret_number = random.randint(1, 100)
    attempts = 0

    while True:
        guess = int(input("Enter your guess: "))
        attempts += 1

        if guess == secret_number:
            print(f"Congratulations! You guessed the correct number {secret_number} in {attempts} attempts.")
            break
        elif guess < secret_number:
            print("Too low. Try again.")
        else:
            print("Too high. Try again.")

if __name__ == "__main__":
    # Call the start_game function when the script is executed
    start_game()
