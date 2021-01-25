# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import re

with open("syslog.log") as fp:
    syslog_lines = fp.readlines()

user_errors = {}
user_infos = {}

errors = {}

for a_line in syslog_lines:
    user_name = re.search(r'\((.*)\)$', a_line).groups()[0]
    # if user_name not in users.index:
    user_errors[user_name] = user_errors.get(user_name, 0)
    user_infos[user_name] = user_infos.get(user_name, 0)

    if re.search(r'ERROR', a_line):
        error_name = re.search(r'ERROR.(.*)$', a_line).groups()[0]
        if re.search(r'\[#?\d+\]', error_name):
            error_name = re.search(r'\[(#?\d+)\]', error_name).groups()[0]
        if re.search(r'\(.*\)', error_name):
            error_name = re.search(r'^(.*)\s\(.*\)$', error_name).groups()[0]
        errors[error_name] = errors.get(error_name, 0) + 1
        user_errors[user_name] = user_errors[user_name] + 1
    elif re.search(r'INFO', a_line):
        user_infos[user_name] = user_infos[user_name] + 1

# errors.sort_values(by='count', ascending=False, inplace=True)
# users.sort_values(by='name', inplace=True)

errors_list = [[k, errors[k]] for k in errors]
errors_list.sort(key=lambda x: x[1], reverse=True)

user_list = [[k, user_infos[k], user_errors[k]] for k in user_errors]
user_list.sort(key=lambda x: x[0])

with open("error_message.csv", mode="w") as fp:
    fp.write('Error, Count\n')
    for error in errors_list:
        fp.write(', '.join([error[0], str(error[1])]) + '\n')

with open("user_statistics.csv", mode="w") as fp:
    fp.write('Username, INFO, ERROR\n')
    for user_info in user_list:
        fp.write(', '.join([user_info[0],
                            str(user_info[1]),
                            str(user_info[2])]) +
                 '\n')

# errors.to_csv('error_list.csv')
# users.to_csv('users_list.csv')
