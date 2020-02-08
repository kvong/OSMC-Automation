# Import xbmc library to control osmc player
import xbmc
import time
import datetime
from random import *

# Author: Khanh Vong
# Description: Tv show automation

# Set watch option
randomize = 1
sequential = 0
watch_option = randomize

# Pick show to play "HIMYM" or "FRIENDS"
show = "DrakeAndJosh"
show = "HIMYM"
show = "BigBang"
show = "FRIENDS"

# Get current time of day
hour = datetime.datetime.now().hour

# Set size of playlist according to time of day 
if hour > 8 and hour < 21:
    # During day time set long playlist
    size = 30
    show = "BigBang"
else:
    # Short playlist size for night
    size = 9
    show = "BigBang"
    show = "FRIENDS"

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


if ( watch_option == sequential ):
# Watch with bookmarks
# Open to read number from bookmark.dat as an integer
    f = open("/home/osmc/.kodi/userdata/Automation.dat/" + show + "_bookmark.dat", "r")
#bookmark = int(f.readline())
## Use modulus so that playlist will start over when we reach the end
    start = bookmark
    bookmark = ((bookmark + (size - 1)) % episodes) + 1
    f.close()
## Update bookmark
    f = open("/home/osmc/.kodi/userdata/Automation.dat/" + show + "_bookmark.dat", "w+")
    f.write(str(bookmark)) 
    f.close()
elif ( watch_option == randomize )
# Watch at random
# Randomly pick a show
    seed()
    bookmark = randint(1, episodes)
    start = bookmark

# Random First Fit Scheduling
    f = open("/home/osmc/.kodi/userdata/Automation.dat/" + show + "_mem.dat", "r")

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

    bit = 0

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
    block_size = np.array(block_stop) - np.array(block_start)

# Get random point
    seed()
    random_point = randint(0, len(showlist) - 1 - size)

    print(available_extend)
    print(available)
    print(block_size)
    print(block_start)
    print(block_stop)

    print(random_point)

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
        f = open("/home/osmc/.kodi/userdata/Automation.dat/" + show + "_mem.dat", "w")
        print('Writing blocks %d' % random_point)
        f.writelines([str(available_extend[i]) + '\n' for i in range(len(available_extend))])
        f.close()
    else:
        # Find opening block
        for i in range(len(block_stop)):
            # If block size has enough space available
            if block_stop[i] - block_start[i] > size:
                # Pick a random point in the block we are looking at
                random_point = randint(block_start[i], block_stop[i] - size)
                # Check that the block is valid for playing
                if block_start[i] < random_point and block_stop[i] > random_point and available[i] != 1:
                    # Updating available vector for new block
                    for j in range(len(available_extend)):
                        if j == random_point - 1:
                            for k in range(size):
                                available_extend[random_point + k] = 1
                            break
                    # Writing a the block to 'mem'
                    f = open("/home/osmc/.kodi/userdata/Automation.dat/" + show + "_mem.dat", "w")
                    print('Writing blocks %d' % random_point)
                    f.writelines([str(available_extend[j]) + '\n' for j in range(len(available_extend))])
                    print(available_extend)
                    f.close()
                    break
            # If in the end of iterations and we can't find any blocks, then reset available vector to all 0s, and start any where
            if i == len(block_start) - 1:
                print('Resetting blocks')
                f = open('mem', 'w')
                random_point = randint(0, len(available_extend) - 1 - size)
                available_extend = [0 for k in range(len(available_extend))]
                for k in range(size):
                    available_extend[random_point + k] = 1
                print(available_extend)
                for j in range(count):
                    f.write(str(available_extend[j]) + '\n')
                f.close()
         
    print('starting point of playlist is %d' % random_point)
    start = random_point

# Write to current playlist
# Open playlist.dat for reading
f = open("/home/osmc/.kodi/userdata/Automation.dat/" + show + "_episodelist.dat", "r")
# Loop through every video individual video in xxxxx_episodelist.dat
for i in range(episodes):
    # Once we find where the book mark is loop, start adding video to a list
    episode = f.readline().strip('\n')
    if i + 1 == start :
        # Read line from playlist.dat removing \n at the end
        episode = d + episode
        episodelist = [ episode ]
        fw = open("/home/osmc/.kodi/userdata/Automation.dat/currentplaylist.dat", "w+")
        fw.write(str(episode) + '\n')
        for j in range(size - 1):
            episode = f.readline().strip('\n')
            episode = d + episode
            episodelist.append( episode )
            fw.write(str(episode) + '\n')
        fw.close()
        break
f.close()


# Get osmc current playlist and clear it
playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
playlist.clear()
    
# Add list to playlist
for k in range(len(episodelist)):
    playlist.add(str(episodelist[k]))

# Play videos
xbmc.Player().play(playlist)


# Set timer for shutdown after every episode in playlist is played
# converted to seconds
time.sleep(size * 60 * 24)
xbmc.shutdown()
