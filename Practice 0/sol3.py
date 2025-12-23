# Grade calculator

Score = int(input("enter a number :"))

if Score >= 101:
    print("please check your grade")
    exit()

if Score >= 90:
    grade = "A"
elif Score >= 80:
    grade = "B"
elif Score >= 70:
    grade = "c"
elif Score >= 60:
    grade = "D"
else :
    grade = "F"

print("The grade opten by student", grade)

