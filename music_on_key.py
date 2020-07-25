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
PLAY_KEY = "`"
FOUND_MUSIC = []
MAX_VOLUME = 20  # from 0 to 100

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


def play_music():
    pygame.mixer.music.set_volume(0)
    pygame.mixer.music.play()
    for i in range(0, MAX_VOLUME):
        pygame.mixer.music.set_volume(i / 100)
        sleep(0.04)


next_melody = load_music()


while True:
    if keyboard.is_pressed(PLAY_KEY) and not PLAYING:
        PLAYING = True
        print(f"Playing: {next_melody}")
        play_music()

        while keyboard.is_pressed(PLAY_KEY):
            continue

    elif keyboard.is_pressed(PLAY_KEY) and PLAYING:
        PLAYING = False
        print("Stopping")

        pygame.mixer.music.fadeout(3000)
        sleep(3)

        next_melody = load_music()

        while keyboard.is_pressed(PLAY_KEY):
            continue

    elif PLAYING and not pygame.mixer.music.get_busy():
        next_melody = load_music()
        print(f"Playing: {next_melody}")
        play_music()

    clock.tick(60)
