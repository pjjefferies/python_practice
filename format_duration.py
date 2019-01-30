# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 10:41:47 2019

@author: PaulJ
"""


def format_duration(seconds):
    if seconds == 0:
        return 'now'
    years, seconds = seconds // (60*60*24*365), seconds % (60*60*24*365)
    days, seconds = seconds // (60*60*24), seconds % (60*60*24)
    hours, seconds = seconds // (60*60), seconds % (60*60)
    minutes, seconds = seconds // 60, seconds % 60
    years_str = (str(years) + ' years' if years > 1
                 else ('1 year' if years == 1
                       else ''))
    days_str = (str(days) + ' days' if days > 1
                else ('1 day' if days == 1
                      else ''))
    hours_str = (str(hours) + ' hours' if hours > 1
                 else ('1 hour' if hours == 1
                       else ''))
    mins_str = (str(minutes) + ' minutes' if minutes > 1
                else ('1 minute' if minutes == 1
                      else ''))
    secs_str = (str(seconds) + ' seconds' if seconds > 1
                else ('1 second' if seconds == 1
                      else ''))

    result_str = ''
    for a_time_str in [years_str, days_str, hours_str, mins_str, secs_str]:
        if a_time_str:
            result_str += (a_time_str + ', ')
    result_str = result_str[:-2]
    if result_str.count(','):
        result_str = result_str[::-1].replace(' ,', ' dna ', 1)[::-1]

    return result_str
