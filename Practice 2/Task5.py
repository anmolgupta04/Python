import re


def count_words(filename):
    """
    Count word occurrences in a text file.
    
    Args:
        filename (str): Name of the file to read
    
    Returns:
        dict: Words and their counts in alphabetical order
    """
    try:
        # Read the file
        with open(filename, 'r') as file:
            text = file.read()
        
        # Convert to lowercase and extract words
        words = re.findall(r'\b[a-z]+\b', text.lower())
        
        # Count occurrences
        word_count = {}
        for word in words:
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1
        
        # Sort alphabetically
        sorted_words = dict(sorted(word_count.items()))
        
        return sorted_words
    
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found!")
        return None


# Main program
print("File Word Counter")
print("-" * 40)

filename = input("Enter filename: ")

word_counts = count_words(filename)

if word_counts:
    print(f"\nWord Count Results (Alphabetical Order)")
    print("-" * 40)
    print(f"{'Word':<20} {'Count':<10}")
    print("-" * 40)
    
    for word, count in word_counts.items():
        print(f"{word:<20} {count:<10}")
    
    print("-" * 40)
    print(f"\nTotal unique words: {len(word_counts)}")
    print(f"Total words: {sum(word_counts.values())}")