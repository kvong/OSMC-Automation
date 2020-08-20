##########################################################################################
# Author: Khanh Vong
# Description: RaspberryPi Tv show automation player.
##########################################################################################

# Import xbmc library to control osmc player
from scheduler import Scheduler # Newly Added
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
    show = "FRIENDS"
    show = "BigBang"
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
    random_point, available, available_extend, block_start, block_stop, open_index = Scheduler.RandomFirstFit(mem_filename, episodes, size)
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

count = 0
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
                print('Writing blocks %d' % (random_point + count))
                count += 1
                print(available_extend)
            else:
                for i in range(len(block_stop)):
                    # Check that the block is valid for playing
                    if block_start[i] <= random_point and block_stop[i] > random_point:
                        # Writing a the block to 'mem'
                        f = open(mem_filename, 'w')
                        print('Writing blocks %d' % random_point)
                        count += 1
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
