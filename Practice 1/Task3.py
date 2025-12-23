import re


def validate_email(email):
    """
    Validates whether a given string is a valid email address.
    
    Checks include:
    - Presence of exactly one "@" symbol
    - Valid characters in local part (before @)
    - Valid domain name structure
    - Proper domain extension
    
    Args:
        email (str): The email address to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    # Check if email is a string and not empty
    if not isinstance(email, str) or not email:
        return False
    
    # Basic check: must contain exactly one @ symbol
    if email.count('@') != 1:
        return False
    
    # Split email into local part and domain
    local_part, domain = email.split('@')
    
    # Check if both parts exist
    if not local_part or not domain:
        return False
    
    # Validate local part (before @)
    # - Must start with alphanumeric character
    # - Can contain letters, numbers, dots, hyphens, underscores
    # - Cannot start or end with a dot
    # - Cannot have consecutive dots
    if local_part[0] == '.' or local_part[-1] == '.':
        return False
    
    if '..' in local_part:
        return False
    
    # Check for valid characters in local part
    local_pattern = r'^[a-zA-Z0-9._-]+$'
    if not re.match(local_pattern, local_part):
        return False
    
    # Validate domain part
    # - Must contain at least one dot
    # - Must have valid domain name and extension
    if '.' not in domain:
        return False
    
    # Split domain into parts
    domain_parts = domain.split('.')
    
    # Check if domain has at least 2 parts (name and extension)
    if len(domain_parts) < 2:
        return False
    
    # Check each domain part
    for part in domain_parts:
        if not part:  # Empty part (consecutive dots)
            return False
        
        # Domain parts should contain only alphanumeric and hyphens
        # Cannot start or end with hyphen
        if part[0] == '-' or part[-1] == '-':
            return False
        
        if not re.match(r'^[a-zA-Z0-9-]+$', part):
            return False
    
    # Check that top-level domain (last part) is at least 2 characters
    if len(domain_parts[-1]) < 2:
        return False
    
    return True


def validate_email_detailed(email):
    """
    Validates email and provides detailed feedback.
    
    Args:
        email (str): The email address to validate
        
    Returns:
        tuple: (is_valid: bool, message: str)
    """
    if not isinstance(email, str) or not email:
        return False, "Email must be a non-empty string"
    
    if email.count('@') == 0:
        return False, "Email must contain an '@' symbol"
    
    if email.count('@') > 1:
        return False, "Email must contain exactly one '@' symbol"
    
    local_part, domain = email.split('@')
    
    if not local_part:
        return False, "Local part (before @) cannot be empty"
    
    if not domain:
        return False, "Domain part (after @) cannot be empty"
    
    if local_part[0] == '.' or local_part[-1] == '.':
        return False, "Local part cannot start or end with a dot"
    
    if '..' in local_part:
        return False, "Local part cannot contain consecutive dots"
    
    local_pattern = r'^[a-zA-Z0-9._-]+$'
    if not re.match(local_pattern, local_part):
        return False, "Local part contains invalid characters (only letters, numbers, dots, hyphens, and underscores allowed)"
    
    if '.' not in domain:
        return False, "Domain must contain at least one dot"
    
    domain_parts = domain.split('.')
    
    if len(domain_parts) < 2:
        return False, "Domain must have at least a name and extension"
    
    for i, part in enumerate(domain_parts):
        if not part:
            return False, "Domain cannot contain consecutive dots or empty parts"
        
        if part[0] == '-' or part[-1] == '-':
            return False, f"Domain part '{part}' cannot start or end with a hyphen"
        
        if not re.match(r'^[a-zA-Z0-9-]+$', part):
            return False, f"Domain part '{part}' contains invalid characters"
    
    if len(domain_parts[-1]) < 2:
        return False, "Top-level domain must be at least 2 characters"
    
    return True, "Valid email address"


def main():
    """
    Main function to demonstrate email validation.
    """
    print("=" * 60)
    print("           EMAIL VALIDATOR")
    print("=" * 60)
    print()
    
    # Test cases
    test_emails = [
        "user@example.com",           # Valid
        "john.doe@company.co.uk",     # Valid
        "test_email@domain.org",      # Valid
        "user123@test-domain.com",    # Valid
        "invalid.email",              # Invalid - no @
        "@example.com",               # Invalid - no local part
        "user@",                      # Invalid - no domain
        "user@@example.com",          # Invalid - multiple @
        "user@domain",                # Invalid - no domain extension
        ".user@example.com",          # Invalid - starts with dot
        "user.@example.com",          # Invalid - ends with dot
        "user..name@example.com",     # Invalid - consecutive dots
        "user@domain..com",           # Invalid - consecutive dots in domain
        "user name@example.com",      # Invalid - space in local part
        "user@-example.com",          # Invalid - domain starts with hyphen
        "user@example.c",             # Invalid - TLD too short
    ]
    
    print("Testing various email addresses:")
    print("-" * 60)
    
    for email in test_emails:
        is_valid = validate_email(email)
        status = "✓ VALID" if is_valid else "✗ INVALID"
        print(f"{status:12} | {email}")
    
    print()
    print("=" * 60)
    print()
    
    # Interactive mode
    print("Interactive Email Validation")
    print("-" * 60)
    
    while True:
        try:
            email = input("\nEnter an email address to validate (or 'quit' to exit): ").strip()
            
            if email.lower() in ['quit', 'exit', 'q']:
                print("\nThank you for using the Email Validator!")
                break
            
            if not email:
                print("Please enter an email address.")
                continue
            
            is_valid, message = validate_email_detailed(email)
            
            if is_valid:
                print(f"✓ VALID: {message}")
            else:
                print(f"✗ INVALID: {message}")
                
        except KeyboardInterrupt:
            print("\n\nProgram terminated by user.")
            break


if __name__ == "__main__":
    main()