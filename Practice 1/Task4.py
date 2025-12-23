def add(a, b):
    """Add two numbers."""
    return a + b


def subtract(a, b):
    """Subtract second number from first."""
    return a - b


def multiply(a, b):
    """Multiply two numbers."""
    return a * b


def divide(a, b):
    """Divide first number by second."""
    if b == 0:
        return None, "Error: Division by zero is not allowed"
    return a / b, None


def modulus(a, b):
    """Calculate modulus (remainder) of first number divided by second."""
    if b == 0:
        return None, "Error: Modulus by zero is not allowed"
    return a % b, None


def calculate(num1, num2, operator):
    """
    Perform calculation based on operator.
    
    Args:
        num1 (float): First number
        num2 (float): Second number
        operator (str): Operation to perform (+, -, *, /, %)
        
    Returns:
        tuple: (result, error_message)
    """
    if operator == '+':
        return add(num1, num2), None
    elif operator == '-':
        return subtract(num1, num2), None
    elif operator == '*':
        return multiply(num1, num2), None
    elif operator == '/':
        return divide(num1, num2)
    elif operator == '%':
        return modulus(num1, num2)
    else:
        return None, f"Error: Invalid operator '{operator}'"


def main():
    """
    Main function to run the calculator program.
    """
    print("=" * 60)
    print("              BASIC CALCULATOR")
    print("=" * 60)
    print()
    print("Available operations:")
    print("  +  : Addition")
    print("  -  : Subtraction")
    print("  *  : Multiplication")
    print("  /  : Division")
    print("  %  : Modulus (remainder)")
    print()
    print("=" * 60)
    
    while True:
        try:
            print()
            # Get first number
            num1_input = input("Enter the first number (or 'quit' to exit): ").strip()
            
            if num1_input.lower() in ['quit', 'exit', 'q']:
                print("\nThank you for using the calculator!")
                break
            
            try:
                num1 = float(num1_input)
            except ValueError:
                print("Error: Please enter a valid number.")
                continue
            
            # Get operator
            operator = input("Enter an operator (+, -, *, /, %): ").strip()
            
            if operator not in ['+', '-', '*', '/', '%']:
                print(f"Error: Invalid operator '{operator}'. Please use +, -, *, /, or %.")
                continue
            
            # Get second number
            num2_input = input("Enter the second number: ").strip()
            
            try:
                num2 = float(num2_input)
            except ValueError:
                print("Error: Please enter a valid number.")
                continue
            
            # Perform calculation
            result, error = calculate(num1, num2, operator)
            
            if error:
                print(f"\n{error}")
            else:
                # Format the result nicely
                print()
                print("-" * 60)
                
                # Display integers without decimal point
                if isinstance(result, float) and result.is_integer():
                    print(f"Result: {num1} {operator} {num2} = {int(result)}")
                else:
                    print(f"Result: {num1} {operator} {num2} = {result}")
                
                print("-" * 60)
            
            # Ask if user wants to perform another calculation
            print()
            another = input("Do you want to perform another calculation? (y/n): ").strip().lower()
            if another not in ['y', 'yes']:
                print("\nThank you for using the calculator!")
                break
                
        except KeyboardInterrupt:
            print("\n\nProgram terminated by user.")
            break
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")


if __name__ == "__main__":
    main()