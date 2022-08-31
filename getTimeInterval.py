#!/usr/bin/env python3
import datetime as dt
from dateutil.tz import tz

def nextMonth(month, year):
    month += 1
    if month > 12:
        year += 1
        month = 1
    return (month, year)

def prevMonth(month, year):
    month -= 1
    if month < 1:
        year -= 1
        month = 12
    return (month, year)

def getPeriod(which, year = None, TZ = None):
    MS = 999999
    name = which
    if TZ:
        now   = dt.datetime.now(tz = tz.gettz(TZ))
    else:
        now   = dt.datetime.now()
    if year:
        now = now.replace(year = year)
    if which == 'Today':
        end   = now.replace(hour = 23, minute = 59, second = 59, microsecond = MS)
        start = now.replace(hour = 0, minute = 0, second =0, microsecond = 0)
    elif which == 'Yesterday':
        end   = now.replace(hour = 23, minute = 59, second = 59, microsecond = MS) - \
             dt.timedelta(days = 1)
        start = now.replace(hour = 0, minute = 0, second =0, microsecond = 0) - \
             dt.timedelta(days = 1)
    elif which == 'Prev7days':
        end   = now.replace(hour = 23, minute = 59, second = 59, microsecond = MS) - \
            dt.timedelta(days = 1)
        start = now.replace(hour = 0, minute = 0, second =0, microsecond = 0) - \
            dt.timedelta(days = 7)
    elif which == 'This Week':
        end   = now.replace(hour = 23, minute = 59, second = 59, microsecond = MS) - \
            dt.timedelta(days = 1)
        start = now.replace(hour = 0, minute = 0, second = 0, microsecond = 0) - \
            dt.timedelta(days = now.weekday())
    elif which == 'Last Week':
        end   = now.replace(hour = 23, minute = 59, second = 59, microsecond = MS) - \
            dt.timedelta(days = 1 + now.weekday())
        start = now.replace(hour = 0, minute = 0, second = 0, microsecond = 0) - \
            dt.timedelta(days = 7 + now.weekday())
    elif which == 'This Month':
        (nMonth, nYear) = nextMonth(now.month, now.year)
        if TZ:
            end   = dt.datetime(nYear, nMonth, 1, tzinfo = tz.gettz(TZ)) -\
                dt.timedelta(microseconds = 1)
        else:
            end   = dt.datetime(nYear, nMonth, 1) - dt.timedelta(microseconds = 1)
        start = now.replace(day = 1, hour = 0, minute = 0, second = 0, microsecond = 0)
        name = start.strftime('%b %Y')
    elif which == 'Last Month':
        if TZ:
            end   = dt.datetime(now.year, now.month, 1, tzinfo = tz.gettz(TZ)) - \
                dt.timedelta(microseconds = 1)
        else:
            end   = dt.datetime(now.year, now.month, 1) - dt.timedelta(microseconds = 1)
        (pMonth, pYear) = prevMonth(now.month, now.year)
        if TZ:
            start = dt.datetime(pYear, pMonth, 1, tzinfo = tz.gettz(TZ))
        else:
            start = dt.datetime(pYear, pMonth, 1)
        name = start.strftime('%b %Y')
    elif which == 'Last30Days':
        end   = now.replace(hour = 23, minute = 59, second = 59, microsecond = MS) - \
            dt.timedelta(days = 1)
        start = now.replace(hour = 0, minute = 0, second =0, microsecond = 0) - \
            dt.timedelta(days = 30)
    elif which == 'Year':
        if TZ:
            end   = dt.datetime(year = year + 1, month = 1, day = 1, tzinfo = tz.gettz(TZ)) - \
                dt.timedelta(microseconds = 1)
            start =  dt.datetime(year = year, month = 1, day = 1, tzinfo = tz.gettz(TZ))
        else:
            end   = dt.datetime(year = year + 1, month = 1, day = 1) - dt.timedelta(microseconds = 1)
            start =  dt.datetime(year = year, month = 1, day = 1)
        name = 'Year ' + start.strftime('%Y')
    elif which == 'LastYear':
        # 365(6) days
        end   = now.replace(hour = 23, minute = 59, second = 59, microsecond = MS) - \
             dt.timedelta(days = 1)
        start = now.replace(year = now.year - 1, \
                            hour = 0, minute = 0, second =0, microsecond = 0) - \
                            dt.timedelta(days = 1)
        #print(which, start, end)
    elif which == 'YearByMonth':
        # beginning of this month last year until yestarday
        end   = now.replace(hour = 23, minute = 59, second = 59, microsecond = MS) - \
            dt.timedelta(days = 1)
        start = now.replace(year = now.year - 1, day = 1, \
                            hour = 0, minute = 0, second =0, microsecond = 0)
        #print(which, start, end)
    elif which == 'All':
        if TZ:
            mytz = tz.gettz(TZ)
        else:
            mytz = None
        end   = dt.datetime(dt.MAXYEAR, 12, 31, 23, 59, 59, MS, tzinfo = mytz)
        start = dt.datetime(dt.MINYEAR,  1,  1,  0,  0,  0,  0, tzinfo = mytz)
    else:
        try:
            # interpret as a single date 'yyyy-mm-dd'
            start = dt.datetime.combine(dt.datetime.strptime(which, '%Y-%m-%d').date(), \
                                        dt.time.min)
            end   = dt.datetime.combine(dt.datetime.strptime(which, '%Y-%m-%d').date(), \
                                        dt.time.max)
        except:
            print('getPeriod: ', which, 'not implemented')
            start = end = None
    return start, end, name

