art = ''' _____________________
|  _________________  |
| | JO           0. | |
| |_________________| |
|  ___ ___ ___   ___  |
| | 7 | 8 | 9 | | + | |
| |___|___|___| |___| |
| | 4 | 5 | 6 | | - | |
| |___|___|___| |___| |
| | 1 | 2 | 3 | | x | |
| |___|___|___| |___| |
| | . | 0 | = | | / | |
| |___|___|___| |___| |
|_____________________|'''

def add(n1, n2):
    return n1 + n2

def sub(n1, n2):
    return n1 - n2

def mul(n1, n2):
    return n1 * n2

def div(n1, n2):
    return n1 / n2

operations = {
    '+': add,
    '-': sub,
    '*': mul,
    '/': div
}

def calculator():
    print(art)
    should_accumulate = True
    first_number = float(input("Enter first number: "))
    
    while should_accumulate:
        for symbol in operations:
            print(symbol)
        operation_symbol = input("Choose an operation: ")
        
        second_number = float(input("Enter second number: "))
        
        answer = operations[operation_symbol](first_number, second_number)
        print(f"Result: {first_number} {operation_symbol} {second_number} = {answer}")
        
        choice = input(f"Type 'y' to continue with {answer}, or 'n' to start a new calculation: ").lower()
        
        if choice == 'y':
            first_number = answer
        else:
            should_accumulate = False
            print("\n" * 20)
            calculator()

calculator()

