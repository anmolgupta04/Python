alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

direction = input("Type 'encode' to encrypt, type 'decode' to decrypt: ").lower()
text = input("type your message:").lower()
shift = int(input("type the shift number:"))

def encrypt(original_text, shift_text):
    cipher_text = ""
    for letter in original_text:
        shift_position = alphabet.index(letter) + shift_text
        shift_position = shift_position % len(alphabet)
        cipher_text += alphabet[shift_position]
    print(f"\nThe cipher text is: {cipher_text}")


def decrypt(original_text, shift_text):
    cipher_text = ""
    for letter in original_text:
        shift_position = alphabet.index(letter) - shift_text
        shift_position = shift_position % len(alphabet)
        cipher_text += alphabet[shift_position]
    print(f"\nThe cipher text is: {cipher_text}")


def caesar(original_text, shift_text, encode_or_decode):
    cipher_text = ""
    for letter in original_text:

        if encode_or_decode == "decode":
            shift_text *= -1

        shift_position = alphabet.index(letter) - shift_text
        shift_position = shift_position % len(alphabet)
        cipher_text += alphabet[shift_position]
    print(f"\nThe cipher text is: {cipher_text}")



caesar(original_text=text, shift_text= shift, encode_or_decode=direction)
# encrypt(original_text = text, shift_text = shift)
# decrypt(original_text = text, shift_text = shift)