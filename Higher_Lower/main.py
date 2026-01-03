from art import logo, vs
from game_data import data
import random


def format_data(account):
    """Return a formatted string for an account dict."""
    account_name = account["name"]
    account_descr = account["description"]
    account_country = account["country"]
    return f"{account_name}, a {account_descr}, from {account_country}"


def check_answer(user_guess, a_followers, b_followers):
    """Return True if user_guess is correct, otherwise False."""
    if a_followers > b_followers:
        return user_guess == 'a'
    else:
        return user_guess == 'b'


print(logo)
score = 0
game_should_continue = True

# Start with a random account B
account_b = random.choice(data)

while game_should_continue:
    # A becomes previous B
    account_a = account_b
    # Generate new B until it is different from A
    account_b = random.choice(data)
    while account_a == account_b:
        account_b = random.choice(data)

    print(f"Compare A: {format_data(account_a)}")
    print(vs)
    print(f"Compare B: {format_data(account_b)}")

    guess = input("Who has more followers? Type 'A' or 'B': ").lower()

    a_follower_count = account_a["follower_count"]
    b_follower_count = account_b["follower_count"]

    is_correct = check_answer(guess, a_follower_count, b_follower_count)

    print("\n" * 20)
    print(logo)

    if is_correct:
        score += 1
        print(f"You're right! Current score: {score}.")
    else:
        game_should_continue = False
        print(f"Sorry, that's wrong. Final score: {score}.")
