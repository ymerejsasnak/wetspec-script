'''
Jeremy Kansas
CS 499
Artifact 2 part 2 of 2
Raspberry Pi "WetSpec" Script - Hash Table Implementation
Used as part of Category 2 - Data Structures and Algorithms
'''


from datetime import datetime
from datetime import timedelta

import random as r
import math

# NOTE - will have to be sure wetspec takes readings exactly on the half hour (minutes wise, can drop sec and micro)
# and just hash by that so can search for reasonable number of possibles per day (12 hrs daylight, 25 readings max?)


class HashTableJK():

    def __init__(self):
        self.current_size = 211
        self.table = [None] * self.current_size

    def _get_hash(self, key: datetime):
        # zero out everything but date and convert it to an integer
        date = key.replace(hour=0, minute=0, second=0, microsecond=0)
        date = int(key.timestamp())

        # then get hour and minute values separately
        hour = key.hour
        minute = key.minute

        # conver to single integer indicating which half hour segment we are in
        # ex: 8:00 am is 16, 8:30 is 17, 9am is 18, etc.
        halfhour = h * 2 + m//30

        # add date and halfhour
        value = date + halfhour

        #mod by table size to get actual index value
        index = int(value) % self.current_size

        return index



    def _store_data(self, index: int, data: list):
        self.table[index] = data






    def insert(self, key: datetime, data: list):
        #get Hash
        #check for collision
        #resolve if necessary
        #check size
        #resize if nec
        pass


    def get(self, key: datetime):
        #get Hash
        #remember to check for potential linear probe store
        #return data if found else error/message/default?
        pass





# main function to make dummy data, test some stuff

if __name__ == '__main__':

    ht = HashTableJK()

    test = [0] * ht.current_size

    d = datetime.now()
    d = d.replace(minute=0, second=0, microsecond=0)
    d += timedelta(minutes=r.randint(10, 10000))


    for i in range(200):
        d += timedelta(minutes=30)

        if d.hour >= 8 and d.hour <= 20 and r.random() > 0.2:
            test[ht._get_hash(d)] += 1


    print(''.join([str(x) if x > 0 else '.' for x in test]))
    print('entries:')
    print(sum(test))
    print('collision percent:')
    print(sum([x-1 if x > 1 else 0 for x in test])/sum(test))
