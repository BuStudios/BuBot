import re
import time

def isNumber(input):
    try: float(input); return True
    except ValueError: return False


""""
example timestamp in millis = 1_711_564_138_797
unix timestamp in seconds = 1_711_564_138
the goal is to convert a input into a unix timestamp in millis
    --> e.g 5h5m should be converted into a specific time in millis
"""

def datetimeParse(time):

    if isNumber(time):
        # if the number is longer than 12 digits it is assumed to be a timestamp in millis
        if int(time) >= 1_000_000_000_000: return time
        # if the number is longer than 9 digits it is assumed to be a UNIX timestamp in seconds
        elif int(time) >= 1_000_000_000: return str(int(time) * 1000) # convert to millis
        else: return "error" 
    
    # check if input matches any structured time layout, e.g YYYY-MM-DD HH:MM:SS
    


print(datetimeParse("1223444534"))