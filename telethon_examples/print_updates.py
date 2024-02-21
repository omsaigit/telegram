#!/usr/bin/env python3
# A simple script to print all updates received.
# Import modules to access environment, sleep, write to stderr
import os
import sys
import time ,json
import re
from kite_trade import *
from api import *
from datetime import datetime
# current_directory = os.getcwd()
# Print the current working directory
# print("Current working directory:", current_directory)
with open('/Users/anunaya/Downloads/Telethon-1/telethon_examples/config.json') as ff:
    dataf = json.load(ff)
kite = KiteApp(enctoken=dataf["EV5068"])

# Import the client
from telethon import TelegramClient


# This is a helper method to access environment variables or
# prompt the user to type them in the terminal if missing.
def get_env(name, message, cast=str):
    if name in os.environ:
        return os.environ[name]
    while True:
        value = input(message)
        try:
            return cast(value)
        except ValueError as e:
            print(e, file=sys.stderr)
            time.sleep(1)


# Define some variables so the code reads easier
session = os.environ.get('TG_SESSION', 'printer')
api_id = 21151878 #get_env('TG_API_ID', 'Enter your API ID: ', int)
api_hash = '2cb59b7dfbcaf929a9cfc25fbe8cf4e8' #get_env('TG_API_HASH', 'Enter your API hash: ')
proxy = None  # https://github.com/Anorov/PySocks


# This is our update handler. It is called when a new update arrives.
async def handler(update):
    response_string=str(update)
    pattern = r"message='(.*?)'"

    # Use regular expression to find the message value
    message_match = re.search(pattern, response_string)

    if message_match:
        message_value = message_match.group(1)
        # Split the string by space
        parts = message_value.split()

        # Extract Buy Signal and Sell Price
        ts = parts[3]
        print("TS value::",ts)
        buy_price = parts[-1].strip(":")
        quote=kite.quote("NFO:"+ts)["NFO:"+ts]
        print(quote['last_price'])
        print("Message value:", ts,"Buy Price:",buy_price)


# Use the client in a `with` block. It calls `start/disconnect` automatically.
with TelegramClient(session, api_id, api_hash, proxy=proxy) as client:
    # Register the update handler so that it gets called
    client.add_event_handler(handler)

    # Run the client until Ctrl+C is pressed, or the client disconnects
    print('(Press Ctrl+C to stop this)')
    client.run_until_disconnected()
