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
        self.data_count = 0
        self.table = [None] * self.current_size

        self.collision_count = 0
        self.probe_count = 0
        self.resize_count = 0


    def __str__(self):
        output = []
        hashes = []
        for item in self.table:
            if item: # ie not None
                next_hash = self._get_hash(item[0])
                if next_hash in hashes:
                    collide = '*'
                else:
                    collide = ''
                    hashes.append(next_hash)
                output.append(collide + str(next_hash) + '   ' + str(item) + '\n')
            else:
                output.append('---\n')
        return ''.join(output)

    def brief(self, linelength):
        chars = 0
        for item in self.table:
            if item:
                print('0', end='')
            else:
                print('_', end='')
            chars += 1
            if chars == linelength:
                print()
                chars = 0
        print()

    def _get_hash(self, key: datetime):
        # zero out seconds and microseconds, get date as numeric value
        date = key.replace(second=0, microsecond=0)
        date = date.timestamp()

        #mod by table size to get actual index value
        index = int(date) % self.current_size

        return index


    def _store_data(self, index: int, data: list):
        self.table[index] = data
        self.data_count += 1


    def _collision(self, index):
        # default value is None so will return false if nothing there (no collision)
        return self.table[index]


    def _resize(self):
        # first double the size
        new_size = self.current_size * 2

        # then increment to next prime value
        self.current_size = next_prime(new_size)

        self.resize_count += 1


    def _rehash(self):
        # copy old table
        old_table = self.table[:]

        # create new table
        self.table = [None] * self.current_size

        # iterate through old table, rehashing into new
        for item in old_table:
            if item:
                self.insert(item)


    def insert(self, data: list):
        # get key from data (1st item in list is datetime)
        key = data[0]

        # hash key and get index
        index = self._get_hash(key)

        # if collision, increment index until there is no collision (linear probe)
        if self._collision(index):
            self.collision_count += 1
        while (self._collision(index)):
            index = (index + 1) % self.current_size
            self.probe_count += 1

        self._store_data(index, data)


        #check contents vs size

        if (self.data_count / self.current_size) > 0.5:
            self._resize()
            self._rehash()



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
    d += timedelta(minutes=r.randint(-999999999, 999999999))

    # then 0 the minutes so we're on the 0/30 interval, and 0 sec and micro because unused
    d = d.replace(minute=0, second=0, microsecond=0)

    # loop until desired # of data points collected
    while (len(data) < total):

      # check if daylight hours and a little random to simulate lack of 'daylight' conditions (ie cloudy)
      if d.hour >= 8 and d.hour <=20 and r.random() > 0.2:
          # add new dummy data
          data.append([d, r.randint(0, 100), r.randint(0, 100)])

      # increment time
      d += timedelta(minutes=30)


    return data




# get next prime number
def next_prime(n):

    # base case
    if (n <= 1):
        return 2

    m = n
    got_prime = False

    # Loop until is_prime returns true
    while(not got_prime):
        m = m + 1
        got_prime = is_prime(m)

    return m


# determine if n is prime
def is_prime(n):

    # Corner cases
    if(n <= 1):
        return False
    if(n <= 3):
        return True

    # This is checked so that we can skip
    # middle five numbers in below loop
    if(n % 2 == 0 or n % 3 == 0):
        return False

    for i in range(5,int(math.sqrt(n) + 1), 6):
        if(n % i == 0 or n % (i + 2) == 0):
            return False

    return True




# main function, test some stuff

if __name__ == '__main__':


    '''
    # roughly a year's worth of readings
    ht = HashTableJK(14009)
    dummy = create_dummy(7000)

    for item in dummy:
        ht.insert(item)
        
    # print('\n\n')
    #print(ht)
    #print()

    print("Inserts: {}\nCollisions: {}\nProbes: {}\n".format(7000, ht.collision_count, ht.probe_count))

    '''


    # starting small
    start_size = 11
    dummy_items = 100

    ht = HashTableJK(11)
    dummy = create_dummy(100)

    for item in dummy:
        ht.insert(item)

    print('\n\n')
    print(ht)
    print()

    print("Inserts: {}\nCollisions: {}\nProbes: {}\n".format(dummy_items, ht.collision_count, ht.probe_count))
    print("Start Size: {}\nEnd Size: {}\nResizes: {}\n".format(start_size, ht.current_size, ht.resize_count))


    #resizing about 2 too many times, why?
