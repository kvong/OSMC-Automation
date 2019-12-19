# Import xbmc library to control osmc player
import xbmc
import time
from random import *

# Author: Khanh Vong
# Description: Tv show automation

# Pick show to play "HIMYM" or "FRIENDS"
show = "DrakeAndJosh"
show = "HIMYM"
show = "FRIENDS"
show = "BigBang"

# Directory where our videos are located
d = "/media/ElementDrive/" + show + "/" 

# Size of playlist
size = 9

# Change episode list depending on show
if show == "HIMYM":
    episodes = 208
elif show == "FRIENDS":
    episodes = 234
elif show == "DrakeAndJosh":
    episodes = 58
elif show == "BigBang":
    episodes = 159
else:
    episodes = 0

# Open to read number from bookmark.dat as an integer
#f = open("/home/osmc/.kodi/userdata/Automation.dat/" + show + "_bookmark.dat", "r")
#bookmark = int(f.readline())
# Use modulus so that playlist will start over when we reach the end
#start = bookmark
#bookmark = ((bookmark + (size - 1)) % episodes) + 1
#f.close()

# Randomly pick a show
bookmark = randint(1, episodes)
start = bookmark

# To know which episode to play
# - Pick an episode and subtract 9 from it


# Open to update bookmark.dat for time we power on
#f = open("/home/osmc/.kodi/userdata/Automation.dat/" + show + "_bookmark.dat", "w+")
#f.write(str(bookmark)) #Note: subtract 4 to handle tv double powered on bug *works better with even playlist
#f.close()

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


# Set timer for shutdown ( 200 minutes )
# converted to seconds
time.sleep(size * 60 * 23)
xbmc.shutdown()
