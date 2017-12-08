import argparse
import socket as s # For scanning ports on your computer
import subprocess # For clearning the terminal
import sys  # For printing one character at a time
import time # For sleeping between scans in learning mode

# Number of valid ports on machines
NUM_PORTS = 65535

# How many ports to scan before adding another symbol to the progress bar
PROGRESS_BAR = NUM_PORTS/10

# Number of seconds between executions
GAP_TIME = 10 # in seconds, 60 sec/ 1 minute
RUNNING_TIME = 3600 # runs for an hour total

# Handling the three possible modes by having two optional args, defaults to user-mediated mode
parser = argparse.ArgumentParser(description='A tool for detecting the more obvious backdoors by looking for any ports that should not be open')
parser.add_argument('--learning', help='Acticates learning mode', action="store_true")
parser.add_argument('-auto', metavar='PORTSFILE', help='Activates autonomous monitoring mode, needs a txt file of commonly used ports')

# Clears the terminal for the output from this program
subprocess.call('clear', shell=True)

# Subfunction for scanning your own computer for open ports
def self_scan(quiet): # Quiet is a boolean which indicates if this function is in quiet mode
    port_num = 1
    list = []
    if not quiet: # Only prints out the progress bar if NOT in quiet mode, i.e. quiet is False
        print 'Progress |',
    # Loop through and scan each potentially open port
    while port_num <= NUM_PORTS:
        # Sockets are used to connect to another computer
        sock = s.socket(s.AF_INET, s.SOCK_STREAM)
        sock.settimeout(2) #2 Second Timeout
        result = sock.connect_ex(('127.0.0.1', port_num)) # Scanning yourself
        if result == 0: # If the port is open, appends it to the list
            list.append(port_num)
        port_num = port_num + 1 # Increment port number
        if (port_num % PROGRESS_BAR) == 0: # Increases the level on the loading bar after 10% more of the scans are complete
            if not quiet:
                sys.stdout.write('x')
                sys.stdout.flush()
    # Source of code:
    # https://stackoverflow.com/questions/19196105/python-how-to-check-if-a-network-port-is-open-on-linux
    if not quiet:
        print '|' # Ends progress bar
    return list # Returns the list of open ports

# USER-MEDIATED MONITORING
def user_monitoring():
    ports = self_scan(False) # Scan yourself for open ports, False means verbose mode
    if not ports: #if empty list
        print "No ports open!"
    else:
        fixes_required = [] # A list of ports that the user says should NOT be open
        for port in ports:
            print 'Port # ' + str(port) + ' is open.'
            answer = raw_input('Do you think this port should be open? (y/n): ')
            if answer is 'n' or answer is 'N': # Asks the user if this port should be open
                fixes_required.append(port)
        print # Adds a newline after the list of ports
        print '#####Scans complete#####'
        if not fixes_required: # Check if the list is empty
            print 'No recommended fixes. Have a good day!'
        else:
            print 'Recommended fix is to close the following ports:'
            for port in fixes_required:
                print '-' + str(port)
        print '**As a reminder, it is safer to close as many ports as possible'

# LEARNING MODE
def learning():
    print 'Starting learning process: ' + str(RUNNING_TIME) + '  seconds remaining'
    i = 0
    scan = 1
    normal_ports = []
    try:
        while i <= RUNNING_TIME:
            # Once an hour, record the ports in use
            print 'Starting scan #' + str(scan) + ': ' + str(i) + ' seconds in with ' + str(RUNNING_TIME - i) + ' seconds remaining'
            ports = self_scan(False) # False means self-scan in verbose mode
            print 'Open ports: '
            if ports is not []:
                print ports
            else:
                print 'None'
            for port in ports:
                if port not in normal_ports:
                    normal_ports.append(port)
            i = i + GAP_TIME # Counts the gap time between scans
            scan = scan + 1
            time.sleep(GAP_TIME)
    except KeyboardInterrupt:
        pass
    # Write the list of 'normal' ports to a file after the scan completes
    file = open('normal_ports.txt', 'w')
    for port in normal_ports:
        file.write(str(port) + ',')
    file.close()

# AUTONOMOUS MONITORING
def auto_monitoring():
    # Opens the file passed as an argument to -auto
    file = open(args.auto, 'r')
    list = file.read()
    print '** Press CTRL-C at any time to stop the process'
    print 'Ports found in list:'
    normal_ports = list.split(',')
    for port in normal_ports: # Print out the ports in the file
        if port != '':        # that we are going to label as normal
            print '-' + port
    try:
        while True:
            found_ports = self_scan(True) # Self-scan for open ports in quiet mode
            sketchy_ports = [] # Integer list of ports that we have alerted users about
            for found in found_ports:
                # Found ports are integers
                sketchy_port = False # First we assume the port isn't sketch
                for normal in normal_ports:
                    # Normal ports are all strings
                    in_list = False  # Then we check if the port is in the list of normal ports
                    if str(found) == normal:
                        in_list = True
                if in_list == False: # If this open port is not in the list, we tell the user it might be sketchy
                    sketchy_port = True
                    if found not in sketchy_ports: # Makes it so that we don't do too many alerts
                        print 'ALERT: open port #' + str(found) + ' may be sketchy'
                        sketchy_ports.append(found)
    except KeyboardInterrupt:
        pass

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
    
