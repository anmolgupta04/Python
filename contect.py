"""
Contact Book Application
A command-line program to manage contacts stored in a text file.
Features: Add, View, Search contacts
"""

def display_menu():
    """Display the main menu options"""
    print("\n" + "="*40)
    print("    CONTACT BOOK APPLICATION")
    print("="*40)
    print("1. Add New Contact")
    print("2. View All Contacts")
    print("3. Search Contact")
    print("4. Exit")
    print("="*40)


def add_contact():
    """Add a new contact to the contact book"""
    print("\n--- Add New Contact ---")
    
    # Get contact details from user
    name = input("Enter Name: ").strip()
    if not name:
        print("Error: Name cannot be empty!")
        return
    
    phone = input("Enter Phone Number: ").strip()
    email = input("Enter Email: ").strip()
    address = input("Enter Address: ").strip()
    
    # Format: name|phone|email|address
    contact_data = f"{name}|{phone}|{email}|{address}\n"
    
    # Write to file (append mode)
    try:
        with open("contacts.txt", "a") as file:
            file.write(contact_data)
        print(f"\n✓ Contact '{name}' added successfully!")
    except Exception as e:
        print(f"Error saving contact: {e}")


def view_all_contacts():
    """Display all contacts from the file"""
    print("\n--- All Contacts ---")
    
    try:
        with open("contacts.txt", "r") as file:
            contacts = file.readlines()
        
        if not contacts:
            print("No contacts found. The contact book is empty.")
            return
        
        # Display header
        print(f"\n{'Name':<20} {'Phone':<15} {'Email':<25} {'Address':<30}")
        print("-" * 90)
        
        # Display each contact
        for i, contact in enumerate(contacts, 1):
            # Remove newline and split by |
            parts = contact.strip().split("|")
            if len(parts) == 4:
                name, phone, email, address = parts
                print(f"{name:<20} {phone:<15} {email:<25} {address:<30}")
        
        print(f"\nTotal contacts: {len(contacts)}")
        
    except FileNotFoundError:
        print("No contacts found. The contact book is empty.")
    except Exception as e:
        print(f"Error reading contacts: {e}")


def search_contact():
    """Search for a contact by name"""
    print("\n--- Search Contact ---")
    
    search_term = input("Enter name to search: ").strip().lower()
    
    if not search_term:
        print("Error: Search term cannot be empty!")
        return
    
    try:
        with open("contacts.txt", "r") as file:
            contacts = file.readlines()
        
        # Find matching contacts
        found_contacts = []
        for contact in contacts:
            parts = contact.strip().split("|")
            if len(parts) == 4:
                name = parts[0]
                # Case-insensitive search
                if search_term in name.lower():
                    found_contacts.append(parts)
        
        # Display results
        if found_contacts:
            print(f"\nFound {len(found_contacts)} contact(s):")
            print(f"\n{'Name':<20} {'Phone':<15} {'Email':<25} {'Address':<30}")
            print("-" * 90)
            
            for name, phone, email, address in found_contacts:
                print(f"{name:<20} {phone:<15} {email:<25} {address:<30}")
        else:
            print(f"\nNo contacts found matching '{search_term}'")
    
    except FileNotFoundError:
        print("No contacts found. The contact book is empty.")
    except Exception as e:
        print(f"Error searching contacts: {e}")


def main():
    """Main program loop"""
    print("\nWelcome to Contact Book!")
    
    while True:
        display_menu()
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            add_contact()
        elif choice == "2":
            view_all_contacts()
        elif choice == "3":
            search_contact()
        elif choice == "4":
            print("\nThank you for using Contact Book. Goodbye!")
            break
        else:
            print("\n✗ Invalid choice! Please enter a number between 1 and 4.")
        
        # Pause before showing menu again
        input("\nPress Enter to continue...")


# Run the program
if __name__ == "__main__":
    main()