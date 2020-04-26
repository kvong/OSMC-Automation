##########################################################################################
# Author: Khanh Vong
# Description: RaspberryPi Tv show automation player.
##########################################################################################
from random import *
import numpy as np

def RandomFirstFit(mem_filename, episodes, size):
    # Watch at random
    # Random First Fit Scheduler function that takes in filename of file that has the resource vector { '0\n' ,'0\n' ,'0\n' ,'1\n' ,'1\n',... }
    # Open memory file
    f = open(mem_filename, "r")

   # Bit vector representing opening and occupied sequence (minimal representation)
    available = []
   # Extended bit vector representing opening and occupied resources for the entire episode list (extended representation length equal to the total number of episodes in episodelist)
    available_extend = []

   # Hold start and end index of a block
    block_start = [0]
    block_stop = []

    first_line = f.readline()
    bit = int(first_line[0])
    print(bit)
    f.close()

    # Filling representation vectors according to *mem.dat file
    f = open(mem_filename, "r")
    for index, line in enumerate(f):
        # Fill minimal representation vector on places where the bit change
        if int(line[0]) != bit:
            available.append(bit)
            block_start.append(index)
            if bit == 1:
                bit = 0
            elif bit == 0:
                bit = 1

            if index != 0:
                block_stop.append(index)
        available_extend.append(bit)
    f.close()

    if len(available) != 0:
        if available[len(available) -1] == 1:
            available.append(0)
        else:
            available.append(1)

   # Append final ending point at the end of list
    block_stop.append(episodes)

    print(block_start)
    print(block_stop)

    block_size = np.array(block_stop) - np.array(block_start)

    print(available_extend)
    print(available)

   # Get random point
    seed()
    random_point = randint(1, episodes - 1 - size)

   # If available list is empty, then set the vector is 0s
    if len(available) == 0:
        available_extend = [0 for k in range(episodes)]
    else:
        open_index = []
        # Find opening block
        for i in range(len(block_stop)):
            # If block size has enough space available and unoccupied
            if block_stop[i] - block_start[i] >= size and available[i] != 1:
                open_index.append(i)
        
        open_index_length = len(open_index)
        if open_index_length == 0:
            # If in the end of iterations and we can't find any blocks, then reset available vector to all 0s, and start any where
            print('Resetting blocks')
            random_point = randint(1, episodes - 1 - size)
            available_extend = [0 for k in range(episodes)]
            print(available_extend)
        else:
            # Get random index from open_index
            random_index = randint(0, open_index_length - 1)
            random_open = open_index[random_index]
            # Pick a random point in the block we are looking at
            random_point = randint(block_start[random_open], block_stop[random_open] - size)
    print('starting point of playlist is %d' % random_point)
    return random_point, available, available_extend, block_start, block_stop, open_index
