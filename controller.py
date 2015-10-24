from app import app, search
from flask import request, redirect, session
import twilio.twiml
import pdb

SECRET_KEY = 'a secret key'
callers = {}
addresses = {}

def parseInitialResponse(body, from_number):
  resp = twilio.twiml.Response()
  initial_response = int(body)

  if initial_response == 1:
    callers[from_number] = 'shelter'
    resp.message("Great, enter your current street address.")
  elif initial_response == 2:
    callers[from_number] = 'meal'
    resp.message("Great, enter your current street address.")
  else:
    callers[from_number] = 'init'
    resp.message("Invalid Response. Press 1 for the nearest shelter, press 2 for a meal.")

  return str(resp)

def getShelter(address, from_number):
  resp = twilio.twiml.Response()

  request = search.get_closest_service('shelter', address)
  status = request[1]
  messsage = search.get_details(request)

  if status:
    callers[from_number] = 'shelter_address'
    addresses[from_number] = address
  else:
    callers[from_number] = 'init'
    resp.message("Press 1 for the nearest shelter, press 2 for a meal.")

  resp.message(messsage)

  return str(resp)

def getMeal(address, from_number):
  resp = twilio.twiml.Response()
  callers[from_number] = 'meal_address'

  request = search.get_closest_service('food', address)
  status = request[1]
  messsage = search.get_details(request)

  if status:
    callers[from_number] = 'food_address'
    addresses[from_number] = address
  else:
    callers[from_number] = 'init'
    resp.message("Press 1 for the nearest shelter, press 2 for a meal.")

  resp.message(messsage)
  return str(resp)

def getShelterAddress(address, from_number):
  resp = twilio.twiml.Response()

  request = search.get_closest_service('shelter', addresses[from_number])
  messsage = search.get_directions(request)
  callers[from_number] = 'init'

  resp.message(messsage)
  return str(resp)

def getFoodAddress(address, from_number):
  resp = twilio.twiml.Response()

  request = search.get_closest_service('food', addresses[from_number])
  messsage = search.get_directions(request)
  callers[from_number] = 'init'

  resp.message(messsage)
  return str(resp)

options = {
  'init' : parseInitialResponse,
  'shelter' : getShelter,
  'meal' : getMeal,
  'shelter_address': getShelterAddress,
  'food_address': getFoodAddress
}

@app.route("/text_messaging", methods=['GET', 'POST'])
def index():
  resp = twilio.twiml.Response()

  from_number = request.values.get('From')
  if from_number in callers:
    state = callers[from_number]
    if state in options:
      body = request.values.get('Body')
      return options[state](body, from_number)
    else:
      callers[from_number] = 'init'
      resp.message("Invalid Response. Press 1 for the nearest shelter, press 2 for a meal.")
  else:
    callers[from_number] = 'init'
    resp.message("Welcome to Text2Help. Press 1 for the nearest shelter, press 2 for a meal.")

  return str(resp)