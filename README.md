# rockingMotorcycle
An accelerometer triggered sound and light generator for rocking motorcycles. Developed with python and a raspberry pi zero

## Todo

- ~~Add button that changes the volume on a single press and restarts the app on a long press~~
- Add a led strip that has at least two modes:
  - Idle mode: Fading in and out 
  - LED chase where the speed can be changed
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
## Install libs
- sudo apt-get install python3-rpi.gpio -y
