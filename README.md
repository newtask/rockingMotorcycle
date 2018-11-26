# rockingMotorcycle
An accelerometer triggered sound and light generator for rocking motorcycles. Developed with python and a raspberry pi zero

## Todo

- ~~Add button that changes the volume on a single press and restarts the app on a long press~~
- ~~Add a led strip that has at least two modes~~:
  - ~~Idle mode: Fading in and out~~
  - ~~LED chase where the speed can be changed~~
- ~~Add a status led which display the status of the app and gives feedback when pressing the button~~
- Add a audio system that can play audio files in a loop and switch to another track immediately
- Combine everything in a game with the following gameplay


| Mode  | Audio |  LED | Trigger |
| ------------- | ------------- | ------------- | ------------- |
| STARTING  | Motorcycle starts engine  |  Bright flash |  when app starts |
| IDLE  | Motorcycle is neutral gear  | slow fading | after STARTING or BREAKING mode| 
| ACCELERATE| Motorcycle is geeting more speed | LED chase is starting  and getting faster |Accelerometer detects movement | 
| RUNNING | Motorcycle is driving | LED chase at high speed | Accelerometer continues detecting movement |
| DEACCELERATE | Motorcycle is slowing down | LED chase is slowing down | Accelerometer does detect less movement |

# How to install rockingMototcycle
Check if you have python3 installed

# links
https://www.stuffaboutcode.com/2012/06/raspberry-pi-run-program-at-start-up.html
https://raspberrypi.stackexchange.com/questions/37920/how-do-i-set-up-networking-wifi-static-ip-address/74428#74428

# Install guide
## Setup pi
1. Flash a new raspbian lite
2. Before putting the sdcard into the raspi, create a empty file "ssh"
3. Create a new file "wpa_supplicant.conf" with the wifi settings:
    - ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
network={
    ssid=""
    psk=""
    key_mgmt=WPA-PSK
}

## Install Adafruit_Python_GPIO
- sudo apt-get update
- sudo apt-get install build-essential python3-pip python3-dev python-smbus python3-setuptools git -y
- git clone https://github.com/adafruit/Adafruit_Python_GPIO.git
- cd Adafruit_Python_GPIO
- sudo python3 setup.py install
- Activate the i2c bus with the raspi-config tool:
    - sudo raspi-config
    - select Interfacing Options
    - Select I2C
    - Select yes and ok 
- check imu address:
    - sudo i2cdetect -y 1
	
# Install Lib for alternative 6dof sensor lsm303d
- sudo pip3 install lsm303d
    
# Install NeoPixel
- cd ~
- sudo apt-get install gcc make scons swig -y
- git clone https://github.com/jgarff/rpi_ws281x
- cd rpi_ws281x/
- sudo scons
- cd python
- sudo pip3 install rpi_ws281x
- sudo python3 setup.py build
- sudo python3 setup.py install



## Installation of Wiring pi
- cd ~
- git clone git://git.drogon.net/wiringPi
- cd wiringPi
- ./build

- Test Wiring pi
    - gpio -v
    - gpio readall
- cd ~/rockingMotorcycle
- gcc -o gpio_alt gpio_alt.c
- sudo chown root:root gpio_alt
- sudo chmod u+s gpio_alt
- sudo mv gpio_alt /usr/local/bin/
- enable audio on rapsi:
    - sudo raspi-config
        - Advanced options
        - Audio
        - Force 3.5mm (Headphone)
        - Finish
    - test audio:
        - aplay audio/h_start.wav
        - set audio volume via alsamixer
- set gpio alt automatically:
	- sudo chmod +x /home/pi/rockingMotorcycle/pcmaudio.sh
	- sudo cp /home/pi/rockingMotorcycle/pwmaudio.service  /lib/systemd/system/pwmaudio.service
	- sudo systemctl enable pwmaudio.service
	- sudo systemctl start pwmaudio.service
	
# Install pygame
- sudo python3 -m pip install -U pygame --user
- sudo apt-get install libsdl1.2debian libasound2-dev libsdl-mixer1.2 python-alsaaudio -y
- cd ~
- git clone https://github.com/larsimmisch/pyalsaaudio.git
- cd pyalsaaudio/
- sudo python3 setup.py build 
- sudo python3 setup.py install

# install rocking game 
- sudo apt-get install python3-rpi.gpio daemon -y   
- sudo cp /home/pi/rockingMotorcycle/rockinggame /etc/init.d/rockinggame
- sudo chmod 755 /etc/init.d/rockinggame
- sudo update-rc.d rockinggame defaults