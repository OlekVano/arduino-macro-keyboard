import serial
import time
import json
import os
import pyperclip
import pyautogui

def get_settings():
    try:
        with open('./settings.json', 'r') as f:
            settings = json.load(f)
        return settings
    except:
        raise Exception('Could not get the settings from the "settings.json" file')


def connect(port, rate):
    for _ in range(10):
        try:
            arduino = serial.Serial(port=port, baudrate=rate, timeout=0.1)
            return arduino
        except:
            time.sleep(0.5)

    raise Exception(f'Could not connect to the arduino at port {port}')

def get_shortcuts(folder):
    shortcuts = {}
    try:
        for filename in os.listdir(folder):
            if filename[-4:] != '.txt':
                continue
            with open(f'{folder}/{filename}', 'r', encoding='utf8') as f:
                shortcuts[filename[:-4]] = f.read()
                
        return shortcuts
    except:
        raise Exception(f'Could not get the shortcuts from the {folder} folder')

settings = get_settings()
arduino = connect(settings['port'], settings['rate'])
shortcuts = get_shortcuts(settings['folder'])

while True:
    read = arduino.read().decode('utf-8')

    if read == '':
        continue
    if read not in shortcuts.keys():
        continue

    pyperclip.copy(shortcuts[read])
    pyautogui.hotkey('ctrl', 'v')