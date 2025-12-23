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

def my_funtion():
    for i in range(1,21):
        if i == 20:
            print("you got this")

my_funtion()