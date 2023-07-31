def calculate(weight, height):
    try:
        bmi = weight / (height ** 2)
        bmi = round(bmi, 2)
    except ZeroDivisionError:
	    bmi = "Please enter a valid height and weight."
    return bmi

