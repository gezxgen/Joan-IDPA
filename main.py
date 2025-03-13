import subprocess

def play_sound(sound_file):
    # mpg123 für MP3-Dateien verwenden
    subprocess.run(["mpg123", sound_file])

play_sound("Oktave 1/sound_okatve1_C.mp3")
