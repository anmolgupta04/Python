def fibonacci(n):
    """
    Generate Fibonacci sequence up to n terms.
    
    Args:
        n (int): Number of terms to generate
    
    Returns:
        list: Fibonacci sequence
    """
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    
    sequence = [0, 1]
    
    for i in range(2, n):
        next_term = sequence[i-1] + sequence[i-2]
        sequence.append(next_term)
    
    return sequence


# Main program
print("Fibonacci Sequence Generator")
print("-" * 30)

try:
    n = int(input("Enter the number of terms: "))
    
    if n <= 0:
        print("Please enter a positive number!")
    else:
        result = fibonacci(n)
        
        print(f"\nFibonacci sequence ({n} terms):")
        print(result)
        
        # Display in a formatted way
        print("\nFormatted output:")
        for i, num in enumerate(result):
            print(f"Term {i+1}: {num}")

except ValueError:
    print("Invalid input! Please enter a number.")