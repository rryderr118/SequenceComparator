'''
Created on Dec 7, 2020

@author: Ryder Holder
'''
from classes import SequenceCompare, db_entries
from classes import db_utils
    
def findMatch(pri_seq):
    data = pullSequences()
    
    outSeqID = None
    #isParent = False
    for entry in data:
        lenStoredSequence = -1
        currentSequenceID = -1
        for value in entry.values.items():
            if value[0] == 'seq_id':
                currentSequenceID = value[1]
            if value[0] == 'pri_seq':
            #compare sequence look for "best" match
                if SequenceCompare.compareSequences(pri_seq, value[1]):
                    if len(pri_seq) > lenStoredSequence:
                        outSeqID = currentSequenceID
                        lenStoredSequence = len(value[1])
                        #could possible want to store sub sequence if modeMap pri seq is smaller
                        #storeSubSequence()
    
    '''
    if isParent:
        modeMap.pri_seq_type = 'PARENT'
    else:
        modeMap.pri_seq_type = 'CHILD'
    '''
    return outSeqID


def pullSequences():
    db = db_utils.db_connections()
    db.connect2db()
    results = db.retrieve('env_sequence_elements', ['seq_id', 'pri_seq'], 0, '')
    return results


#this is a placeholder for storing the subsequence if I needed
def storeSubSequence(pri_seq, nextID):
    #this needs testing, otherwise use execute below
    db = db_utils.db_connections()
    db.add('env_sequence_elements', db_entries('env_sequence_elements',[nextID, pri_seq]))
    #OR
    db = db_utils.db_connections()
    db.execute('insert into env_sequence_elements (seq_id, pri_seq) values (' + nextID + ', ' + pri_seq + ')')
    