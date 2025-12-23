distance = int(input("enter a distance :"))

if distance < 3:
    transport  = "walk"
elif distance <= 15:
    transport = "bike"
else:
    transport = "car"

print("google recommands you to go with" , transport)