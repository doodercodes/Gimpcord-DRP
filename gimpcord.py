#! /usr/bin/env python2
# -*- coding: utf-8 -*-

import datetime
import sys, traceback, trace
import os, io, time
from gimpfu import *
import discord_rpc

pdb = gimp.pdb
today = datetime.date.today() # Get today's date
formatted_date = today.strftime( "%d/%m/%Y" ) # Format the date as DD/MM/YYYY
whoiam="\n"+os.path.abspath(sys.argv[0])
plugin_name="drp"
author="Dooder"
where="<Image>"
menu="/Filters/Discord/drp"
menu_path=where+menu
path_to_config = 'C:\Users\User\AppData\Roaming\GIMP\\2.10\plug-ins\Dooder\gimpcord\config.txt'
date_of_creation=formatted_date
desc=""

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
    """
    Open config.txt for reading. Create
    the file if it does not exist
    Return: list[list[str]]
    """
    with open(path_to_config, "r+") as file:
        lines = [line.strip().replace(" ", "").split(":") for line in file]

    return lines

def setClientID(clientID):
    """
    Update the clientID in config.txt
    """
    lines = readConfigFile()
    lines[0][1] = clientID

    with open(path_to_config, "w") as file:
        for line in lines:
            file.write(":".join(line) + "\n")

def getClientID():
    """
    Get the clientID from config.txt
    Return: str
    """
    read_config = readConfigFile()
    client_id = read_config[0][1]

    return client_id

def initDiscordRPC(image, drawable, clientID):
    """

    """
    if clientID == "":
        echo.echo("Client ID is empty or incorrect.\r\nFailed to connect to Discord.\r\n\r\nPlease reactivate the plug-in at " + menu + " and try again.\r\nAlternatively, you can re-show the last used filter by using the default keybinding 'Shift+Ctrl+F' to try entering in your ID again.")

    else:
        echo.echo("Connected to Discord RPC")
        discord_rpc.initialize( clientID, callbacks=callbacks, log=False )
        setClientID(clientID)


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

def gimpcord(image, drawable, clientID):
    """
    Main plug-in function
    """
    initDiscordRPC(image, drawable, clientID)

def register_plugin():
    """
    Register the plugin
    """
    register(
        plugin_name,  # Unique name for your plugin
        desc+whoiam, # The label that appears in GIMP's menus
        desc,  # Description of your plugin
        author, # Your name as the plugin author
        author, # Copyright information
        date_of_creation, # Date of the plugin
        menu_path,
        "*",
        [
                (PF_STRING, "text", "ClientID: ", " "),

        ],
        [],  # No return values
        gimpcord, # Your plugin function
        )

# Run the plugin
register_plugin()
main()
