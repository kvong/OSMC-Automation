import xbmc

import time

# Author: Khanh Vong

# Directory where out videos are located
d = "/media/0C6B-AD88/HIMYM/" 

# Open to read number from bookmark.dat as an integer
f = open("/home/osmc/.kodi/userdata/bookmark.dat", "r")
bookmark = int(f.readline())
# Use modulus so that playlist will start over when we reach the end
bookmark = ((bookmark + 9) % 208) + 1
f.closed

# Open to update bookmark.dat for time we power on
f = open("/home/osmc/.kodi/userdata/bookmark.dat", "w")
f.write(str(bookmark))
f.closed

# Open playlist.dat for reading
f = open("/home/osmc/.kodi/userdata/playlist.dat", "r")
# Loop through every video individual video in playlist.dat
for i in range(208):
    # Once we find where the book mark is loop, start adding video to a list
    episode = f.readline().strip('\n')
    if i + 1 == bookmark:
        # Read line from playlist.dat removing \n at the end
        episode = d + episode
        episodelist = [ episode ]
        for j in range(9):
            episode = f.readline().strip('\n')
            episode = d + episode
            episodelist.append( episode )
        break
f.closed

# Get osmc current playlist and clear it
playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
playlist.clear()

# Add list to playlist
for k in range(len(episodelist)):
    playlist.add(str(episodelist[k]))

# Play videos
xbmc.Player().play(playlist)


# Set timer for shutdown ( 3 hours )
xbmc.sleep(10800000)
xbmc.shutdown()
