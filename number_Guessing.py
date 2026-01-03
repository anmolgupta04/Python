print('''

      ''')


from random import randint

EASY_LEVEL_TURNS = 10
HARD_LEVEL_TURNS = 5

turns = 0

def check_answer(user_guess, actual_answer, turns):
    if user_guess > actual_answer:
        print("too high.")
        return turns - 1
    elif user_guess < actual_answer:
        print("too low.")
        return turns - 1
    else:
        print("you got it! The answer was {actual_answer}")


def set_difficulty():
    level = input("Choose a difficulty . Type 'easy' or 'hard' :")
    if level == "easy":
        return  EASY_LEVEL_TURNS
    else:
        return  HARD_LEVEL_TURNS


def game():
    print("Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 to 100.")
    answer = randint(1, 100)
    print(f"Pssst , the correct answer is {answer}")

    turns = set_difficulty()
    

    guess = 0
    while guess != answer:
        print(f"You have {turns} attempts remaining to guess the number.")
        guess = int(input("make a guess:"))
        turns = check_answer(guess, answer, turns)
        if turns  == 0 :
            print("you've run out of guesses, you lose.")
            return
        elif guess != answer: 
            print("Guess Again")

    # turns = 0
    # print(f"you have{turns} attemps remaining to guess the number:")

game()
