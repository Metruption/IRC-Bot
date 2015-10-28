IRC Bot
=======
A simple IRC Bot written in Python
To start it just `cd` to the `src` directory and type `./ircbot.py`, although
before using the bot it's recommended to check the config first.

The bot can handle multiple channels at a time, also if you want to have a 
_private_ discussion it can be queried (`/query PPyBot`).

IRC Protocol reference: [RFC 1459](http://www.irchelp.org/irchelp/rfc/rfc.html
"IRC Protocol")


Adding commands
===============
1. In `src/config.py` you must add the name of the command to the `cmds_list`'s
   end(without _!_)
2. In `src/cmds/` directory you must create a file named after your command
3. Into the newly created file you must define a function named after your
   command that takes one parameter, this parameter will contain the command
   components sent by the user, the function must return either a 
   message(string) to be sent on the channel, either a list, first item being a
   command(other than PRIVMSG which is added automatically if needed) and the 
   second being the command's arguments.

E.g.:

If you want to create a command `!ncmd`, you must follow these steps:

1. Add 'ncmd' to the `cmds_list` in `src/config.py`
2. Create `src/cmds/ncmd.py`
3. In `src/cmds/ncmd.py` define `def dance(param):`, `param` will hold the users
   command components(see `src/parser.py`) in case you must do some checkings, 
   it must return a message(eg. `return 'Dance time!'`, in this
   case `src/ircbot.py` will automatically add `PRIVMSG` at the beginning and 
   `\r\n` at the end) or a list(eg. `return ['JOIN ', '#chan1,#chan2']`, in this
   case the list will be joined and `\r\n` added at the end)

If you want to create a command that the bot should execute if something happens
on the chat (not if the command is manually triggered) you should add the
command name to the `auto_cmds_list` insead of `cmds_list`.

Config
======
See `src/config.py`:

* `owner` - the users who are allowed to send a specific command to the bot
(for example the `!quit` command)
* `log` - path to the logging directory, all logs are stored here
* `server` - server to connect to (default: chat.freenode.net)
* `port` - port number to use (default: 6667)
* `channels` - a list of channels to connect to
* `nicks` - a list of strings, the bot's name will be the first unused nick from
  this list or the first nick in the list and a random sequence appended if all
  nicks are used
* `real_name` - bot's "real name"
* `cmds_list` - a list of strings that the bot knows to answer to
* `auto_cmds_list` - a list of commands defined as regular commands with the
  only difference that they cannot be invoked by users, the bot executes them as
  result of an event

Dependencies
============
When I implement the functionality for this to press buttons it will depend upon PyAutoGUI for those to work. PyAutoGUI can be found here: https://github.com/asweigart/pyautogui

License
=======
The Licence for the thing that I originally forked it from:
(C) Copyright 2011-2014 Barbu Paul - Gheorghe

This program is free software: you can redistribute it and/or modify it under 
the terms of the GNU General Public License as published by the Free Software 
Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with 
this program. If not, see http://www.gnu.org/licenses/.