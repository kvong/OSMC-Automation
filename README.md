# Description:
Automatically play and turn off background tv show. (Great for people who sleeps with the tv on.)

# Prerequisite:
	* Raspberry PI with OSMC installed
	* SHOWNAME_bookmark.dat ( contain the index of the last episode played by osmc )
	* SHOWNAME_episodelist.dat ( contain the names of all the video files in a list)
	* SHOWNAME_mem.dat ( contain data for RRF scheduling )
	* currentplaylist.dat
	* Video files (must be playable by kodi)
	* python2 numpy
		* sudo apt install python-numpy

# Features:
	* Python script will take the bookmark number and read that number of lines in playlist.dat.
	* From that position it will create a list of the next 9 episode ( if reach the end, loop over).
	* Random episode mode as also been added.
	* Variable playlist size based on time of day.
		* Shorter playlist during night time.
		* Longer playlist during day time.
	* Shutdown time dependent on playlist size.
	* Random-First-Fit Scheduling for minimal overlapping between playlists

# Instruction:
	* Simply put content of file in ~.kodi/userdata/
