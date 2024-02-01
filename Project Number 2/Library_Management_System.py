# Author: UMERJAMSHIAD
# Roll Number: ?
# Email: Umerjamshaid481@gmail.com

"""
Creating a Number Guessing Game in Python.
"""

# Import the 'random' module to generate random numbers
# Like an library.
import random

# Function to start the Number Guessing Game
def start_game():
    """
    code to start the Game.
    """

 # Display a welcome message to the user
    print("Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100. guess it?")


# Generate a random number between 1 and 100 and store it in 'secret_number'
    secret_number = random.randint(1, 100)
    
    # Initialize the 'attempts' variable to count the number of guesses
    attempts = 0

# Start an infinite loop for the game
    while True:
    # Ask the user to input their guess and convert it to an integer
        guess = int(input("Enter your guess: "))
         # Increment the 'attempts' variable
        attempts += 1

        # Check if the guess is correct
        if guess == secret_number:
            print(f"Congratulations! You guessed the correct number {secret_number} in {attempts} attempts.")
            break

        # Check if the guess is too low
        elif guess < secret_number:
            print("Too low. Try again.")

         # If neither of the above conditions is true, the guess is too high
        else:
            print("Too high. Try again.")

if __name__ == "__main__":
    # Call the start_game function when the script is executed (not imported as a module)
    start_game()
