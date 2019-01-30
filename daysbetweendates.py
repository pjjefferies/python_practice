# By Websten from forums
#
# Given your birthday and the current date, calculate your age in days. 
# Compensate for leap days. 
# Assume that the birthday and current date are correct dates (and no time travel). 
# Simply put, if you were born 1 Jan 2012 and todays date is 2 Jan 2012 
# you are 1 day old.
#
# Hint
# A whole year is 365 days, 366 if a leap year. 

def is_a_leap_year(year):
    return ((year % 4 == 0) and ((year % 100 != 0) or (year % 400 == 0)))

def days_in_month(month, year):
    if is_a_leap_year(year):
        return (0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)[month]
    else:
        return (0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)[month]

def nextDay(year, month, day):
    day += 1
    if day > days_in_month(month, year):
        day = 1
        month += 1
        if month == 13:
            month = 1
            year += 1
    return year, month, day
        
def dateIsAfter(year1, month1, day1, year2, month2, day2):
    """Returns True if year1-month1-day1 is after year2-month2-day2.  Otherwise, returns False."""
    if year1 > year2:
        return True
    if year1 == year2:
        if month1 > month2:
            return True
        if month1 == month2:
            return day1 > day2
    return False        

def daysBetweenDates(year1, month1, day1, year2, month2, day2):
    if dateIsAfter(year1, month1, day1, year2, month2, day2):
        return "AssertionError"
    days = 0
    while dateIsAfter(year2, month2, day2, year1, month1, day1):
        days += 1
#        print year2, month2, day2, year1, month1, day1, days
        year1, month1, day1 = nextDay(year1, month1, day1)
    return days

def test():
    test_cases = [((2012,1,1,2012,2,28), 58), 
                  ((2012,1,1,2012,3,1), 60),
                  ((2011,6,30,2012,6,30), 366),
                  ((2011,1,1,2012,8,8), 585 ),
                  ((1900,1,1,1999,12,31), 36523)]
    
    for (args, answer) in test_cases:
        result = daysBetweenDates(*args)
        if result != answer:
            print "Test with data:", args, "failed"
        else:
            print "Test case passed!"

test()