import os
import os.path
import time
import logging

# some commands can be executed only if the user's nick is found in this list
owner = list(set([
    'Metruption'
]))

owner_email = {
    'Metruption': 'theaaront222@yahoo.com',
}

# server to connect to
server = 'irc.twitch.tv'
# server's port
port = 6667

# bot's nicknames
nicks = list(set(['Metrotwitchplays']))
# bot's real name
real_name = 'Metruption'

# channels to join on startup
channels = list(set([
    '#metrotwitchplays'
]))

cmds = {
    # core commands list, these commands will be run in the same thread as the bot
    # and will have acces to the socket that the bot uses
    'core': list(set([
        'quit',
        'join',
        'channels',
    ])),

    # normal commands list, the ones that are accessible to any user
    'user': list(set([
        #REMOVE ALL THE OLD COMMANDS I DONT NEED ANY OF THEM MWAGHHAHAH (i'll keep their code just so I can cheat and look at them)
        #todo(metro) think of commands and implement them
        '''
        -savestate
        -loadstate
        -setstate
        -autosavestate
        '''
        ])),

    # commands list that the bot will execute even if a human didn't request an
    # action
    'auto': list(set([
        'email_alert',
    ])),
}

# smtp server for email_alert
smtp_server = 'smtp.gmail.com'
smtp_port = 25
from_email_address = 'changeme@gmail.com'
from_email_password = 'p@s$w0rd'

# users should NOT modify below!
log = os.path.join(os.getcwd(), '..', 'logs', '')
logging_level = logging.DEBUG
start_time = time.time()
current_nick = ''
