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

def monitorForQuit(p1):
    global end_flag
    while True:
        if kb.is_pressed('ctrl+q'):
            # print('User tried to quit')
            end_flag = 1
            break
    p1.end_time = time()
    p1.playtime = int(p1.end_time - p1.start_time)
    p1.wpm = p1.words * 60 // p1.playtime

    # Write the necessary data of current player to jsondata.
    jsondata["P" + str(players)]['name'] = p1.name
    jsondata["P" + str(players)]['words'] = p1.words
    jsondata["P" + str(players)]['time'] = p1.playtime
    jsondata["P" + str(players)]['wpm'] = p1.wpm

    # Update the leaderboard
    update_leaderboard('scorecard.json', p1.name, p1.wpm)

    showLeaderBoard()

    print('\nHIT ENTER')

def getUserInput(p1):
    global end_flag
    print('Start typing the paragraph shown to you. Press Ctrl+Q to exit')
    p1.start_time = time()
    
    while True:
        if end_flag == 1:
            print('Your turn finished !!')
            break

        # Display the paragraph to the user.
        current_sentence = random.choice(content).strip()
        print()
        print(Fore.BLUE + current_sentence + Fore.RESET)

        # Get the user input.
        user_inp = input()

        current_sentence_words = current_sentence.split()
        user_typed_words = user_inp.split()

        for user_given in user_typed_words:
            if user_given in current_sentence_words:
                p1.words += 1

        print()

class Player:
    def __init__(self, name):
        self.name = name
        self.words = 0
        self.start_time = 0
        self.end_time = 0
        self.wpm = 0

game_run = 1
para_g = open('Source_file.txt', 'r')
content = para_g.readlines()

try:
    fr = open('scorecard.json', 'r')
    jsondata = json.loads(fr.read())
except FileNotFoundError:
    fr = open('scorecard.json', 'w+')
    fr.write("{}")
    fr.seek(0)
    jsondata = json.loads(fr.read())

players = len(jsondata)
fr.close()

while game_run:

    end_flag = 0

    player = input(Fore.MAGENTA + 'ENTER YOUR NAME : ' + Fore.RESET)          
    p1 = Player(player)                       
    
    players += 1                                
    jsondata['P' + str(players)] = {}                

    t1 = Thread(target=getUserInput, args=(p1,))
    t1.start()

    t2 = Thread(target=monitorForQuit, args=(p1,))
    t2.start()

    t1.join()
    t2.join()

    input('\nPress ENTER to see the results')

    print()
    print(Fore.YELLOW + '1. Play another game')
    print('2. Quit game')
    option = input('Enter your option : ' + Fore.RESET)

    if option == '2':
        game_run = 0
    elif option == '1':
        pass
    else:
        print('You have entered an invalid option.')
        print('Game will end')
        break
    print()

para_g.close()

fsw = open('scorecard.json', 'w')                    
json.dump(jsondata, fsw, indent=4)
fsw.close()

print('Data saved successfully.')
