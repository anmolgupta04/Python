def is_palindrome_simple(text):
    """
    Check if a string is a palindrome (simple version).
    Case-sensitive and considers spaces/punctuation.
    
    Args:
        text (str): The string to check
        
    Returns:
        bool: True if palindrome, False otherwise
    """
    return text == text[::-1]


def is_palindrome(text):
    """
    Check if a string is a palindrome.
    Case-insensitive and ignores spaces/punctuation.
    
    Args:
        text (str): The string to check
        
    Returns:
        bool: True if palindrome, False otherwise
    """
    # Remove spaces and convert to lowercase
    cleaned = ''.join(char.lower() for char in text if char.isalnum())
    
    # Check if cleaned string equals its reverse
    return cleaned == cleaned[::-1]


def is_palindrome_detailed(text):
    """
    Check if a string is a palindrome with detailed feedback.
    
    Args:
        text (str): The string to check
        
    Returns:
        tuple: (is_palindrome: bool, cleaned_text: str, message: str)
    """
    if not text:
        return False, "", "Empty string is not considered a palindrome"
    
    # Clean the text
    cleaned = ''.join(char.lower() for char in text if char.isalnum())
    
    if not cleaned:
        return False, "", "No alphanumeric characters found"
    
    # Check if palindrome
    is_palin = cleaned == cleaned[::-1]
    
    if is_palin:
        message = f"✓ '{text}' is a palindrome!"
        if text.lower() != cleaned:
            message += f" (cleaned: '{cleaned}')"
    else:
        reversed_text = cleaned[::-1]
        message = f"✗ '{text}' is not a palindrome"
        if text.lower() != cleaned:
            message += f" (cleaned: '{cleaned}' vs reversed: '{reversed_text}')"
    
    return is_palin, cleaned, message


def main():
    """
    Main function to demonstrate palindrome checking.
    """
    print("=" * 70)
    print("                    PALINDROME CHECKER")
    print("=" * 70)
    print()
    print("A palindrome reads the same forward and backward.")
    print("Examples: 'madam', 'racecar', 'A man a plan a canal Panama'")
    print()
    print("=" * 70)
    print()
    
    # Test cases
    test_words = [
        # Simple palindromes
        "madam",
        "racecar",
        "level",
        "radar",
        "civic",
        
        # Not palindromes
        "hello",
        "python",
        "programming",
        
        # Palindromes with mixed case
        "Madam",
        "RaceCar",
        
        # Phrase palindromes (with spaces)
        "A man a plan a canal Panama",
        "Was it a car or a cat I saw",
        "Never odd or even",
        
        # Palindromes with punctuation
        "A Santa at NASA",
        "Do geese see God?",
        
        # Single character
        "a",
        
        # Numbers
        "12321",
        "12345",
    ]
    
    print("Testing various strings:")
    print("-" * 70)
    
    for text in test_words:
        is_palin = is_palindrome(text)
        status = "✓ PALINDROME    " if is_palin else "✗ NOT PALINDROME"
        print(f"{status} | {text}")
    
    print()
    print("=" * 70)
    print()
    
    # Interactive mode
    print("Interactive Palindrome Checker")
    print("-" * 70)
    print("Enter text to check if it's a palindrome.")
    print("The checker ignores spaces, punctuation, and case.")
    print()
    
    while True:
        try:
            text = input("Enter a word or phrase (or 'quit' to exit): ").strip()
            
            if text.lower() in ['quit', 'exit', 'q']:
                print("\nThank you for using the Palindrome Checker!")
                break
            
            if not text:
                print("Please enter some text.\n")
                continue
            
            is_palin, cleaned, message = is_palindrome_detailed(text)
            print(f"\n{message}\n")
            
        except KeyboardInterrupt:
            print("\n\nProgram terminated by user.")
            break


# Additional helper function for comparison
def compare_methods(text):
    """
    Compare simple vs advanced palindrome checking.
    """
    simple_result = is_palindrome_simple(text)
    advanced_result = is_palindrome(text)
    
    print(f"Text: '{text}'")
    print(f"  Simple method (exact match): {simple_result}")
    print(f"  Advanced method (ignore case/spaces): {advanced_result}")
    print()


if __name__ == "__main__":
    # Show comparison for educational purposes
    print("=" * 70)
    print("COMPARISON: Simple vs Advanced Palindrome Checking")
    print("=" * 70)
    print()
    
    comparison_tests = [
        "madam",
        "Madam",
        "A man a plan a canal Panama",
    ]
    
    for test in comparison_tests:
        compare_methods(test)
    
    print("=" * 70)
    print()
    
    # Run main program
    main()