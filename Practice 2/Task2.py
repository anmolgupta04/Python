import random

def number_guesser():
    """
    A number guessing game where the user tries to guess a randomly generated number.
    The program provides feedback if the guess is too high or too low.
    """
    
    # Define the range for the random number
    min_number = 1
    max_number = 100
    
    # Generate a random number
    secret_number = random.randint(min_number, max_number)
    
    # Initialize attempt counter
    attempts = 0
    
    # Welcome message
    print("\n" + "="*50)
    print("🎯 Welcome to the Number Guessing Game! 🎯")
    print("="*50)
    print(f"\nI'm thinking of a number between {min_number} and {max_number}.")
    print("Try to guess it!\n")
    
    # Game loop
    while True:
        try:
            # Get user input
            guess = int(input("Enter your guess: "))
            
            # Validate input range
            if guess < min_number or guess > max_number:
                print(f"⚠️  Please enter a number between {min_number} and {max_number}!")
                continue
            
            # Increment attempts
            attempts += 1
            
            # Check the guess
            if guess < secret_number:
                print("📈 Too low! Try a higher number.\n")
            elif guess > secret_number:
                print("📉 Too high! Try a lower number.\n")
            else:
                # Correct guess
                print("\n" + "="*50)
                print("🎉 Congratulations! You guessed it! 🎉")
                print("="*50)
                print(f"The secret number was: {secret_number}")
                print(f"You guessed it in {attempts} {'attempt' if attempts == 1 else 'attempts'}!")
                print("="*50 + "\n")
                break
                
        except ValueError:
            print("❌ Invalid input! Please enter a valid number.\n")
        except KeyboardInterrupt:
            print("\n\n👋 Game interrupted. Thanks for playing!")
            break

def play_again():
    """Ask if the user wants to play again."""
    while True:
        choice = input("Would you like to play again? (yes/no): ").lower().strip()
        if choice in ['yes', 'y']:
            return True
        elif choice in ['no', 'n']:
            return False
        else:
            print("Please enter 'yes' or 'no'.")

def main():
    """Main function to run the game with replay option."""
    while True:
        number_guesser()
        
        if not play_again():
            print("\n👋 Thanks for playing! Goodbye!\n")
            break

if __name__ == "__main__":
    main()