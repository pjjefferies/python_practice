# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 21:59:44 2019

@author: PaulJ
"""

def anagrams(word, words):
    anagrams_found = []
    for a_word in words:
        a_word_remain = a_word
        poss_anagram = True
        for a_letter in word:
            print('1: a_word_remain:', a_word_remain)
            first_let_pos = a_word_remain.find(a_letter)
            if first_let_pos == -1:
                poss_anagram = False
                continue
            a_word_remain = (a_word_remain[:first_let_pos] +
                             a_word_remain[first_let_pos + 1:])
            print('2: a_word_remain:', a_word_remain)
        if not a_word_remain and poss_anagram:
            anagrams_found.append(a_word)
    return anagrams_found


print('result: ', anagrams('abba', ['aabb', 'abcd', 'bbaa', 'dada']))