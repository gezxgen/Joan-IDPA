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
        # Use cvlc (command-line VLC) with options to hide interface and exit after playback
        subprocess.Popen(['cvlc', '--play-and-exit', '--no-video', '--quiet', sound_file], 
                        stdout=subprocess.DEVNULL, 
                        stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"Error playing sound: {e}")

# Initialize lgpio and open the chip
try:
    h = lgpio.gpiochip_open(0)  # Open GPIO chip 0 (Raspberry Pi's main GPIO chip)
    print("LGPIO initialized successfully")
except Exception as e:
    print(f"LGPIO initialization error: {e}")
    print("Make sure lgpio is installed: sudo apt install python3-lgpio")
    print("Make sure you're running with sudo")
    sys.exit(1)

# Current octave
current_octave = 1

# Store previous GPIO states to detect changes
previous_states = {}

# Setup GPIO pins as inputs with pull-down resistors
try:
    print("Setting up GPIO pins...")
    # Set up all pins and track their initial states
    all_pins = list(NOTE_PINS.keys()) + list(OCTAVE_PINS.keys())
    for pin in all_pins:
        try:
            # Set up as input with pull-down
            lgpio.gpio_claim_input(h, pin, lgpio.SET_PULL_DOWN)
            # Store initial state
            previous_states[pin] = lgpio.gpio_read(h, pin)
            # Print setup info
            if pin in NOTE_PINS:
                print(f"  Set up note pin GPIO {pin} ({NOTE_PINS[pin]})")
            else:
                print(f"  Set up octave pin GPIO {pin} (Octave {OCTAVE_PINS[pin]})")
        except Exception as e:
            print(f"  Error setting up GPIO {pin}: {e}")
except Exception as e:
    print(f"Error setting up GPIO: {e}")
    lgpio.gpiochip_close(h)
    sys.exit(1)

# Main program
print("\n--- LGPIO Piano Program ---")
print("Press GPIO buttons to play notes")
print("Current octave: 1")
print("Press Ctrl+C to exit")

# Play a sound at startup to indicate the program is ready
print("Playing startup sound...")
startup_sound = "Oktave 1/sound_okatve1_C.mp3"
play_sound(startup_sound)
time.sleep(1)  # Give a moment for the sound to play

try:
    # Keep the program running
    while True:
        # Check all pins for state changes
        for pin in all_pins:
            try:
                current_state = lgpio.gpio_read(h, pin)
                # Check for rising edge (0 to 1)
                if current_state == 1 and previous_states[pin] == 0:
                    if pin in NOTE_PINS:
                        note = NOTE_PINS[pin]
                        print(f"NOTE PRESSED: {note} (GPIO {pin})")
                        sound_file = f"Oktave {current_octave}/sound_okatve{current_octave}_{note}.mp3"
                        print(f"Playing: {sound_file}")
                        play_sound(sound_file)
                    elif pin in OCTAVE_PINS:
                        current_octave = OCTAVE_PINS[pin]
                        print(f"OCTAVE CHANGED: Now using Octave {current_octave} (GPIO {pin})")
                # Update previous state
                previous_states[pin] = current_state
            except Exception as e:
                print(f"Error reading GPIO {pin}: {e}")
                # Prevent repeated error messages
                time.sleep(1)
        # Short delay to avoid high CPU usage
        time.sleep(0.01)
except KeyboardInterrupt:
    print("\nProgram exited")
finally:
    # Clean up LGPIO on exit
    lgpio.gpiochip_close(h)
    print("GPIO cleaned up")
