from blinker import signal
import web, json, time
import gv  # Get access to sip's settings, gv = global variables
from urls import urls  # Get access to sip's URLs
from sip import template_render
from webpages import ProtectedPage

params = []

# Read in the parameters for this plugin from it's JSON file
def load_params():
    global params
    try:
        with open('./data/ospi.json', 'r') as f:  # Read the settings from file
            params = json.load(f)
    except IOError: #  If file does not exist create file with defaults.
        params = {
            'nstations': 3,
            'active': 'low'
        }
        with open('./data/ospi.json', 'w') as f:
            json.dump(params, f)
    return params

load_params()


nstations = 3

