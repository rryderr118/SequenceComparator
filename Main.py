'''
Created on Dec 7, 2020

@author: Ryder
'''
from classes import SequenceComparator

def Main(pri_seq = [7706, 7701, 5019, 8253]):
    matchedID = SequenceComparator.findMatch(pri_seq)
    print(matchedID)
    return matchedID
    
Main()