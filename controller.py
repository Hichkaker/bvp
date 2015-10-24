from app import app
from flask import request, redirect, session
import twilio.twiml
import pdb

SECRET_KEY = 'a secret key'
callers = {}

def parseInitialResponse():
  initial_response = int(request.values.get('Body'))
  from_number = request.values.get('From')
  
  if initial_response == 1:
    callers[from_number] = 'shelter';
    resp.message("Great, enter your current street address.")
  elif initial_response == 2:
    callers[from_number] = 'meal';
    resp.message("Great, enter your current street address.")
  else:
    resp.message("Invalid Response. Press 1 for the nearest shelter, press 2 for a meal.")
  
  return str(resp)

def getShelter():
  address = request.values.get('Body')
  # make API request against shelter endpoint with address
  resp.message("Go here to get shelter.")
  return str(resp)

def getMeal():
  address = request.values.get('Body')
  # make API request against meal endpoint with address
  resp.message("Go here to get meal.")
  return str(resp)

options = {
  'init' : parseInitialResponse,
  'shelter' : getShelter,
  'meal' : getMeal,
}

@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def index():
  resp = twilio.twiml.Response()

  from_number = request.values.get('From')
  if from_number in callers:
    state = callers[from_number]
    if state in options:
      options[state]()
    else:
      resp.message("Invalid Response. Press 1 for the nearest shelter, press 2 for a meal.")
  else:
    resp.message("Welcome to HelpNow. Press 1 for the nearest shelter, press 2 for a meal.")
    callers[from_number] = 'init';

  return str(resp)