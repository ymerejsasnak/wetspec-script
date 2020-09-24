'''
Jeremy Kansas
CS 499
Artifact 2 part 2 of 2
Raspberry Pi "WetSpec" Script - Hash Table Implementation
Used as part of Category 2 - Data Structures and Algorithms
'''


from datetime import datetime


class HashTableJK():

    def __init__(self):
        self.current_size = 101
        self.table = [None] * self.current_size

    def get_hash(self, key: datetime):
        #convert to fully numeric value
        time = key.timestamp()
        #shift decimal point 6 to the right (microsecond digits in timestamp are right of decimal) and convert to integer
        time = time * 1000000
        #mod by table size to get index value
        index = time % len(self.table)

        return index

    def store_data(self, index: int, data: list):
        self.table[index] = data
        pass



#demo main

if __name__ == '__main__':
    ht = HashTableJK()

    for i in range(10):
        d = datetime.now()
        print(d)
        print(ht.get_hash(d))
