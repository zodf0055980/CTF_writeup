#!/usr/bin/env python3
import sys
import random
import signal

class TimeoutError(Exception):
    pass

def handler(signum, frame):
    raise TimeoutError

def go():
    current = random.randint(0,2)
    play = ["rock","paper","scissors"]
    hint = ['!','?',':']

    print("Let's play a game" + hint[current])

    for i in range(100):
        print('=' * 30)
        print("Round {}:".format(i))
        choice = input("rock, paper, or scissors ( choose one of them ): ").strip()
        if choice == "rock": choice = 0
        elif choice == "paper": choice = 1
        elif choice == "scissors": choice = 2
        else:
            print("I don't know what that is, bye...")
            sys.exit(1)
        if choice == ((current + 1) % 3): print("You Win!!")
        else:
            print("You Lose...")
            sys.exit(1)
        current = (current + 1) % 3

signal.signal(signal.SIGALRM, handler)
signal.alarm(20)

try:
    go()
except TimeoutError:
    print("\nTimes up, bye...")
    sys.exit(1)

with open('/home/ctf/flag') as data:
    print(data.read())
