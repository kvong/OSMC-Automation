echo "Install script should be executed in the '/home/osmc/OSMC-Automation/' directory. Do you wish to continue? [y/n]"

read choice

if [ $choice == 'y' ] || [ $choice == 'Y' ] || [ $choice == 'yes' ] || [ $choice == 'YES' ] 
then
    echo Updating repos...
    sudo apt-get -y update
    echo Copying over Automation.dat...
    cp -r ./Automation.dat ~/.kodi/userdata/
    echo Copying over autoexec.py...
    cat ./autoexec.py > ~/.kodi/userdata/autoexec.py
    echo Updating .bashrc...
    cat ./alias >> ~/.bashrc
    echo Installing prerequisites...
    sudo apt install -y vim python-numpy build-essential pkg-config
    echo Creating FFmpeg...
    git clone https://github.com/FFmpeg/FFmpeg.git ~/ffmpeg
    cd ~/ffmpeg/
    ./configure
    make
    sudo make install
    echo OSMC-Automation completed. Rebooting in 5 seconds.
    sleep 5s
    reboot
fi
