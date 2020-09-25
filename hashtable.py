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

    def __init__(self, init_size):
        self.current_size = init_size
        self.table = [None] * self.current_size


    def __str__(self):
        output = []
        for item in self.table:
            if item: # ie not None
                output.append(str(item) + '\n')
            else:
                output.append('---\n')
        return ''.join(output)

    def _get_hash(self, key: datetime):
        # zero out everything but date and convert it to an integer
        date = key.replace(hour=0, minute=0, second=0, microsecond=0)
        date = int(date.timestamp())

        # then get hour and minute values separately
        hour = key.hour
        minute = key.minute

        # conver to single integer indicating which half hour segment we are in
        # ex: 8:00 am is 16, 8:30 is 17, 9am is 18, etc.
        halfhour = hour * 2 + minute//30

        # add date and halfhour
        value = date + halfhour

        #mod by table size to get actual index value
        index = int(value) % self.current_size

        return index


    def _store_data(self, index: int, data: list):
        self.table[index] = data


    def _collision(self, index):
        # default value is None so will return false if nothing there (no collision)
        return self.table[index]




    def insert(self, data: list):
        # get key from data (1st item in list is datetime)
        key = data[0]

        # hash key and get index
        index = self._get_hash(key)

        # if collision, increment index until there is no collision (linear probe)
        while (self._collision(index)):
            index = (index + 1) % self.current_size

        self._store_data(index, data)


        #check contents vs size
        #resize if nec
        pass


    def get(self, key: datetime):
        #get Hash
        #remember to check for potential linear probe store  (ie something is there but not equal to expected?, search until empty slot or success?)
        #return data if found else error/message/default?
        pass






# function to make dummy data

def create_dummy(total):
    data = []

    # arbitrary starting point, randomized a bit
    d = datetime.now()
    d += timedelta(minutes=r.randint(-100000, 100000))

    # then 0 the minutes so we're on the 0/30 interval, and 0 sec and micro because unused
    d = d.replace(minute=0, second=0, microsecond=0)

    # loop until desired # of data points collected
    while (len(data) < total):

      # check if daylight hours and a little random to simulate lack of 'daylight' conditions (ie cloudy)
      if d.hour >= 8 and d.hour <=20 and r.random() > 0.2:
          # add new dummy data
          data.append([d, r.randint(30, 100), r.randint(0, 100)])

      # increment time
      d += timedelta(minutes=30)


    return data



# main function, test some stuff

if __name__ == '__main__':

    ht = HashTableJK(29)

    dummy = create_dummy(15)


    for item in dummy:
        ht.insert(item)

    print('\n\n')
    print(ht)
    print('\n\n')

    #print(''.join([str(x) if x > 0 else '.' for x in test]))
    #print('entries:')
    #print(sum(test))
    #print('collision percent:')
    #print(sum([x-1 if x > 1 else 0 for x in test])/sum(test))
    
