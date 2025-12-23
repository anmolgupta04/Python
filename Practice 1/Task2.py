def celsius_to_fahrenheit(celsius):
    """
    Converts Celsius to Fahrenheit.
    
    Args:
        celsius (float): Temperature in Celsius
        
    Returns:
        float: Temperature in Fahrenheit
    """
    return (celsius * 9/5) + 32


def fahrenheit_to_celsius(fahrenheit):
    """
    Converts Fahrenheit to Celsius.
    
    Args:
        fahrenheit (float): Temperature in Fahrenheit
        
    Returns:
        float: Temperature in Celsius
    """
    return (fahrenheit - 32) * 5/9


def main():
    """
    Main function to handle user input and temperature conversion.
    """
    print("=" * 50)
    print("     TEMPERATURE CONVERSION PROGRAM")
    print("=" * 50)
    print()
    
    while True:
        try:
            # Get temperature value from user
            temp_value = float(input("Enter the temperature value: "))
            
            # Get unit of measurement
            print("\nSelect the unit of measurement:")
            print("1. Celsius (C)")
            print("2. Fahrenheit (F)")
            unit = input("Enter your choice (1 or 2): ").strip()
            
            print()
            
            # Perform conversion based on user's choice
            if unit == '1' or unit.upper() == 'C':
                converted_temp = celsius_to_fahrenheit(temp_value)
                print(f"{temp_value}°C = {converted_temp:.2f}°F")
            elif unit == '2' or unit.upper() == 'F':
                converted_temp = fahrenheit_to_celsius(temp_value)
                print(f"{temp_value}°F = {converted_temp:.2f}°C")
            else:
                print("Invalid choice! Please select 1 or 2.")
                continue
            
            # Ask if user wants to convert another temperature
            print()
            another = input("Do you want to convert another temperature? (y/n): ").strip().lower()
            if another != 'y' and another != 'yes':
                print("\nThank you for using the Temperature Conversion Program!")
                break
            print()
            
        except ValueError:
            print("Error: Please enter a valid numeric value for temperature.")
            print()
        except KeyboardInterrupt:
            print("\n\nProgram terminated by user.")
            break


if __name__ == "__main__":
    main()