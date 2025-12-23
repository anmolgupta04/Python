import random


def guessing_game():
    """
    Simple number guessing game.
    The computer generates a random number between 1 and 100,
    and the user tries to guess it with hints.
    """
    # Generate random number between 1 and 100
    secret_number = random.randint(1, 100)
    attempts = 0
    
    print("=" * 50)
    print("        NUMBER GUESSING GAME")
    print("=" * 50)
    print()
    print("I'm thinking of a number between 1 and 100.")
    print("Try to guess it!")
    print()
    
    while True:
        try:
            # Get user's guess
            guess_input = input("Enter your guess: ").strip()
            
            # Convert to integer
            try:
                guess = int(guess_input)
            except ValueError:
                print("Please enter a valid number!")
                continue
            
            # Check if guess is in valid range
            if guess < 1 or guess > 100:
                print("Please enter a number between 1 and 100!")
                continue
            
            # Increment attempts
            attempts += 1
            
            # Check the guess and provide feedback
            if guess < secret_number:
                print("Too low! Try again.")
                print()
            elif guess > secret_number:
                print("Too high! Try again.")
                print()
            else:
                # Correct guess!
                print()
                print("=" * 50)
                print("🎉 Congratulations! You guessed it!")
                print(f"The number was {secret_number}.")
                print(f"You got it in {attempts} attempts!")
                print("=" * 50)
                break
        
        except KeyboardInterrupt:
            print(f"\n\nGame ended. The number was {secret_number}.")
            break


if __name__ == "__main__":
    guessing_game()
    
    # Ask if player wants to play again
    while True:
        print()
        play_again = input("Do you want to play again? (yes/no): ").strip().lower()
        
        if play_again in ['yes', 'y']:
            print()
            guessing_game()
        elif play_again in ['no', 'n']:
            print("\nThanks for playing! Goodbye!")
            break
        else:
            print("Please enter 'yes' or 'no'.")