# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 23:34:19 2019

@author: PaulJ
"""


def cakes(recipe, available):
    return min(available.get(x, 0)//recipe[x] for x in recipe)
    # return (available.get(k, 0)/recipe[k] for k in recipe)
