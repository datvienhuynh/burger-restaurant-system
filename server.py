from flask import Flask
from init import bootstrap_system
from pickle_system import load_data

app = Flask(__name__)
app.secret_key = '123456'

system = load_data()

mains = []
sides_drinks = []
total_price = 0
