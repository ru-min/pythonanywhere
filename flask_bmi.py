def calculate(weight, height):
    bmi = weight / (height ** 2)
    bmi = round(bmi, 1)
    return bmi

def health(bmi):
    if bmi <= 18.5:
        health = "You are underweight! Eat more."
    elif bmi <= 22.9:
        health = "Congrats! You are healthy."
    elif bmi <= 29.9:
        health = "You are overweight! Watch your diet."
    else:
       health = "You are Obese! You need to reduce your weight now! "
    return health
