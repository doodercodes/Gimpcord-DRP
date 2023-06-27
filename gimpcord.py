#! /usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import sys, traceback, trace
import os, io, time
from gimpfu import *
import discord_rpc

pdb = gimp.pdb
today = datetime.date.today() # Get today's date
formatted_date = today.strftime( "%d/%m/%Y" ) # Format the date as DD/MM/YYYY

class HandleErrors:
    def __init__(self):
        self.exc_type, self.exc_value, self.exc_traceback = sys.exc_info()
    def throwTraceback(self):
        error_message = ' '.join( traceback.format_exception( self.exc_type, self.exc_value, self.exc_traceback ))
        pdb.gimp_message(error_message)

class Echo:
    def __init__(self):
        pass
    def echo( self, *args ):
        text = ' '.join(map( str, args ))
        pdb.gimp_message(text)
    def trace( self, *args ):
        text = ' '.join( map( str, args ))
        line_number = sys._getframe(1).f_lineno
        cwd = os.getcwd()
        file = os.path.join( cwd, 'gimpcord.py' )
        pdb.gimp_message('{}\r\nLine: #{}\r\nFile: {}\r\n'
                        .format( text, line_number,file ))

echo = Echo()

def readyCallback( current_user ):
    print('Our user: {}'.format( current_user ))

def disconnectedCallback( codeno, codemsg ):
    print('Disconnected from Discord rich presence RPC. Code {}: {}'
        .format( codeno, codemsg ))

def errorCallback( errno, errmsg ):
    print('An error occurred! Error {}: {}'.format( errno, errmsg ))

callbacks = {
    'ready': readyCallback,
    'disconnected': disconnectedCallback,
    'error': errorCallback,
}

def readConfigFile():
    path_to_config = 'C:\Users\User\AppData\Roaming\GIMP\\2.10\plug-ins\Dooder\gimpcord\config.txt'
    with open(path_to_config, "r+") as file:
        lines = [line.strip().replace(" ", "").split(":") for line in file]

    return lines

def loadClientID():
    read_config = readConfigFile()
    client_id = read_config[0][1]

    return client_id

def initDiscordRPC(image):
    client_id = loadClientID()
    echo.echo(client_id)

    if client_id != None:
        echo.echo("Connected to Discord RPC")
        discord_rpc.initialize( client_id, callbacks=callbacks, log=False )

        start = time.time()
        file_name = image.filename
        active = image.active_layer
        width = image.width
        height = image.height
        layers = len(image.layers)

        while True:
            discord_rpc.update_presence(
                details=file_name,
                state='Resolution: {}x{} | Layers: {}'
                .format( width, height, layers ),
                start='{}'.format(start),
                large_image='default' )
            discord_rpc.update_connection()
            time.sleep(2)
            discord_rpc.run_callbacks()
    else:
        pass

# discord_rpc.shutdown()
def gimpcord(image, drawable):
    initDiscordRPC(image)

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
