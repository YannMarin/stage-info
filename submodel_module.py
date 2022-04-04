''' Module reading a Sub-model file consisting of a single file  '''
#TODO a tester
import numpy as np
import os

def file_type():
	return 'submodel'

def description():
	return ''

def file_exists(path):
	if(os.path.isfile(path)):
		return True;
	else:
		return False

def read(path):
	submodel_array = []

	with open(path) as f:
		while(True):
			stri = f.readline().rstrip('\n')
			if (stri == ''):
				break;
			split = stri.split(" ")
			submodel_array.append([int(split)]);
	return submodel_array



def read_serializable(path):
	return read(path)

def write(subset, path):
	with open(path, "w") as submodel_file:
		for elem in subset:
			submodel_file.write(str(elem) + '\n')

	return;

def delete(path):
	try:
		os.remove(path)
	except OSError:
		pass


def list_files(path):
	return [path];

def check_file_consistency(ldkdict, content):
	return True
