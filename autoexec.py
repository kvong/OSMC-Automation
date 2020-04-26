##########################################################################################
# Author: Khanh Vong
# Description: RaspberryPi Tv show automation player.
##########################################################################################

# Import xbmc library to control osmc player
import xbmc     # REMOVE FOR TEST
import time
import datetime
from random import *
import numpy as np

# Watch option constants
randomize = 1
sequential = 0

# Set watch option
watch_option = sequential

# Pick show to play "HIMYM" or "FRIENDS"
show = "DrakeAndJosh"
show = "BigBang"
show = "FRIENDS"
show = "test"

# Get current time of day
hour = datetime.datetime.now().hour

# Set size of playlist according to time of day 
if hour > 8 and hour < 21:
    # During day time set long playlist
    size = 18
    show = "BigBang"
    show = "FRIENDS"
    #show = "test"      # UNCOMMENT FOR TEST
else:
    # Short playlist size for night
    size = 9
    show = "FRIENDS"
    #show = "test"      # UNCOMMENT FOR TEST

# Directory where our videos are located
d = "/media/ElementDrive/" + show + "/" 

# Change episode list depending on show
if show == "HIMYM":
    episodes = 208
elif show == "FRIENDS":
    episodes = 234
elif show == "DrakeAndJosh":
    episodes = 58
elif show == "BigBang":
    episodes = 279
else:
    episodes = 0

# Set a random play point initially to 0
random_point = 0

if ( watch_option == sequential ):
    # Watch with bookmarks
    # Open to read number from bookmark.dat as an integer
    f = open("/home/osmc/.kodi/userdata/Automation.dat/" + show + "_bookmark.dat", "r")
    bookmark = int(f.readline())
    start = bookmark
    f.close()
elif ( watch_option == randomize ):
    mem_filename = "/home/osmc/.kodi/userdata/Automation.dat/" + show + "_mem.dat"
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
    start = random_point
     
episodelist = []
entire_episodelist = []
current_playlist = []
# Write to current playlist
# Open playlist.dat for reading
f = open("/home/osmc/.kodi/userdata/Automation.dat/" + show + "_episodelist.dat", "r")
# Loop through every video individual video in xxxxx_episodelist.dat
for i in range(episodes):
    # Once we find where the book mark is loop, start adding video to a list
    episode = f.readline().strip('\n')
    if i + 1 == start :
        current_playlist.append( episode )
        # Read line from playlist.dat removing \n at the end
        episode = d + episode
        episodelist.append( episode )
        fw = open("/home/osmc/.kodi/userdata/Automation.dat/currentplaylist.dat", "w+")
        fw.write(str(episode) + '\n')
        for j in range(size - 1):
            episode = f.readline().strip('\n')
            current_playlist.append( episode )
            episode = d + episode
            episodelist.append( episode )
            fw.write(str(episode) + '\n')
        fw.close()
    entire_episodelist.append( episode )
f.close()

# Add padding at the end of entire_episodelist
entire_episodelist.extend( entire_episodelist )

# Get osmc current playlist and clear it           # REMOVE ON TEST 
playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)      # REMOVE ON TEST 
playlist.clear()                                   # REMOVE ON TEST 
    
# Add list to playlist                             # REMOVE ON TEST 
for k in range(len(episodelist)):                  # REMOVE ON TEST 
    playlist.add(str(episodelist[k]))              # REMOVE ON TEST 

# Play videos                                      # REMOVE ON TEST 
xbmc.Player().play(playlist)                       # REMOVE ON TEST 

##########################################################################################
# Function to get duration of video using ffprobe. #
##########################################################################################

import subprocess

def get_duration(filename):
    result = subprocess.check_output(["/home/osmc/ffmpeg/ffprobe", "-v", "error", "-show_entries", 
            "format=duration", "-of", "default=noprint_wrappers=1:nokey=1",
            filename])
    return float(result)

##########################################################################################

# Log episode watched into list
for k in range(size):
    # Get current episode name
    episode_filename = d + entire_episodelist[start + k]

    # Log playlist at the end of playthrough
    if ( watch_option == sequential ):
        ## Use modulus so that playlist will start over when we reach the end
        bookmark = (bookmark % episodes) + 1

        ## Update bookmark
        f = open("/home/osmc/.kodi/userdata/Automation.dat/" + show + "_bookmark.dat", "w+")
        f.write(str(bookmark)) 
        f.close()
    elif ( watch_option == randomize ):
        # Update episode list one at a time
        available_extend[random_point + k] = 1

        # If available list is empty, then the vector is all 0s
        if len(available) == 0:
            # Write new available vector to file
            f = open(mem_filename, 'w')
            print('Writing blocks %d' % random_point)
            f.writelines([str(available_extend[i]) + '\n' for i in range(episodes)])
            f.close()
        else:
            open_index_length = len(open_index)
            if open_index_length == 0:
                f = open(mem_filename, 'w')
                for j in range(episodes):
                    f.write(str(available_extend[j]) + '\n')
                f.close()
            else:
                for i in range(len(block_stop)):
                    # Check that the block is valid for playing
                    if block_start[i] <= random_point and block_stop[i] > random_point:
                        # Writing a the block to 'mem'
                        f = open(mem_filename, 'w')
                        print('Writing blocks %d' % random_point)
                        f.writelines([str(available_extend[j]) + '\n' for j in range(episodes)])
                        print(available_extend)
                        f.close()
                        break

    episode_duration = get_duration(episode_filename)       # REMOVE ON TEST

    # Create a summary file for quick viewing without looking into dat files
    f_info = open('/home/osmc/.kodi/userdata/Automation.dat/summary.dat', 'w+')
    f_info.write('Current show: %s\n' % (show))
    f_info.write('Current episode: %d\n' % (start + k))
    f_info.write('Current playlist:\n')
    for i in range(len(current_playlist)):
        if i == k:
            f_info.write('> %d. %s\n' % ( i + 1, current_playlist[i]))
        else:
            f_info.write('  %d. %s\n' % ( i + 1, current_playlist[i]))
    f_info.close()
    # Sleep until episode ends         # REMOVE ON TEST 
    time.sleep( episode_duration )     # REMOVE ON TEST 

time.sleep(60*3)                       # REMOVE ON TEST

f_info = open('/home/osmc/.kodi/userdata/Automation.dat/summary.dat', 'w+')
f_info.write('No show playing at the moment.\n')
f_info.close()

# Log playlist at the end of playthrough    # REMOVE ON TEST
xbmc.shutdown()                             # REMOVE ON TEST 
