#! /usr/bin/env python
# -*- coding: utf-8 -*-

from gimpfu import *
import os, sys
import datetime, time
import discord_rpc

today = datetime.date.today() # Get today's date
formatted_date = today.strftime("%d/%m/%Y") # Format the date as DD/MM/YYYY
client_id = '1120074792935100567'

def readyCallback(current_user):
    print('Our user: {}'.format(current_user))

def disconnectedCallback(codeno, codemsg):
    print('Disconnected from Discord rich presence RPC. Code {}: {}'.format( codeno, codemsg))

def errorCallback(errno, errmsg):
    print('An error occurred! Error {}: {}'.format(errno, errmsg))

# Note: 'event_name': callback
callbacks = {
        'ready': readyCallback,
        'disconnected': disconnectedCallback,
        'error': errorCallback,
    }

def init_discord_rpc():
    discord_rpc.initialize(client_id, callbacks=callbacks, log=False)
    pdb.gimp_message("Connected to Discord RPC")
    start = time.time()
    while True:
        discord_rpc.update_presence(
            **{
                'details': 'Connected',
                'start_timestamp': start,
                'large_image_key': 'default'
            }
        )

        discord_rpc.update_connection()
        time.sleep(2)
        discord_rpc.run_callbacks()

# discord_rpc.shutdown()


def gimpcord(image, drawable):
    init_discord_rpc()


# Registration
whoiam="\n"+os.path.abspath(sys.argv[0])
author="Dooder"
menu="<Image>/Filters/Discord/drp"
pluginName="drp"
dateOfCreation=formatted_date
desc=""

def register_plugin():
    # Register the plugin
    register(
        pluginName,  # Unique name for your plugin
        desc+whoiam, # The label that appears in GIMP's menus
        desc,  # Description of your plugin
        author, # Your name as the plugin author
        author, # Copyright information
        dateOfCreation, # Date of the plugin
        menu,
        "*",
        [],  # No input parameters required
        [],  # No return values
        gimpcord, # Your plugin function
        )

# Run the plugin
register_plugin()
main()
