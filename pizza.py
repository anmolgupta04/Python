from http.cookiejar import uppercase_escaped_char

print("Welcome to python pizza deliveries!")
size = input("What size pizza do you want? S, M or L").upper()
pepperoni = input("do you want pepperoni in your pizza? Y or N").upper()
extra_cheese = input("do you want extra cheese in your pizza? Y or N").upper()

bill = 0

if size == "S":
        bill = bill + 15
elif size == "M":
        bill = bill + 20
elif size == "L":
        bill = bill + 25
else:
    print("Please enter a valid size")
    exit()

if pepperoni == "Y":
     if size == "S":
        bill = bill + 2
     else:
         bill = bill + 3

if extra_cheese == "Y":
         bill = bill + 1

print(f"Your final bill is $ {bill}")
