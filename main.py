#!/usr/bin/env python3

from random import randrange, randint
from time import sleep
from datetime import datetime, timedelta
import json
import os
import pygame

''' Simple Random Reward applied after a day of programming.
2 by default, + (0-5) randrange or 5% chance to get a jackpot of 10'''

# Get absolute directory of config file for Linux .desktop app, and sounds
# Shebang (what a funny word) on top DOES tell terminal which language to use

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, 'config.json')
SOUNDS_DIR = os.path.join(BASE_DIR, 'sounds')
pygame.mixer.init()

RANGE = (2,8)
CHANCE_OF_JACKPOT = 5 #percent
JACKPOT_AMOUNT = 10 #euro



def check_win_amount(win_amount: int):
    '''Takes hold of win amount and returns appropriate sound'''

    # Check if weel is spun already
    if win_amount == 0:
        filename = 'huh.wav'

    # Check JACKPOT
    elif win_amount == 10:
        filename = 'jackpot.wav'
    else:

        if win_amount <= 4:
            filename = 'fart.wav'
        elif 5 <=win_amount <= 6:
            filename = 'little_win.wav'
        else:
            filename = 'medium_win.wav'

    play_sound(filename)


def play_sound(filename: str):
    '''Plays .wav sound by filename passed by check_win_amount'''

    filepath = os.path.join(SOUNDS_DIR, filename)

    if not os.path.isfile(filepath):
        print(f'[Sound Error] No file named {filename} in the directory {filepath}')
        return False

    try:
        sound = pygame.mixer.Sound(filepath)
        sound.play()
        pygame.time.wait(int(sound.get_length() * 1000))

    except Exception as e:
               print(f"[Sound Error] Could not play '{filename}': {e}")




def check_streak(data):
    '''Handles counting and updating of a sreak'''
    today = datetime.today().date()
    last_spin_date = datetime.strptime(data['last_spin_date'], "%Y-%m-%d").date()

    if last_spin_date != today:
        data['is_spinned'] = False

    if last_spin_date == today:
        print("You've spun it already. Chill. Come back tomorrow.")
        check_win_amount(0)
        return False

    elif last_spin_date == today - timedelta(days=1):
        data['streak'] += 1
        print('Streak continued.')

    else:
        data['streak'] = 1
        print('Streak set to one day, boah. GO ON baby.')

    if data['streak'] > data['biggest_streak']:
        data['biggest_streak'] = data['streak']

    data['last_spin_date'] = str(today)
    data['is_spinned'] = True
    return True


def load_data():
    '''Reads json, coverts strng into suitable types. Adds missing keys if needed.'''

    with open(CONFIG_PATH, 'r') as file:
        data = json.load(file)

        data.setdefault('is_spinned', False)
        data.setdefault('streak', 0)
        data.setdefault('last_jackpot_date', "1970-01-01")
        data.setdefault('jackpot_counter', 0)
        data.setdefault('total_money_won', 0)
        data.setdefault('biggest_streak', 0)

        return data

def save_data(data):
    '''Dump config to JSON. JSON handles the types.'''
    with open(CONFIG_PATH, 'w') as file:
        json.dump(data, file, indent=2)

def random_reward():
    data = load_data()

    if not check_streak(data):
        return

    jackpot = randint(1,100)

    if jackpot <= CHANCE_OF_JACKPOT:
        print(f'Today is your lucky day, go grab a {JACKPOT_AMOUNT} euro reward.')
        result = JACKPOT_AMOUNT
    else:
        result = randrange(*RANGE)
        print(f'Today you have got {result} euro. Keep doin watcha doin.')

    data['total_money_won'] += result

    check_win_amount(result)
    save_data(data)

if __name__ == '__main__':
    for _ in range(5):
        print('.', end='', flush=True)
        sleep(0.4)
    print()
random_reward()

data = load_data()
print(f'Current streak: {data['streak']} day, yeeeehaaaaw.')
