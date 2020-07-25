import os
import random
import sys
from time import sleep

import keyboard
import pygame
from mutagen.mp3 import MP3

# pygame's feature for managing games fps and reducing CPU usage
clock = pygame.time.Clock()

# constants
MUSIC_FOLDER = sys.argv[1] if len(sys.argv) > 1 else 'music_on_key'
PLAYING = False
PLAY_KEY = "dot"
FOUND_MUSIC = []

# scan for music
for folder, children, files in os.walk(MUSIC_FOLDER):
    music_files = [os.path.join(os.getcwd(), folder, file) for file in files if "mp3" in file]
    FOUND_MUSIC.extend(music_files)


# pick random music
def load_music():
    picked_melody = random.choice(FOUND_MUSIC)
    audio = MP3(picked_melody)
    pygame.mixer.quit()
    pygame.mixer.init(frequency=audio.info.sample_rate, allowedchanges=0)
    pygame.mixer.music.load(picked_melody)
    return picked_melody


next_melody = load_music()


while True:
    if keyboard.is_pressed(PLAY_KEY) and not PLAYING:
        print(f"Playing: {next_melody}")
        PLAYING = True

        pygame.mixer.music.set_volume(0)
        pygame.mixer.music.play()
        for i in range(0, 50):
            pygame.mixer.music.set_volume(i/100)
            sleep(0.04)

        while keyboard.is_pressed(PLAY_KEY):
            continue

    elif keyboard.is_pressed(PLAY_KEY) and PLAYING:
        print("Stopping")
        PLAYING = False

        pygame.mixer.music.fadeout(4000)
        sleep(4)

        next_melody = load_music()

        while keyboard.is_pressed(PLAY_KEY):
            continue

    clock.tick(60)
