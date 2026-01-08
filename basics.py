# # name = input("enter your name:")
# # print(len(name))
# # print(type("hello"))
# print("number of letters inn your name: "  , + len(input("enter your name")))


# import random
# random_heads_tails = random.randint(0 ,1)
# if random_heads_tails == 0:
#     print("heads")
# else:
#     print("tails")


# States_of_India = ["gujarat" , "hyderabad", 'jaipur', 'raipur', 'kashmir']
# print(States_of_India[1])


# import random
# friends = ['Anmol' , 'Natsu', 'Ansh', 'Aditya']
# print(random.choice(friends))
#
# print(random.randint(0,3))


# total = 0
# for number in range(1, 101):
#     total += number
# print(total)

# for number in range(1, 101):
#     if number % 3 == 0 and number % 5 == 0:
#         print("fizzbuzz")
#     elif number % 5 == 0:
#         print("Buzz")
#     elif number % 3 == 0:
#         print("fizz")
#     elif number % 2 == 0:
#         print("hello")
#     else:
#         print(number) 


# def life_in_weeks(age):
#     week_left = (90 - age) * 52
#     print(f"you have{week_left} week left to live")

# life_in_weeks(20)



# def greet(name ,location):
#     print(f"Hello {name}")
#     print(f"where are  you {location}")
#
# greet(name = "John", location = "San Francisco")


# programming_dictionary = {
#     "Anmol" : "Gupta",
#     "Ansh" : "Jaiswal",
#     "Riya" : "Pal",
#     "Varsha" : "Pal"
# }
# #
# # print(programming_dictionary["Ansh"])
#
# # programming_dictionary["Aditya"] = "Prakesh"
# programming_dictionary["Anmol"] = "Singh"
# # programming_dictionary = {}
# print(programming_dictionary)
#
# for key in programming_dictionary:
#     print(key)
#
#
# capitals = {
#     "france" : ["paris", "russia"],
#     "usa" : "united states"
# }
# print(capitals["france"])

# nested_list = ['a','b',['c','d']]
# print(nested_list[2][1])

# travel_log ={
#     "France" : {
#         "cities_visited": ["Paris", "Lille", "Dijon"],
#         "total_visits": 3
#     },
#     "Germany" : {
#         "cities_visited": ["Berlin", "Hamburg", "Stuttgart"],
#         "total_visits": 2
#     }
# }
#
# print(travel_log["Germany"]["cities_visited"][2])

# def name_funtion(f_name,l_name):
#     print(f_name.title())
#     print(l_name.title())

# name_funtion("anmol", "GUPTA")

# def is_leap_year(year):
#     if year % 4 == 0:
#         if year % 100 == 0:
#             if year % 400 == 0:
#                 return True
#             else:
#                 return False
#         else:
#             return True
#     else:
#         return False
    

# print(is_leap_year(2400))


# def add(n1, n2):
#   return n1 + n2
 
# def subtract(n1, n2):
#   return n1 - n2
 
# def multiply(n1, n2):
#   return n1 * n2
 
# def divide(n1, n2):
#   return n1 / n2
 
# print(add(2, multiply(5, divide(8, 4))))

# import calendar
# yy = 2020
# mm = 10
# #display calender
# print(calendar.month(yy,mm))


# def my_funtion():
#     for i in range(1,21):
#         if i == 20:
#             print("you got this")

# my_funtion()


# from random import randint
# dice_images = ["1", "2", "3", "4", "5", "6"]
# dice_num = randint(1 , 6)
# print(dice_images[dice_num])


# year = int(input("what's your year of birth ?"))

# if year >  1980 and year < 1994:
#     print("you are a millennial.")
# elif year >= 1994:
#     print("you are a Gen Z.")

# try:
#     age = int(input("How old are you?"))
# except ValueError:
#     print("You typed a invalid number. Please type a numerical integer such a 14")
#     age = int(input("how old are you?"))

# if age > 18:
#     print(f"you can drive at age {age}.")


# word_per_page = 0 
# pages = int(input("No. of pages: "))
# word_per_page = int(input("No. of words per page: "))
# total_words = pages * word_per_page
# print(total_words)


import random
import math


# def mutate(a_list):
#     b_list = []
#     new_item = 0
#     for item in a_list:
#         new_item = item * 2 
#         new_item += random.randint(1, 3)
#         new_item = math.add(new_item, item)
#         b_list.append(new_item)
#     print(b_list)


# mutate([1, 2, 3, 5, 8, 13])


# Target is the number up to which we count

# def fizz_buzz(target):
#     for number in range(1, target + 1):
#         if number % 3 == 0 or number % 5 == 0:
#             print("FizzBuzz")
#         if number % 3 == 0:
#             print("Fizz")
#         if number % 5 == 0:
#             print("Buzz")
#         else:
#             print([number])


# from turtle import Turtle, Screen
# timmy = Turtle()
# print(timmy)
# timmy.shape("turtle")
# timmy.color("coral")
# timmy.forward(100)

# my_screen = Screen()
# print(my_screen.canvheight)
# my_screen.exitonclick()


# s = "hello"
# t = s 
# s = s.upper()
# print(t)

# print({1,2,3} & {2,3,4}) // output = {2,3} print only same value from both 

# a = "python"
# b = "py" + "thon"
# print(a is b) 
# """ Why It Prints True
# Python uses an optimization called string interning. 
# When you create string literals (strings written directly in your code), 
# Python tries to reuse the same memory location for identical strings."""





