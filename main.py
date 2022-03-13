# !/usr/bin/env python3
##
from omxplayer.player import OMXPlayer
from pathlib import Path
from time import sleep
import serial
import time
import os, signal
import keyboard


import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)  # Ignore warning for now
GPIO.setmode(GPIO.BCM)  # Use physical pin numbering
playButton = 23
GPIO.setup(playButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def processKill():
    # Ask user for the name of process
    name = 'omxplayer'
    try:

        # iterating through each instance of the process
        for line in os.popen("ps ax | grep " + name + " | grep -v grep"):
            fields = line.split()

            # extracting Process ID from the output
            pid = fields[0]

            # terminating process
            os.kill(int(pid), signal.SIGKILL)
        print("Process Successfully terminated")

    except:
        print("Error Encountered while running script")
        pass

#kill omx process
processKill()

defaultVideoPath = "/home/pi/video/video.mp4"  # Change this path with default video path that needs to be played in loop

specificPath = "/home/pi/video/video2.mp4"  # Change this path with specific video path that needs to be played with motion detection

#start loop play
player = OMXPlayer(defaultVideoPath, args=['--loop', '-o', 'local','--layer','1'])

specificPlay = False  # This flag will check if specific video is playing

while True:
    if (not GPIO.input(playButton)):
        print("Button Pressed")
        while (not GPIO.input(playButton)):  # wait for button release
            pass
        player.pause()
        playerAfterPress = OMXPlayer(specificPath, args=['-o', 'local', '--layer', '2'])
        playDuration = playerAfterPress.duration()  # Store duration of playing special file
        print("",playDuration)
        #wait the end of video
        time.sleep(playDuration)
        player.play()
        playerAfterPress.quit()
