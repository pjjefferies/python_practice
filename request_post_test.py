# -*- coding: utf-8 -*-
"""
Created on Fri May  8 23:42:33 2020

@author: PaulJ
"""


#! /usr/bin/env python3

import os
import requests


filepath = '.'
filelist = os.listdir(filepath)
feedback = []

for a_file in filelist:
    file_path = filepath + '/' + a_file
    if a_file[0] == '.':
        continue
    print('file_path:', file_path)
    with open(file_path) as f:
        entry = {}
        entry['title'] = f.readline
        entry['name'] = f.readline
        entry['date'] = f.readline
        entry['feedback'] = f.readlines
    feedback.append(entry)

for an_entry in feedback:
    r = requests.post('https://34.72.202.230/feedback', data=an_entry)
    if r.status_code != requests.codes.ok:
        print('an_entryr:', an_entry['title'],
              ', status_code:', r.status_code)
