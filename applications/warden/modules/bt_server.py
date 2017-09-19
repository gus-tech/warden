#!/usr/bin/env python

import json
import pygame
import thread
import time
import websocket
import setproctitle


def get_axes(joystick):
    axes = []
    for x in range(joystick.get_numaxes()): axes.append(joystick.get_axis(x))
    return axes

def get_buttons(joystick):
    buttons = []
    for x in range(joystick.get_numbuttons()): buttons.append(joystick.get_button(x))
    return buttons

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    print("Bluetooth controller connected!")
    

input = {}
last = {}
connected = False
joystick = None

# WebSocket stuff
ws_host = "localhost"
ws_port = 8888
ws_group = "warden"
ws_token = "123456789"
ws_name = "users" #auth.user.username.split("@")[0]
ws_connection_string = "ws://{0}:{1}/realtime/{2}/{3}/{4}".format(ws_host, ws_port, ws_group, ws_token, ws_name)

def get_input(joystick):
    input['axes'] = get_axes(joystick)
    input['velocity_left'] = input['axes'][3]
    input['velocity_right'] = input['axes'][1]
    input['horn'] = (input['axes'][5]+1)/2
    
def set_last_input():
    last['axes'] = input['axes']
    last['velocity_left'] = input['velocity_left']
    last['velocity_right'] = input['velocity_right']
    last['horn'] = input['horn']
    
def reset_last_input():
    last['axes'] = None
    last['velocity_left'] = None
    last['velocity_right'] = None
    last['horn'] = None
    

def wait_for_joystick():
    connected = False
    while not connected: 
        try:
            pygame.joystick.init()
            joystick_count = pygame.joystick.get_count()
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            connected = True
        except: pass
    return joystick
   
def setup_websocket():
    websocket.enableTrace(True)
    ws = websocket.create_connection(ws_connection_string,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    return ws
    
def main():
    
    connected = False
    setproctitle.setproctitle("warden_bt_joystick")
    
    pygame.init()
    ws = setup_websocket()
    ws.send("test")
    joystick = wait_for_joystick()
    get_input(joystick)
    reset_last_input()
    print("Bluetooth controller connected!")
    while True:
        pygame.event.get()
        
        # Get input
        get_input(joystick)
        
        if input['velocity_left'] != last['velocity_left'] or input['velocity_right'] != last['velocity_right']:
                ws.send(json.dumps({'left': input['velocity_left'], 'right': input['velocity_right']}))
                print("{0}, {1}".format(input['velocity_left'], input['velocity_right']))
            
    
        # Track last input
        set_last_input()
        

if __name__ == "__main__":
    main()
