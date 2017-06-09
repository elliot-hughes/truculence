import math
from time import time, sleep
from datetime import datetime
import collections
import yaml



def flatten(d, parent_key='', sep='_'):
	items = []
	for key, value in d.items():
		new_key = parent_key + sep + key if parent_key else key
#		print new_key
		if value and isinstance(value, collections.MutableMapping):
			items.extend(flatten(value, parent_key=new_key).items())
		else:
			items.append((new_key, value))
	return dict(items)

def flatten_list(l):
	return [flatten_list(x) if isinstance(x, list) else x for sublist in l for x in sublist]

def roundup(x):		# Round up to the nearest 10.
	return int(math.ceil(x/10.0))*10

def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
# See http://stackoverflow.com/questions/5595425/what-is-the-best-way-to-compare-floats-for-almost-equality-in-python
	if isinstance(a, (int, float)) and isinstance(b, (int, float)):
		return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)
	else:
		return a == b

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

def progress(current, total, text="", width=50):
	full = int((current + 1)*(float(width)/total))
	empty = width - 1 - full
	percent = 100*float(current + 1)/total
	if current == total - 1:
		print "\t[{}]\t{:.2f} %".format("="*width, 100)
		print "\033[J\033[F"		# Clear to the end of the screen, then move the cursor up one line up
	elif current < total - 1:
		if current%4 == 0:
			print "\t[{}-{}]\t{:.2f} %".format("="*full, " "*empty, percent)
		if (current+1)%4 == 0:
			print "\t[{}/{}]\t{:.2f} %".format("="*full, " "*empty, percent)
		if (current+2)%4 == 0:
			print "\t[{}|{}]\t{:.2f} %".format("="*full, " "*empty, percent)
		if (current+3)%4 == 0:
			print "\t[{}\\{}]\t{:.2f} %".format("="*full, " "*empty, percent)
		print "\033[J",		# Clear to the end of the screen (from the new line after the bar)
		print "\t\t" + str(text)
		print "\033[2F",		# Move the cursor up two lines.
	else:
		print "ERROR (utilities.progress): You tried to go over the maximum: {}/{} ({} %)".format(current, total, percent)


# http://stackoverflow.com/questions/5121931/in-python-how-can-you-load-yaml-mappings-as-ordereddicts:
def ordered_load(stream, Loader=yaml.Loader, object_pairs_hook=collections.OrderedDict):
	class OrderedLoader(Loader):
		pass
	
	def construct_mapping(loader, node):
		loader.flatten_mapping(node)
		return object_pairs_hook(loader.construct_pairs(node))
	
	OrderedLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping)
	
	return yaml.load(stream, OrderedLoader)

def wcl(path):
	n = 0
	with open(path) as in_file:
		n = sum(1 for line in in_file)
	return n


