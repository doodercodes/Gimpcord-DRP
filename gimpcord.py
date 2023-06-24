#! /usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import sys, traceback
import os, io, time
from gimpfu import *
import discord_rpc

class HandleErrors:
    def __init__(self):
        self.exc_type, self.exc_value, self.exc_traceback = sys.exc_info()

    def throw_GIMP_traceback(self):
        error_message = "".join(traceback.format_exception(self.exc_type, self.exc_value, self.exc_traceback))
        pdb.gimp_message(error_message)

class Echo:
    def __init__(self):
        pass
    def echo(self,param1):
        pdb.gimp_message('{}'.format(param1))

echo = Echo()

today = datetime.date.today() # Get today's date
formatted_date = today.strftime("%d/%m/%Y") # Format the date as DD/MM/YYYY

def readyCallback(current_user):
    print('Our user: {}'.format( current_user ))

def disconnectedCallback(codeno, codemsg):
    print('Disconnected from Discord rich presence RPC. Code {}: {}'.format( codeno, codemsg ))

def errorCallback(errno, errmsg):
    print('An error occurred! Error {}: {}'.format( errno, errmsg ))

# Note: 'event_name': callback
callbacks = {
        'ready': readyCallback,
        'disconnected': disconnectedCallback,
        'error': errorCallback,
    }

def load_client_id():
        dotenv_path = os.path.abspath("/plug-ins/Dooder/gimpcord/.env")
        client_id = os.getenv('client_id')
        if not client_id:
            echo.echo("Null")
            raise ValueError('Missing client ID in .env file')
        return client_id

def init_discord_rpc(image,client_id):
    discord_rpc.initialize(client_id, callbacks=callbacks, log=False)
    pdb.gimp_message("Connected to Discord RPC")

    start = time.time()
    fileName = image.filename
    active = image.active_layer
    width = image.width
    height = image.height
    layers = len(image.layers)

    while True:
        discord_rpc.update_presence(
            details=fileName,
            state='Resolution: {}x{} | Layers: {}'.format(width,height,layers),
            start='{}'.format(start),
            large_image='default')
        discord_rpc.update_connection()
        time.sleep(2)
        discord_rpc.run_callbacks()

# discord_rpc.shutdown()
def gimpcord(image, drawable):
    client_id = load_client_id()
    init_discord_rpc(image,client_id)


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
