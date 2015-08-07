import math
from time import time, sleep
from datetime import datetime

def roundup(x):		# Round up to the nearest 10.
	return int(math.ceil(x/10.0))*10

def time_string():
	return datetime.now().strftime("%y%m%d_%H%M%S.%f")[:-3]		# Chop off the last three decimal places, leaving three (not rounding).

def time_to_string(t):
	return datetime.fromtimestamp(t).strftime("%y%m%d_%H%M%S.%f")[:-3]

def string_to_time(string):
#	string = string.split(".")[0]		# Ignore possible decimals in seconds.
	pieces = string.split("_")
	time_object = datetime(2000 + int(pieces[0][:2]), int(pieces[0][2:4]), int(pieces[0][4:6]), int(pieces[1][:2]), int(pieces[1][2:4]), int(float(pieces[1][4:])))
#	print time_object
#	print time()
#	print datetime.utcfromtimestamp(0)
	delta = time_object - datetime.utcfromtimestamp(0)
	return delta.total_seconds()
