def reverse_string(text):
    """
    Reverses the input string.
    
    Args:
        text (str): The string to be reversed
        
    Returns:
        str: The reversed string
    """
    return text[::-1]


# Example usage
if __name__ == "__main__":
    # Test cases
    test_strings = [
        "hello",
        "Python",
        "12345",
        "A man a plan a canal Panama",
        ""
    ]
    
    print("String Reversal Examples:")
    print("-" * 40)
    
    for string in test_strings:
        reversed_string = reverse_string(string)
        print(f"Input:  '{string}'")
        print(f"Output: '{reversed_string}'")
        print()