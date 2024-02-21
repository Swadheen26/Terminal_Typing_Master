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
        
def show_leaderboard(file_path):
    file_path = 'scorecard.json'
    try:
        with open(file_path, 'r') as f:
            leaderboard = json.load(f)
    except FileNotFoundError:
        leaderboard = {}

    sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: x[1]['wpm'], reverse=True)

    print("\nLeaderboard:")
    print("Name\t\tWPM")
    for idx, (name, stats) in enumerate(sorted_leaderboard[:5], start=1):
        print(f"{idx}. {name}\t\t{stats['wpm']:.2f}")

    return leaderboard

def showLeaderBoard():
    global jsondata
    sleep(2)
    print()
    print(Fore.GREEN+'NAME\t\tWORDS\t\tTIME(sec)\tWPM'+Fore.RESET)
    print(Fore.RED+'='*60+Fore.RESET)

    sorted_list = sorted(jsondata, key=lambda key: jsondata[key]['wpm'], reverse=True)

    for key in sorted_list:
        print('{}\t\t{}\t\t{}\t\t{}'.format(jsondata[key]['name'], jsondata[key]['words'], jsondata[key]['time'], jsondata[key]['wpm']))
    
    # Display the leaderboard
    show_leaderboard('scorecard.json')
