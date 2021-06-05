echo "Install script should be executed in the '/home/osmc/OSMC-Automation/' directory. Do you wish to continue? [y/n]"

read choice

if [ $choice == 'y' ] || [ $choice == 'Y' ] || [ $choice == 'yes' ] || [ $choice == 'YES' ] 
then
    echo Updating repos...
    sudo apt-get -y update
    echo Installing nvm
    curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.11/install.sh | bash && nvm install stable
    echo Copying over node server
    cp -r ./node-server ~/
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
    cd ~/node-server/
    npm install
    cd
    echo OSMC-Automation completed. Reboot to see changes.
    echo Remember auto start the node server from /etc/rc.local
fi
