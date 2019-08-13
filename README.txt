Description: Automatically play and turn off background tv show. ( Great for people who sleeps with the tv on )

Prerequisite:
	showname_bookmark.dat ( contain the index of the last episode played by osmc )
	showname_episodelist.dat ( contain the names of all the video files in a list)
	video files

Features:
	Python script will take the bookmark number and read that number of lines in playlist.dat.
	From that position it will create a list of the next 9 episode ( if reach the end, loop over)
	
	Shutdown in 3 hours.
