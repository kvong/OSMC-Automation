### Description:
Automatically play and turn off background tv show with RPi. (Great for people who sleeps with the tv on.)

### Prerequisite:
- Raspberry PI with OSMC installed.
	- Guide for Windows [here](https://flixed.io/install-osmc-raspberry-pi/)
- SHOWNAME_bookmark.dat ( contain the index of the last episode played by osmc )
- SHOWNAME_episodelist.dat ( contain the names of all the video files in a list)
- SHOWNAME_mem.dat ( contain data for RRF scheduling )
- currentplaylist.dat
- Video files (must be playable by kodi)
- Python2 NumPy
- ffmpeg to get video durations.

### Install:
- Instruction to [login](https://osmc.tv/wiki/general/accessing-the-command-line/)
	- Note: It's better to install locally than over SSH as this may take a while.
	1. Clone this repository to `$HOME` which should be `/home/osmc/`.
	2. Run installation script:
		```
		cd OSMC-Automation
		./install.sh
		```
	
### Features:
- Python script will take the bookmark number and read that number of lines in playlist.dat.
- From that position it will create a list of the next 9 episode ( if reach the end, loop over).
- Random episode mode as also been added.
- Variable playlist size based on time of day.
	- Shorter playlist during night time.
	- Longer playlist during day time.
- Shutdown time dependent on playlist size and total episodes duration.
- Random-First-Fit Scheduling for minimal overlapping between playlists.
	- Record episodes as it is played instead of all at once.
