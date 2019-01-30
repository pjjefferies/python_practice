# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 00:47:04 2019

@author: PaulJ
"""

def sqInRect(length, width):
    # your code
    if length == width:
        return None
    if width > length:
        length, width = width, length
    solution = []
    while width > 0:
        solution.append(width)
        length -= width
        if width > length:
            length, width = width, length
    return solution
