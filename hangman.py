import random

# ASCII art for hangman stages
hangman_stages = [
    # Stage 0 - No mistakes
    """
       ------
       |    |
       |
       |
       |
       |
    -------
    """,
    # Stage 1 - Head
    """
       ------
       |    |
       |    O
       |
       |
       |
    -------
    """,
    # Stage 2 - Body
    """
       ------
       |    |
       |    O
       |    |
       |
       |
    -------
    """,
    # Stage 3 - Left arm
    """
       ------
       |    |
       |    O
       |   /|
       |
       |
    -------
    """,
    # Stage 4 - Right arm
    """
       ------
       |    |
       |    O
       |   /|\\
       |
       |
    -------
    """,
    # Stage 5 - Left leg
    """
       ------
       |    |
       |    O
       |   /|\\
       |   /
       |
    -------
    """,
    # Stage 6 - Right leg (Game Over)
    """
       ------
       |    |
       |    O
       |   /|\\
       |   / \\
       |
    -------
    """
]

# List of words to choose from
words = ['boruta', 'hinata', 'hori', 'natsu', 'naruto']

# Choose a random word
word = random.choice(words)

# Create a list to track guessed letters
guessed_letters = []

# Number of tries allowed
tries = 6

# Game loop
print("Welcome to Hangman!")
print(hangman_stages[0])
print("_ " * len(word))

while tries > 0:
    # Calculate mistakes and show hangman
    mistakes = 6 - tries
    print(hangman_stages[mistakes])

    # Show current progress
    display = ""
    for letter in word:
        if letter in guessed_letters:
            display += letter + " "
        else:
            display += "_ "

    print(display)
    print(f"Tries remaining: {tries}")
    print(f"Guessed letters: {', '.join(guessed_letters)}")

    # Check if player won
    if "_" not in display:
        print(f"\nCongratulations! You won! The word was '{word}'")
        break

    # Get player's guess
    guess = input("\nGuess a letter: ").lower()

    # Validate input
    if len(guess) != 1 or not guess.isalpha():
        print("Please enter a single letter.")
        continue

    # Check if already guessed
    if guess in guessed_letters:
        print("You already guessed that letter!")
        continue

    # Add to guessed letters
    guessed_letters.append(guess)

    # Check if guess is in the word
    if guess in word:
        print(f"Good job! '{guess}' is in the word!")
    else:
        print(f"Sorry, '{guess}' is not in the word.")
        tries -= 1

# Check if player lost
if tries == 0:
    print(hangman_stages[6])
    print(f"\nGame Over! The word was '{word}'")


