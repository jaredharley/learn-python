import os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def colorText(text, color='none'):
	if color == 'red':
		return bcolors.FAIL + text + bcolors.ENDC
	elif color == 'green':
		return bcolors.OKGREEN + text + bcolors.ENDC
	elif color == 'yellow':
		return bcolors.WARNING + text + bcolors.ENDC
	elif color == 'none':
		return text
	else:
		return text

def ClearScreen():
	os.system('cls')
	os.system('clear')
	return