#! /usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import sys, traceback, trace
import os, io, time
from gimpfu import *
import discord_rpc

pdb = gimp.pdb

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
        line_number = sys._getframe(1).f_lineno
        cwd = os.getcwd()
        file = os.path.join( cwd, 'gimpcord.py' )
        text = ' '.join( map( str, args ))
        pdb.gimp_message('{}\r\nLine: #{}\r\nFile: {}\r\n'
                        .format( text, line_number,file ))

today = datetime.date.today() # Get today's date
formatted_date = today.strftime( "%d/%m/%Y" ) # Format the date as DD/MM/YYYY
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
        lines = [line.strip() for line in file]
    return lines

        # for i in file:
        #     # echo.trace(i)
        #     split = i.split(":")
        #     return split[1].replace(" ", "")

def loadClientID():
        read_config = readConfigFile()

        # process the lines
        for line in read_config:
            split = line.split(":")
            echo.echo(split)

        # client_id = config_file
        # echo.trace(read_config)
        # if not file.seek(8) or file.seek(9):
        #     echo.trace( 'ClientID is not set or is invalid.' )
        #     return None
        # else:
        #     file.seek(9) or file.seek(9)
        #     client_id = file.readline()

        # return client_id

def initDiscordRPC(image):
    client_id = loadClientID()
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
