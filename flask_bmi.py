def calculate(weight, height):
    try:
        height = height/100
        bmi = weight / (height ** 2)
        bmi = round(bmi, 1)
    except ZeroDivisionError:
        bmi = 0.0
    return bmi

def health(bmi):
    if bmi < 9:
        health = "Please enter a valid height and weight values."
    elif bmi < 18.5:
        health = "You are underweight! Eat more."
    elif bmi <= 24.9:
        health = "Congrats! You are in the healthy range."
    elif bmi <= 29.9:
        health = "You are overweight! Watch your diet."
    elif bmi<=90:
       health = "You are Obese! You need to reduce your weight now! "
    else:
        health = "Please enter a valid height and weight values."
    return health
