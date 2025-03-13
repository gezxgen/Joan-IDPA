#!/usr/bin/env python3
import lgpio
import time
import sys
import os
import subprocess

# Define GPIO pins for notes
NOTE_PINS = {
    22: "Bb",  # Corrected - GPIO 22 is Bb
    23: "B",   # Corrected - GPIO 23 is B
    24: "A",
    10: "Ab",
    9: "G",
    25: "Gb",
    11: "F",
    8: "E",
    7: "Eb",
    0: "D",
    1: "Db",
    5: "C"
}

# Define GPIO pins for octaves
OCTAVE_PINS = {
    19: 1,  # GPIO 19 for Octave 1 (updated)
    26: 2,  # GPIO 26 for Octave 2 (updated)
    4: 3,   # GPIO 4 for Octave 3
    14: 4,  # GPIO 14 for Octave 4
    15: 5,  # GPIO 15 for Octave 5
    17: 6,  # GPIO 17 for Octave 6
    18: 7   # GPIO 18 for Octave 7
}

# Function to play sound using VLC
def play_sound(sound_file):
    try:
        subprocess.Popen(['cvlc', '--play-and-exit', '--no-video', '--quiet', sound_file], 
                        stdout=subprocess.DEVNULL, 
                        stderr=subprocess.DEVNULL)
    except Exception:
        pass

# Initialize lgpio and open the chip
try:
    h = lgpio.gpiochip_open(0)
except Exception:
    sys.exit(1)

# Current octave
current_octave = 1

# Store previous GPIO states to detect changes
previous_states = {}

# Setup GPIO pins as inputs with pull-down resistors
try:
    all_pins = list(NOTE_PINS.keys()) + list(OCTAVE_PINS.keys())
    for pin in all_pins:
        try:
            lgpio.gpio_claim_input(h, pin, lgpio.SET_PULL_DOWN)
            previous_states[pin] = lgpio.gpio_read(h, pin)
        except Exception:
            pass
except Exception:
    lgpio.gpiochip_close(h)
    sys.exit(1)

# Play a sound at startup to indicate the program is ready
startup_sound = "Oktave 1/sound_okatve1_C.mp3"
play_sound(startup_sound)
time.sleep(1)

try:
    while True:
        for pin in all_pins:
            try:
                current_state = lgpio.gpio_read(h, pin)
                if current_state == 1 and previous_states[pin] == 0:
                    if pin in NOTE_PINS:
                        note = NOTE_PINS[pin]
                        sound_file = f"Oktave {current_octave}/sound_okatve{current_octave}_{note}.mp3"
                        play_sound(sound_file)
                    elif pin in OCTAVE_PINS:
                        current_octave = OCTAVE_PINS[pin]
                previous_states[pin] = current_state
            except Exception:
                time.sleep(1)
        time.sleep(0.01)
except KeyboardInterrupt:
    pass
finally:
    lgpio.gpiochip_close(h)
