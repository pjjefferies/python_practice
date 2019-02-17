# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 21:58:34 2019

@author: PaulJ
"""

pk_cache = {'0:0': 1}


def pk(k, n):
    input_cache_str = ':'.join([str(k), str(n)])
    if input_cache_str in pk_cache:
        return pk_cache[input_cache_str]
    if k <= 0 or n <= 0:
        return 0
    result = pk(k, n-k) + pk(k-1, n-1)
    pk_cache[':'.join([str(k), str(n)])] = result
    return result


def exp_sum(n):
    p = 0
    for k in range(1, n+1):
        p += pk(k, n)
    return p
