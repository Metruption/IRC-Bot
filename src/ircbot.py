#! /usr/bin/env python3.5
import sys
import signal
import concurrent.futures
import logging
import os
import pyautogui

import test_config
import parser_please_work
import err
from functions import *

def run(socket, cmds):
    print(str(cmds))
    # buffer for some command received
    buff = ''

    #this line was in the original bot, i have no idea what it does but i'm keeping it because it's probably better than whatever i'll end up writing...
    #num_workers = sum(len(v) for k, v in cmds.iteritems())
    num_workers = len(cmds) + 14 #i wrote this one worker for each command plus 12 to account for the nesbuttons

    # TODO: what happens if I use all the workers?

    # TODO: don't let commands to run for more than one minute

    print('entering the big loop of doom')
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
        while True:
            response = ''
            receive = socket.recv(4096).decode('utf-8')
            buff = buff + receive


            if receive:
                logging.debug(receive + \
                    ('' if '\n' == receive[len(receive)-1] else '\n'))

            if -1 != buff.find('\n'):
                # get a full command from the buffer
                command = buff[0 : buff.find('\n')]
                buff = buff[buff.find('\n')+1 : ]

                # command's components after parsing
                components = parser_please_work.parse_command(command)
                to = send_to(command)

                #THIS IS SUCH BAD CODE AND IM NOT FIXING IT
                    #SORRY FOR YELLING
                    #i forgot i had capslock on
                if 'PING' == components['action']:
                    response = []
                    response.append('PONG')
                    response.append(':' + components['arguments'])

                elif 'PRIVMSG' == components['action']:

                    if '!' == components['arguments'][0]:
                        # a command from a user only makes sense if it starts
                        # with an exclamation mark

                        pos = components['arguments'].find(' ')
                        if -1 == pos:
                            pos = len(components['arguments'])

                        # get the command issued to the bot without the "!"
                        cmd = components['arguments'][1:pos]
                        args = components['arguments'][pos+1:].split

                        callable_cmd = get_cmd(cmd, cmds['user'])
                        if callable_cmd:
                            run_cmd(socket, executor, to, callable_cmd,
                                    components)
                        # else:
                        #     callable_cmd = get_cmd(cmd, cmds['core'])
                        
                        #     if callable_cmd:
                        #         try:
                        #             response = callable_cmd(socket, components)
                        #         except Exception as e:
                        #             response = err.C_EXCEPTION.format(
                        #             callable_cmd.__name__)

                        #             logging.error(str(e))


                    '''so we need to parse out "up, down, left, right, a, b, start, select
                        a/b/start/select will only be parsed out if it is the only thing in the message

                        up/down/left/right will only be parsed out if the first characters in it are the command and all others are either
                        a number (to indicate how many) or whitepace

                    '''
                    #todo(metro) make this spot a little more DRY. you know you can do better ;)
                    if components['arguments'] in ['a','b','start','select']:
                        logging.info(components['sender'] + ' pressed ' + components['arguments'])
                        print(components['sender'] + ":" + components['arguments'])
                        pyautogui.typewrite(test_config.buttons[components['arguments']])
                    
                    else:
                        direction = parse_direction(components['arguments'])
                        if direction[0] in ['up','down','left','right']:
                            logging.info(components['sender'] + ' pressed ' + components['arguments'])
                            print(components['sender'] + ":" + components['arguments'])
                            for i in range(direction[1]):
                               pyautogui.typewrite(test_config.buttons[direction[0]])    


                    # run auto commands
                    for cmd in test_config.cmds['auto']:
                        callable_cmd = get_cmd(cmd, cmds['auto'])
                        if callable_cmd:
                            run_cmd(socket, executor, to, callable_cmd,
                                    components)

                #this shoudl never happen so imma comment it out and hope it still works.

                # elif 'KICK' == components['action'] and \
                #     nick == components['action_args'][1]:
                #         channels.remove(components['action_args'][0])

                # elif 'QUIT' == components['action'] and \
                #         -1 != components['arguments'].find('Ping timeout: '):
                #     channels[:] = []


            # this call is still necessary in case that a PONG response or a
            # core command response should be sent, every other response is
            # sent when the futures finish working from their respective
            # thread
            send_response(response, to, socket)

            buff = ''


def main():
    valid_cfg = check_cfg(test_config.owner, test_config.server, test_config.nick, test_config.log, test_config.cmds)

    if not valid_cfg:
        sys.exit(err.INVALID_CFG)

    if not os.path.isdir(test_config.log):
        try:
            os.makedirs(test_config.log)
        except os.error as e:
            print("Log directory creation failed: " + str(e))
            sys.exit(1)
        else:
            print ("Log directory created")

    logfile = get_datetime()['date'] + '.log'

    try:
        logging.basicConfig(filename=os.path.join(test_config.log, logfile),
            level=test_config.logging_level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')
    except IOError as e:
        print("Couldn't set up logging: " + str(e))
        sys.exit(1)

    if not check_channel(test_config.channel):
        sys.exit(err.INVALID_CHANNELS)

    signal.signal(signal.SIGINT, sigint_handler)

    socket = create_socket()

    if socket and connect_to((test_config.server, test_config.port), socket):
        content = 'Connected to {0}:{1}'.format(test_config.server, test_config.port)
        logging.info(content)
        print(content)

        test_config.current_nick = test_config.nick
        #socket.connect((test_config.server, test_config.port))
        socket.send("PASS {PASS}\r\n".format(PASS=test_config.password).encode('utf-8'))
        socket.send("NICK {NICK}\r\n".format(NICK=test_config.nick).encode('utf-8'))
        socket.send("JOIN #{CHANNEL}\r\n".format(CHANNEL=test_config.channel).encode('utf-8'))

        run(socket, test_config.cmds)

        quit_bot(socket)
        socket.close()

        content = 'Disconnected from {0}:{1}'.format(test_config.server, test_config.port)
        logging.info(content)
        print(content)

if '__main__' == __name__: #pragma: no cover
    main()
