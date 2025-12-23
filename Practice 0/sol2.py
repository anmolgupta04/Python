# Movie Ticket Pricing 

age = int(input("Enter the age:"))
day = "Wednesday"

price = 12 if age >= 18 else 8

if day == "wednesday":
    price = price- 2

print("The Price of the movie ticket:", price)



