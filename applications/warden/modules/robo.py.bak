#!/usr/bin/env python
# -*- coding: utf-8 -*-
#from gluon import *

#!/usr/bin/env python


import pygame
import time
import sys
import os
from RoboClaw import Roboclaw


# Import SPI library (for hardware SPI) and MCP3008 library.
#import CHIP_IO.GPIO as GPIO
#import Adafruit_GPIO.SPI as SPI
#import Adafruit_PCA9685


def get_axes(joystick):
    axes = []
    for x in range(joystick.get_numaxes()): axes.append(joystick.get_axis(x))
    return axes


def get_buttons(joystick):
    buttons = []
    for x in range(joystick.get_numbuttons()): buttons.append(joystick.get_button(x))
    return buttons


def main():
    # setup pygame to run headlessly
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    pygame.display.set_mode((1,1))
    
    #GPIO.cleanup()
    #GPIO.setup("CSID0", GPIO.OUT)
    #GPIO.output("CSID0", GPIO.HIGH)
    
    stdout = sys.__stdout__
    stderr = sys.__stderr__
    print("start")
    
    
    address = 0x80
    accel = 1
    
    for x in range(0,3):
        try:
            rc = Roboclaw("/dev/ttyACM"+str(x),115200)
            rc.Open()
            rc.DutyAccelM1M2(address, accel, 0, accel, 0)
            break
        except: time.sleep(0.1)
    
    bat_v = 0
    bat_v_last = 0
    
    try:
        pygame.joystick.init()
        joystick_count = pygame.joystick.get_count()
        if joystick_count < 1: sys.exit()
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
    except: sys.exit()

    velocity_left = 0.0
    velocity_right = 0.0
    velocity_left_last = 0.0
    velocity_right_last = 0.0
    moved = False
    #i = 0
    while True:
        #i += 1
        #sys.stdout = open(os.devnull,'w')
        #sys.stderr = open(os.devnull,'w')
        pygame.event.get()
        # Get input
        axes = get_axes(joystick)
        velocity_left = axes[3]
        velocity_right = axes[1]
        
        if abs(velocity_left) < 0.01: velocity_left = 0.0;
        if abs(velocity_right) < 0.01: velocity_right = 0.0;
        #horn = (axes[5]+1)/2
        if velocity_left != velocity_left_last or velocity_right != velocity_right_last:
            rc.DutyAccelM1M2(address, accel, velocity_left, accel, velocity_right)
            moved = True
            
        if moved == False and velocity_left == 0.0 and velocity_right == 0.0:    
            try:
                bat_v = rc.ReadMainBatteryVoltage(address)
                print(bat_v[1])
                f = open('voltage', 'w')
                f.write(str(bat_v[1]))
                f.close()
            except: pass
            
        velocity_left_last = velocity_left
        velocity_right_last = velocity_right
        
        #sys.stdout = stdout
        #sys.stderr = stderr
        """
        if i >= 1000:
            i = 0
            if velocity_left == 0.0 and velocity_right == 0.0: 
                bat_v = rc.ReadMainBatteryVoltage(address)
                if bat_v_last != bat_v[1]: print(bat_v[1])
                bat_v_last = bat_v[1]
                f = open('voltage', 'w')
                f.write(str(bat_v[1]))
                f.close()
        """
        time.sleep(0.01)


if __name__ == "__main__":

    main()
