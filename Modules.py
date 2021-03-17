import os.path
from os import path
import socket
import os


def test_connection():
    try:
        socket.create_connection(("Google.com", 80))
        return True
    except OSError:
        return False


def shift():
    os.system('cls' if os.name == 'nt' else 'clear')


def get_input(str_data):
    return input(str_data + ": ")


def get_number(str_data):
    while True:
        num = input("Please enter " + str_data + ": ")
        try:
            val = int(num)
            if val >= 0:
                break
            else:
                print("Must be positive.")
        except ValueError:
            print("This is not a number. Please enter a valid number.")
    return val


def set_dir(directory):
    if not path.exists(directory):
        os.makedirs(directory)
