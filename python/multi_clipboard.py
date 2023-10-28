#!/usr/bin/env python3
"""
    Author: Pek, Jonetta
    Date: 5 October 2023
    Purpose: Program to save and load data to and from json file
"""

import sys
import clipboard
import json


FILE = 'clipboard.json'


def get_command() -> str:
    if len(sys.argv) == 2:
        return sys.argv[1]
    else:
         print('Please enter exactly one command.')


def save_to_file(filename: str, data: dict) -> None:
    with open(filename, 'w') as f:
        json.dump(data, f)


def load_data(filename: str) -> dict:
    try:
        with open(filename,'r') as f:
            return json.load(f)
    except:
        return {}


def save(data: dict) -> None:
    key = input('Please enter a key:\n>>>')
    data[key] = clipboard.paste()
    save_to_file(FILE, data)
    print('Saved data!')


def load(data: dict) -> None:
    key = input('Please enter a key:\n>>>')
    if key in data.keys():
        print(data.get(key))
    else:
        print(f'Key "{key}" not found.')


def main():
    command = get_command().lower()
    data = load_data(FILE)
    if command == 'save':
        save(data)
    elif command == 'load':
        load(data)
    elif command == 'list':
        print(data)
    else:
        print('Please enter a valid command')


if __name__ == '__main__':
    main()
    