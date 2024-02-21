import keyboard as kb
import random
import json
from time import time, sleep
from threading import Thread
from colorama import Fore


def update_leaderboard(file_path, username, wpm):
    file_path = 'scorecard.json'
    try:
        with open(file_path, 'r') as f:
            leaderboard = json.load(f)
    except FileNotFoundError:
        leaderboard = {}

    if username in leaderboard:
        leaderboard[username]['wpm'] = max(leaderboard[username]['wpm'], wpm)
    else:
        leaderboard[username] = {'wpm': wpm}

    with open(file_path, 'w') as f:
        json.dump(leaderboard, f, indent=4)
