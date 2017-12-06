# Backdoor Hunting Demo
A quick program to help you think about how to detect backdoors on your own system

## Modes

There are several ways that you can use the backdoor hunting demo: user-mediated, learning, and autonomous mode. 

#### Learning

Learning mode is a precursor to autonomous monitoring. It runs for 12 hours, scanning once an hour, in order to get a read on what ports should normally be open. The program then writes what ports are 'normal' to a file that can then be used by autonomous mode.

#### Autonomous Monitoring

This mode requires that the user has run 'Learning' mode prior to use. This option will then use the file of 'normal' ports produced by learning mode in order to determine what ports are valid or not. 

#### User-mediated Monitoring

The simplest option, in this mode the program will scan your computer in order to see what ports are open. It will then go through the list of all open ports and ask you if you intended those ports to be open. At the end, it will print out the ports that the user thinks should be closed.
