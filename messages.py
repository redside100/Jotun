import os
import yaml

data = {}


def init():
    # Create if it doesn't exist
    if not os.path.exists("files/messages.yaml"):
        f = open('files/messages.yaml', 'w')
        f.close()

    # Read messages, load into dict
    with open('files/messages.yaml', 'r+') as message_file:
        global data
        data = yaml.safe_load(message_file)


def reload():
    # Reload messages
    with open('files/messages.yaml', 'r+') as message_file:
        global data
        data = yaml.safe_load(message_file)
