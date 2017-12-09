# Backdoor Hunting Demo
A quick program to help developers and security professionals think about how to detect backdoors on their own systems. This is also an example of how easy it is to program your own monitoring functionality. I have previously written only one short program in Python prior to this program. Coding this project took me approximately 6 hours start to finish, including lots of polishing, commenting, planning, and writing out this README.

I hope this will inspire others to think about what systems they have in place to look for suspicious activity on their own computers and networks.

** Note: this program was designed to work on the Kali Linux distribution. It runs well on Python version 2.7.13

## Modes

There are several ways that you can use the backdoor hunting demo: user-mediated, learning, and autonomous mode. 

#### Learning

Learning mode is a precursor to autonomous monitoring. It runs for 1 hour, scanning every 10 seconds, in order to get a read on what ports should normally be open. The program then writes what ports are 'normal' to a file that can then be used by autonomous mode. One key part of this mode is that you should be fairly confident that all port activity is normal when you engage learning mode since this is the standard that we will rely on during autonomous monitoring mode.

Learning mode can be finished at any time by pressing CTRL-C. The list of normal ports collected so far will still be written to a file.

#### Autonomous Monitoring

This mode requires that the user has run 'Learning' mode prior to use. This option will then use the file of 'normal' ports produced by learning mode in order to determine what ports are valid or not. 

Autonomous monitoring mode can be exited at any time by pressing CTRL-C. 

#### User-mediated Monitoring

This is the simplest option. In this mode, the program will scan your computer in order to see what ports are open. It will then go through the list of all open ports and ask you if you intended for those ports to be open. At the end, it will print out the ports that should be closed.
