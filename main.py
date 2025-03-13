import os

def play_sound(sound_file):
    os.system(f'cvlc --play-and-exit "{sound_file}"')

play_sound("Oktave 1/sound_okatve1_C.mp3")
