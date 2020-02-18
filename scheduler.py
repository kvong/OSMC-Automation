"""
Author:     Khanh Vong
Program:    TV show scheduler using first-random-fit scheduling algorithm.
Problem:    Suppose you have a playlist vector, and you would like to schedule
            a playlist of size k that does not over lap with previous playlist. 
            That is, if yesterday you watch episode 4-12, the episode you watch 
            today won't be any of those episodes you have already watched. Do this 
            for any size playlist. If all episodes have been watched or if we
            cannot create a playlist of size k (when our internal fragmentation
            is too small) flush the playlist vector and start scheduling from 
            anywhere.
"""

from random import *
import time
import datetime
import numpy as np
from random import seed
from random import random

# Random First Fit Scheduler function that takes in filename of file that has the resource vector { '0\n' ,'0\n' ,'0\n' ,'1\n' ,'1\n',... }
def rff_scheduler(mem_filename):

# Open memory file
    f = open(mem_filename, "r")

# Bit vector for episodes
    showlist = []
    indxlist = []
    count = 0
    size = 9

    available = []
    available_extend = []
    blocks = []
    block_start = [0]
    block_stop = []

    first_line = f.readline()
    bit = int(first_line[0])
    print(bit)
    f.close()

    f = open(mem_filename, "r")
# Filling lists
    for index, line in enumerate(f):
        if int(line[0]) != bit:
            available.append(bit)
            block_start.append(index)
            if bit == 1:
                bit = 0
            elif bit == 0:
                bit = 1

            if index != 0:
                block_stop.append(index)
        showlist.append(line[0])
        indxlist.append(index)
        count += 1
        available_extend.append(bit)
    f.close()

    if len(available) != 0:
        if available[len(available) -1] == 1:
            available.append(0)
        else:
            available.append(1)

# Append final ending point at the end of list
    block_stop.append(len(showlist))

    print(block_start)
    print(block_stop)

    block_size = np.array(block_stop) - np.array(block_start)

    print(available_extend)
    print(available)

# Get random point
    seed()
    random_point = randint(1, len(showlist) - 1 - size)

# If available list is empty, then the vector is all 0s
    if len(available) == 0:
        # Updating available vector; 
        for i in range(len(available_extend)):
            # Flip the bits of the items that are in playlist
            if i == random_point - 1:
                for j in range(size):
                    available_extend[random_point + j] = 1
                break
        # Write new available vector to file
        f = open('mem', 'w')
        print('Writing blocks %d' % random_point)
        f.writelines([str(available_extend[i]) + '\n' for i in range(len(available_extend))])
        f.close()
    else:
        open_index = []
        # Find opening block
        for i in range(len(block_stop)):
            # If block size has enough space available and unoccupied
            if block_stop[i] - block_start[i] > size and available[i] != 1:
                open_index.append(i)
        
        open_index_length = len(open_index)
        if open_index_length == 0:
            # If in the end of iterations and we can't find any blocks, then reset available vector to all 0s, and start any where
            print('Resetting blocks')
            f = open('mem', 'w')
            random_point = randint(1, len(available_extend) - 1 - size)
            available_extend = [0 for k in range(len(available_extend))]
            for k in range(size):
                available_extend[random_point + k] = 1
            print(available_extend)
            for j in range(count):
                f.write(str(available_extend[j]) + '\n')
            f.close()
        else:
            # Get random index from open_index
            random_index = randint(0, open_index_length - 1)
            random_open = open_index[random_index]
            # Pick a random point in the block we are looking at
            random_point = randint(block_start[random_open], block_stop[random_open] - size)
            for i in range(len(block_stop)):
                # Check that the block is valid for playing
                if block_start[i] <= random_point and block_stop[i] > random_point:
                    # Updating available vector for new block
                    for j in range(len(available_extend)):
                        if j == random_point - 1 or (random_point == 0 and j == 0):
                            for k in range(size):
                                available_extend[random_point + k] = 1
                            break
                    # Writing a the block to 'mem'
                    f = open('mem', 'w')
                    print('Writing blocks %d' % random_point)
                    f.writelines([str(available_extend[j]) + '\n' for j in range(len(available_extend))])
                    print(available_extend)
                    f.close()
                    break
         
    print('starting point of playlist is %d' % random_point)
    print(open_index)
    return random_point

