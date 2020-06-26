DAYS_OF_WEEK = {
    'Sunday'    : 0,
    'Monday'    : 1,
    'Tuesday'   : 2,
    'Wednesday' : 3,
    'Thursday'  : 4,
    'Friday'    : 5,
    'Saturday'  : 6,
}


def check_valid_day(day):

    if day not in DAYS_OF_WEEK:
        return False
