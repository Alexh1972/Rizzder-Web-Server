from datetime import date
import logging

logger = logging.getLogger(__name__)
def calculateYearsPassed(date):
    today = date.today()
    return today.year - date.year - (
            (today.month, today.day) < (date.month, date.day))

def calculateDaysPassed(date):
    today = date.today()

    return (today - date).days