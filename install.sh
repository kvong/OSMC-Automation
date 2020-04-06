sudo apt-get -y update
cp -r ./Automation.dat ~/.kodi/userdata/
cat ./autoexec.py > ~/.kodi/userdata/autoexec.py
sudo apt install -y vim python-numpy
git clone https://github.com/FFmpeg/FFmpeg.git ~/ffmpeg
cd ~/ffmpeg/
./configure
make
sudo make install
