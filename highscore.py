student_scores = [150,140,752,4652,484,876,87465,846,879,68,46,65,56,46,879,7831]

# print(max(student_scores))
# total_exam_score = sum(student_scores)

# sum = 0
# for score in student_scores:
#     print(student_scores)
#     sum += score 
# print(sum)

max_score = 0
for score in student_scores:
    if score > max_score:
        max_score = score

print(max_score)

