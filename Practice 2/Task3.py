import re
import string

def check_password_strength(password):
    """
    Evaluates the strength of a password based on multiple criteria.
    
    Args:
        password (str): The password to evaluate
    
    Returns:
        dict: A dictionary containing strength score, level, and detailed feedback
    """
    
    # Initialize score and feedback
    score = 0
    feedback = []
    criteria_met = {
        'length': False,
        'uppercase': False,
        'lowercase': False,
        'digits': False,
        'special': False
    }
    
    # Check password length
    length = len(password)
    if length >= 12:
        score += 30
        criteria_met['length'] = True
        feedback.append("✓ Excellent length (12+ characters)")
    elif length >= 8:
        score += 20
        criteria_met['length'] = True
        feedback.append("✓ Good length (8-11 characters)")
    elif length >= 6:
        score += 10
        feedback.append("⚠ Minimum length met (6-7 characters), but consider making it longer")
    else:
        feedback.append("✗ Too short (less than 6 characters) - should be at least 8 characters")
    
    # Check for uppercase letters
    if re.search(r'[A-Z]', password):
        score += 15
        criteria_met['uppercase'] = True
        feedback.append("✓ Contains uppercase letters")
    else:
        feedback.append("✗ Missing uppercase letters")
    
    # Check for lowercase letters
    if re.search(r'[a-z]', password):
        score += 15
        criteria_met['lowercase'] = True
        feedback.append("✓ Contains lowercase letters")
    else:
        feedback.append("✗ Missing lowercase letters")
    
    # Check for digits
    if re.search(r'\d', password):
        score += 15
        criteria_met['digits'] = True
        feedback.append("✓ Contains digits")
    else:
        feedback.append("✗ Missing digits")
    
    # Check for special characters
    special_chars = string.punctuation
    if re.search(f'[{re.escape(special_chars)}]', password):
        score += 15
        criteria_met['special'] = True
        feedback.append("✓ Contains special characters")
    else:
        feedback.append("✗ Missing special characters (!@#$%^&*, etc.)")
    
    # Bonus points for variety
    unique_chars = len(set(password))
    if unique_chars >= length * 0.7:
        score += 10
        feedback.append("✓ Good character variety")
    
    # Penalty for common patterns
    common_patterns = [
        (r'(.)\1{2,}', "⚠ Contains repeating characters"),
        (r'(012|123|234|345|456|567|678|789|890)', "⚠ Contains sequential numbers"),
        (r'(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)', "⚠ Contains sequential letters"),
        (r'(password|pass|pwd|admin|user|login|welcome|qwerty|12345|letmein)', "⚠ Contains common words")
    ]
    
    for pattern, warning in common_patterns:
        if re.search(pattern, password.lower()):
            score -= 10
            feedback.append(warning)
    
    # Ensure score is within bounds
    score = max(0, min(100, score))
    
    # Determine strength level
    if score >= 80:
        strength = "STRONG"
        color = "🟢"
    elif score >= 60:
        strength = "MODERATE"
        color = "🟡"
    elif score >= 40:
        strength = "WEAK"
        color = "🟠"
    else:
        strength = "VERY WEAK"
        color = "🔴"
    
    return {
        'score': score,
        'strength': strength,
        'color': color,
        'criteria_met': criteria_met,
        'feedback': feedback
    }


def display_password_strength(result):
    """
    Display the password strength results in a formatted way.
    
    Args:
        result (dict): The result dictionary from check_password_strength
    """
    print("\n" + "="*60)
    print("PASSWORD STRENGTH ANALYSIS")
    print("="*60)
    
    # Display strength meter
    print(f"\nStrength: {result['color']} {result['strength']}")
    print(f"Score: {result['score']}/100")
    
    # Visual strength bar
    bar_length = 50
    filled = int((result['score'] / 100) * bar_length)
    bar = "█" * filled + "░" * (bar_length - filled)
    print(f"[{bar}]")
    
    # Display criteria summary
    print("\n" + "-"*60)
    print("CRITERIA CHECKLIST:")
    print("-"*60)
    criteria_labels = {
        'length': 'Sufficient Length',
        'uppercase': 'Uppercase Letters',
        'lowercase': 'Lowercase Letters',
        'digits': 'Numbers',
        'special': 'Special Characters'
    }
    
    for key, label in criteria_labels.items():
        status = "✓" if result['criteria_met'][key] else "✗"
        print(f"{status} {label}")
    
    # Display detailed feedback
    print("\n" + "-"*60)
    print("DETAILED FEEDBACK:")
    print("-"*60)
    for item in result['feedback']:
        print(f"  {item}")
    
    # Recommendations
    print("\n" + "-"*60)
    print("RECOMMENDATIONS:")
    print("-"*60)
    if result['score'] < 80:
        print("  • Use at least 12 characters for better security")
        print("  • Include a mix of uppercase, lowercase, numbers, and symbols")
        print("  • Avoid common words, patterns, and personal information")
        print("  • Consider using a passphrase (e.g., 'Coffee@Sunrise#2024!')")
        print("  • Use a unique password for each account")
    else:
        print("  • Your password is strong! Keep it secure.")
        print("  • Don't share it with anyone")
        print("  • Change it periodically")
        print("  • Enable two-factor authentication when possible")
    
    print("="*60 + "\n")


def generate_password_suggestion():
    """
    Generate a strong password suggestion.
    
    Returns:
        str: A randomly generated strong password
    """
    import random
    
    # Character sets
    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase
    digits = string.digits
    special = "!@#$%^&*"
    
    # Ensure at least one from each category
    password_chars = [
        random.choice(uppercase),
        random.choice(uppercase),
        random.choice(lowercase),
        random.choice(lowercase),
        random.choice(digits),
        random.choice(digits),
        random.choice(special),
        random.choice(special)
    ]
    
    # Fill the rest randomly
    all_chars = uppercase + lowercase + digits + special
    password_chars += [random.choice(all_chars) for _ in range(6)]
    
    # Shuffle the characters
    random.shuffle(password_chars)
    
    return ''.join(password_chars)


def main():
    """
    Main function to run the password strength checker.
    """
    print("\n" + "="*60)
    print("🔒 PASSWORD STRENGTH CHECKER 🔒")
    print("="*60)
    print("\nThis tool will evaluate your password strength based on:")
    print("  • Length (8+ characters recommended)")
    print("  • Uppercase and lowercase letters")
    print("  • Numbers")
    print("  • Special characters (!@#$%^&*, etc.)")
    print("  • Character variety")
    print("  • Absence of common patterns")
    
    while True:
        print("\n" + "-"*60)
        choice = input("\nOptions:\n  1. Check a password\n  2. Generate a strong password\n  3. Exit\n\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            # Check password
            password = input("\nEnter password to check (input is hidden): ")
            
            if not password:
                print("⚠ Password cannot be empty!")
                continue
            
            result = check_password_strength(password)
            display_password_strength(result)
            
        elif choice == '2':
            # Generate password
            suggested_password = generate_password_suggestion()
            print(f"\n🔑 Suggested strong password: {suggested_password}")
            print("\nLet's check its strength:")
            result = check_password_strength(suggested_password)
            display_password_strength(result)
            
        elif choice == '3':
            print("\n👋 Thank you for using Password Strength Checker!\n")
            break
        else:
            print("❌ Invalid choice! Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()