import pygame
import os


def play_sound(sound_file):
    try:
        # Initialize pygame mixer
        pygame.mixer.init()

        # Check if file exists
        if not os.path.exists(sound_file):
            print(f"Error: File '{sound_file}' not found")
            return False

        # Load and play the sound
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()

        # Wait for the sound to finish playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    except Exception as e:
        print(f"Error playing sound: {str(e)}")
        return False
    finally:
        pygame.mixer.quit()

    return True


if __name__ == "__main__":
    sound_file = "sound1.mp3"
    play_sound(sound_file)
