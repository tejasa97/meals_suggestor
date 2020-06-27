from datetime import datetime

DAYS_TO_INT = {
    'Sunday'    : 0,
    'Monday'    : 1,
    'Tuesday'   : 2,
    'Wednesday' : 3,
    'Thursday'  : 4,
    'Friday'    : 5,
    'Saturday'  : 6,
}

ID_TO_DAY = {
    0 : 'Sunday',
    1 : 'Monday',
    2 : 'Tuesday',
    3 : 'Wednesday',
    4 : 'Thursday',
    5 : 'Friday',
    6 : 'Saturday'
}

def check_valid_day(day):

    return DAYS_TO_INT.get(day, False)

def get_day_from_id(day_id):

    return ID_TO_DAY.get(day_id)

def get_current_week_number():

    return datetime.now().isocalendar()[1]
    