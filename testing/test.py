import sys
import os
sys.path.append(os.getcwd())

from util.timeparser import datetimeParse

print(datetimeParse("1min"))
print(datetimeParse("1year 5 weeks 12 days 11.5min"))