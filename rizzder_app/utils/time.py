from datetime import date
def calculateYearsPassed(birthDay):
    today = date.today()
    return today.year - birthDay.year - (
            (today.month, today.day) < (birthDay.month, birthDay.day))