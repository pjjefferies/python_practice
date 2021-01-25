# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import re
import pandas as pd

with open("syslog.log") as fp:
    syslog_lines = fp.readlines()

users = pd.DataFrame(columns=['name', 'errors', 'infos'])
users.set_index('name', inplace=True)

errors = pd.DataFrame(columns=['error_name', 'count'])
errors.set_index('error_name', inplace=True)


for a_line in syslog_lines:
    user_name = re.search(r'\((.*)\)$', a_line).groups()[0]
    if user_name not in users.index:
        users = users.append(pd.Series(name=user_name,
                                       data={'errors': 0, 'infos': 0}))
    if re.search(r'ERROR', a_line):
        error_name = re.search(r'ERROR.(.*)$', a_line).groups()[0]
        if re.search(r'\[#?\d+\]', error_name):
            error_name = re.search(r'\[(#?\d+)\]', error_name).groups()[0]
        if re.search(r'\(.*\)', error_name):
            error_name = re.search(r'^(.*)\s\(.*\)$', error_name).groups()[0]
        if error_name in errors.index:
            errors.at[error_name, 'count'] = (
                errors.at[error_name, 'count'] + 1)
        else:
            errors.at[error_name, 'count'] = 1
        # errors[error_name] = errors.get(error_name, 0) + 1
        users.at[user_name, 'errors'] = users.at[user_name, 'errors'] + 1
        # user_error[user_name] = user_error.get(user_name, 0) + 1

    if re.search(r'INFO', a_line):
        users.at[user_name, 'infos'] = users.at[user_name, 'infos'] + 1
        # user_info[user_name] = user_info.get(user_name, 0) + 1

errors.sort_values(by='count', ascending=False, inplace=True)
users.sort_values(by='name', inplace=True)

errors.to_csv('error_list.csv')
users.to_csv('users_list.csv')

