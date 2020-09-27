'''
Jeremy Kansas
CS 499
Artifact 2 part 2 of 2
Raspberry Pi "WetSpec" Script - Hash Table Implementation
Used as part of Category 2 - Data Structures and Algorithms
'''


from datetime import datetime
from datetime import timedelta
from time import perf_counter

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

        # reset data count, rehash will recount data
        self.data_count = 0

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
        result = None

        index = self._get_hash(key)

        # if current item does not match key and is not empty, increment
        while (self.table[index] != None and key != self.table[index][0]):
            index += 1

        return self.table[index]




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



# main function, demo stuff

if __name__ == '__main__':

    # starting small, lots of data
    start_size = 11
    dummy_items = 10000

    ht = HashTableJK(start_size)
    dummy = create_dummy(dummy_items)

    for item in dummy:
        ht.insert(item)


    print("\nInserts: {}\nCollisions: {}\nProbes: {}".format(dummy_items, ht.collision_count, ht.probe_count))
    print("Start Size: {}\nEnd Size: {}\nResizes: {}\n".format(start_size, ht.current_size, ht.resize_count))


    # dict for comparison
    dummy_dict = {}
    for item in dummy:
        dummy_dict[item[0]] = item


    linear_times = []
    pydict_times = []
    hashget_times = []

    test_count = 10000


    for test in range(test_count):
        choice = r.randrange(0, dummy_items)

        # linear search  (if I had more time would be better to compare against binary search)
        start = perf_counter()
        for i in dummy:
            if i == dummy[choice]:
                item = i
                break
        perf = perf_counter() - start
        linear_times.append(perf)

        # my hash lookup
        start = perf_counter()
        item = ht.get(dummy[choice][0])
        perf = perf_counter() - start
        hashget_times.append(perf)

        # dictionary lookup
        start = perf_counter()
        item = dummy_dict.get(dummy[choice][0])
        perf = perf_counter() - start
        pydict_times.append(perf)




    print("\nLinear search array for item.\n\tPerformed {} times for a total time of {} seconds.".format(test_count, sum(linear_times)))
    print("Retrieving from my hash table.\n\tPerformed {} times for a total time of {} seconds.".format(test_count, sum(hashget_times)))
    print("Comparing to Python dictionary.\n\tPerformed {} times for a total time of {} seconds.\n".format(test_count, sum(pydict_times)))
