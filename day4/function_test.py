scores = [80, 55, 90]
def calculate_total(scores):
    total = 0
    for i in scores:
        total += i
    return total
def calculate_average(scores):
    total = 0
    for i in scores:
        total += i
    average = total / len(scores)
    return average
def is_passed(score):
    if score>=60:
        return True
    else:
        return False
print(calculate_total(scores))
print(calculate_average(scores))
print(is_passed(55))