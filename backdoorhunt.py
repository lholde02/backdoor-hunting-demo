import argparse
import scapy.all as scapy
import socket as s
import subprocess
import sys  #for printing one character at a time
import time #for sleeping between scans in learning mode

# Number of valid ports on machines
NUM_PORTS = 65535

# How many ports to scan before adding another symbol to the progress bar
PROGRESS_BAR = NUM_PORTS/10

# Number of seconds between executions
GAP_TIME = 10 #3600 s - 60 sec/ 1 minute - 60 mins/ 1 hour
RUNNING_TIME = 60 # 43200 - 12 hours

# Handling the three possible modes by having two optional args
parser = argparse.ArgumentParser(description='A tool for detecting the more obvious backdoors by looking for any ports that should not be open')
parser.add_argument('--learning', help='Acticates learning mode', action="store_true")
parser.add_argument('-auto', metavar='PORTSFILE', help='Activates autonomous monitoring mode, needs a txt file of commonly used ports')

# Clears the terminal for the output from this program
subprocess.call('clear', shell=True)

# Subfunction for scanning your own computer
def self_scan():
    i = 1
    list = []
    print 'Progress |',
    while i <= NUM_PORTS:
        sock = s.socket(s.AF_INET, s.SOCK_STREAM)
        sock.settimeout(2) #2 Second Timeout
        result = sock.connect_ex(('127.0.0.1', i)) #Scanning yourself
        if result == 0:
            list.append(i)
        i = i + 1
        if (i % PROGRESS_BAR) == 0:
            sys.stdout.write('x')
            sys.stdout.flush()
    # Source of code:
    # https://stackoverflow.com/questions/19196105/python-how-to-check-if-a-network-port-is-open-on-linux
    print '|'
    return list

# USER-MEDIATED MONITORING
def user_monitoring():
    ports = self_scan()
    if not ports: #if empty list
        print "No ports open!"
    else:
        fixes_required = []
        for port in ports:
            print 'Port # ' + str(port) + ' is open.'
            answer = raw_input('Do you think this port should be open? (y/n): ')
            if answer is 'n' or answer is 'N':
                fixes_required.append(port)
        print
        print '#####Scans complete#####'
        print 'Recommended fix is to close the following ports:'
        for port in fixes_required:
            print '-' + str(port)
        print '**As a reminder, it is safer to close as many ports as possible'

# LEARNING MODE
def learning():
    print 'Starting learning process: 12 hours remaining'
    i = 0
    normal_ports = []
    while i <= RUNNING_TIME:
        # Once an hour, record the ports in use
        print 'Starting hourly scan: Hour ' + str(i % GAP_TIME) 
        ports = self_scan()
        print 'Open ports: '
        if ports is not []:
            print ports
        else:
            print 'None'
        for port in ports:
            if port not in normal_ports:
                normal_ports.append(port)
        i = i + 1 + GAP_TIME # Counts the gap time for the sleep mode
        time.sleep(GAP_TIME)
    # Write to a file
    file = open('normal_ports.txt', 'w')
    for port in normal_ports:
        file.write(str(port) + ',')
    file.close()

# AUTONOMOUS MONITORING
def auto_monitoring():
    file = open('normal_ports.txt', 'r')
    list = file.read()
    print list
    normal_ports = list.split(',')
    while 1:
        found_ports = self_scan()
        print found_ports
        for found in found_ports:
            # found ports are integers
            sketchy_port = False
            for normal in normal_ports:
                # normal ports are all strings
                in_list = False
                if str(found) == normal:
                    in_list = True
            if in_list == False:
                sketchy_port = True
                print 'ALERT: sketchy port detected'

# Main function that handles movement between the three modes
args = parser.parse_args()
print '++++++++Backdoor Hunter Demo Software++++++++'
if args.learning:
    print 'Selected Mode: Learning'
    learning()
elif args.auto is not None:
    print 'Selected Mode: Autonomous Monitoring'
    print '** Requires first running in learning mode'
    auto_monitoring()
else:
    print 'Selected Mode: User-Mediated Monitoring'
    user_monitoring()
    
