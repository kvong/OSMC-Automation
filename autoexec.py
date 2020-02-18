# Import xbmc library to control osmc player
import xbmc
import time
import datetime
from random import *
import numpy as np
from scheduler import rrf_scheduler

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
elif ( watch_option == randomize ):
    mem_filename = "/home/osmc/.kodi/userdata/Automation.dat/" + show + "_mem.dat"
    # Watch at random
    start = rff_scheduler(mem_filename, size)

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
