# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 22:21:16 2016

@author: PaulJ
"""

def longestSumSeries(sumToFind, listOfComponents):
    #print("Start longestSumSeries:", sumToFind, listOfComponents, len(listOfComponents))
    if len(listOfComponents) == 1:
        #print("Only one element left:", listOfComponents)
        if listOfComponents[0] == sumToFind:
            #print("Found a solution, yea! Returning", listOfComponents)
            return listOfComponents
        else:
            #print("Only one trial element in list but it doesn't complete the series")
            raise ValueError

    longestSeries = []
    for aCompLeftNo, aCompLeft in enumerate(listOfComponents):
        #print("At start of for loop, aCompLeft:", aCompLeft)
        newRemainder = sumToFind - aCompLeft
        #print("newRemainder:", newRemainder)
        if newRemainder == 0:
            #print("Found a solution", newRemainder, "=", sumToFind, "-", aCompLeft)
            return [aCompLeft]
        if newRemainder < 0:
            #print("Trial number", aCompLeft, "exceded sumToFind of", sumToFind)
            continue
        remainingList = (listOfComponents[:aCompLeftNo] +
                         listOfComponents[aCompLeftNo+1:])
        try:
            nextBestSeries = ([aCompLeft] +
                              longestSumSeries(newRemainder,
                                               remainingList))
        except ValueError:
            continue
        #print(nextBestSeries)
        if sum(nextBestSeries) == sumToFind:
            if len(nextBestSeries) > len(longestSeries):
                longestSeries = nextBestSeries[:]
    if len(longestSeries) > 0:
        #print ("longestSeries:", longestSeries)
        return longestSeries
    else:
        raise ValueError