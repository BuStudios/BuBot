import re
import time
from datetime import datetime

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
    
    # check for any structured time layout, e.g YYYY-MM-DD HH:MM:SS

    time_pattern = r"(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})(?:(?: +|T)(?P<hour>\d{1,2})(?::(?P<minute>\d{1,2}))?(?::(?P<second>\d{1,2}))?)?"
    match = re.match(time_pattern, time)
    if match:
        date_groups = match.groupdict()

        # convert to the YYYY-MM-DD HH:MM:SS format
        # use -or- to remove any None and replace it with a 0

        year, month, day, hour, minute, second = date_groups["year"] or "0", date_groups["month"] or "0", date_groups["day"] or "0", date_groups["hour"] or "0", date_groups["minute"] or "0", date_groups["second"] or "0"

        try:
            new_time = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
            timestamp = int(datetime.timestamp(new_time)) * 1000
        except Exception:
            return "error"

        return timestamp
    
    # check for relative time expressions, e.g 4y 5min



print(datetimeParse("5min"))