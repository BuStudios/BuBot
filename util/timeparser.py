import re
from time import time as unix_time
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
    

    r""""
    !! This is not used as it would require the timezone of the user

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
    """

    # check for relative time expressions, e.g 5h 5min 10s

    pattern = r"\s*(?:(?P<years>\d+(?:\.\d+)?)\s*y(?:e?a?r?s?))?\s*(?:(?P<months>\d+(?:\.\d+)?)\s*m(?:o?nth|o)s?)?\s*(?:(?P<weeks>\d+(?:\.\d+)?)\s*w(?:(?:ee)?k?s?))?\s*(?:(?P<days>\d+(?:\.\d+)?)\s*d(?:ays?)?)?\s*(?:(?P<hours>\d+(?:\.\d+)?)\s*h(?:(our)?s?)?)?\s*(?:(?P<minutes>\d+(?:\.\d+)?)\s*m(?:in(?:ute)?s?)?)?\s*(?:(?P<seconds>\d+(?:\.\d+)?)\s*s(?:ec(?:ond)?s?)?)?\s*"
    match = re.match(pattern, time)
    
    if match:
        date_groups = match.groupdict()
        
        years, months, weeks, days, hours, minutes, seconds = date_groups["years"] or "0", date_groups["months"] or "0", date_groups["weeks"] or "0", date_groups["days"] or "0", date_groups["hours"] or "0", date_groups["minutes"] or "0", date_groups["seconds"] or "0"
        
        # this is not a very efficient nor accurate way to calculate the difference
        # i will change it when i have time to do so
        milliseconds = float(years) * 365 * 24 * 60 * 60 * 1000
        milliseconds += float(months) * 30 * 24 * 60 * 60 * 1000
        milliseconds += float(weeks) * 7 * 24 * 60 * 60 * 1000
        milliseconds += float(days) * 24 * 60 * 60 * 1000
        milliseconds += float(hours) * 60 * 60 * 1000
        milliseconds += float(minutes) * 60 * 1000
        milliseconds += float(seconds) * 1000

        # if more than 2 years error
        if milliseconds / 1000 / 60 / 60 / 24 / 265 >= 2:
            return "error"
        
        return round((unix_time() * 1000) + milliseconds)
    
    # no way to parse the time was found
    return "error"