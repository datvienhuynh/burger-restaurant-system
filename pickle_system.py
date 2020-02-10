from flask import Flask
from init import bootstrap_system
import pickle

def save_data(system):
	try:
		with open('system.pickle','wb') as file:
			pickle.dump(system, file)
	except:
		print("Saving failed")

def load_data():
	try:
		with open('system.pickle','rb') as file:
			system = pickle.load(file)
	except IOError:
		system = bootstrap_system()
		print("Initialize new system")
	
	return system
