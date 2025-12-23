print('''*******************************************************************************
          |                   |                  |                     |
 _________|________________.=""_;=.______________|_____________________|_______
|                   |  ,-"_,=""     `"=.|                  |
|___________________|__"=._o`"-._        `"=.______________|___________________
          |                `"=._o`"=._      _`"=._                     |
 _________|_____________________:=._o "=._."_.-="'"=.__________________|_______
|                   |    __.--" , ; `"=._o." ,-"""-._ ".   |
|___________________|_._"  ,. .` ` `` ,  `"-._"-._   ". '__|___________________
          |           |o`"=._` , "` `; .". ,  "-._"-._; ;              |
 _________|___________| ;`-.o`"=._; ." ` '`."\` . "-._ /_______________|_______
|                   | |o;    `"-.o`"=._``  '` " ,__.--o;   |
|___________________|_| ;     (#) `-.o `"=.`_.--"_o.-; ;___|___________________
____/______/______/___|o;._    "      `".o|o_.--"    ;o;____/______/______/____
/______/______/______/_"=._o--._        ; | ;        ; ;/______/______/______/_
____/______/______/______/__"=._o--._   ;o|o;     _._;o;____/______/______/____
/______/______/______/______/____"=._o._; | ;_.--"o.--"_/______/______/______/_
____/______/______/______/______/_____"=.o|o_.--""___/______/______/______/____
/______/______/______/______/______/______/______/______/______/______/[TomekK]
***************************************************************************''')

print("Welcome to Treasure Island.")
print("Your mission is to find the treasure.")
print("You have to find the treasure island first.")

choice1 = input('you\'re at a crossroad ,where do you want to go? Type "left"  or "right"? .').lower()
if choice1 == "left":
    choice2 =input('you have come to a lake.'
    'There is an island in the middle of the lake.'
     ' Type "wait" or to wait for a boat.'
    'Type "swim" to swim across. ').lower()
    if choice2 == "wait":
      choice3 =input("you arrive at the island unharmed. There are is house with 3 doors. one red ,"
                     "one yellow and one blue"
                    "which colour do you choose? ").lower()
      if choice3 == "red":
          print("It's a room full of gold. Game over.")
      elif choice3 == "yellow":
          print("It's a room full of fire you die. Game over.")
      elif choice3 == "blue":
          print("It's a room full of Chicken. you Won!")
    else:
        print("you got attack by a shark. Game Over")

else:
    print("you fell in to a hole. game over.")


