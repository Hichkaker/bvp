import requests
from app.models import Service
import json
import pdb
import traceback
import re
#from app import keen

def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub(' ', data)

def get_route(address, service):

    request_string = 'https://maps.googleapis.com/maps/api/directions/json?origin=' + address +'&destination='+service.house+'%20'+service.street + '%20San%20Francisco&key=AIzaSyD_nj66yBswG4f3erU5foaVxAsJagST-9M&mode=walking'
    response = requests.get(request_string)
    #if response status code
    response = json.loads(response.text)
   # try:
    #    keen.add_event("request", {
     #     "": "lloyd",
      #    "referred_by": "harry"
      #})
    #except:
     # pass

    directions = []
   # pdb.set_trace()
    for steps in response['routes'][0]['legs'][0]['steps']:
      directions.append(striphtml(steps['html_instructions']))


    data = {
      'service' : service,
      'distance': response['routes'][0]['legs'][0]['distance']['text'].split(" ")[0],
      'duration': response['routes'][0]['legs'][0]['duration']['text'],
      'directions': directions
    }
    return data


def get_closest_service(service_type, address):
  try:
    address = address.split(" ")
    house = address[0].strip()
    street = address[1].strip()
    city = 'San%20Francisco'
    address_string = house+'%20'+street+'%20'+city

    options = Service.query.filter(Service.service_type==service_type).all()
    min_distance_service = {'service':None,'distance': 1000000}

    for service in options:
      #pdb.set_trace()
      service_data = get_route(address_string, service)
      if float(service_data['distance']) < float(min_distance_service['distance']):
        min_distance_service = service_data
    #pdb.set_trace()
    re = (min_distance_service,True)
    return re
  except:
    traceback.print_exc()
    re = ({'service':None}, False)
    return re


def get_details(data):


  if(data[0]['service'] is None):
      answer = """Unfortunately none of the services are currently open. Let's try later!"""
  else:
      answer = """The closest open {} service to your location is {} ~{} away at {} {}. For directions press 5.""".format(
                                          data[0]['service'].service_type,
                                          data[0]['service'].name,
                                          data[0]['duration'],
                                          data[0]['service'].house,
                                          data[0]['service'].street
                                        )
  return answer


def get_directions(data):
  #pdb.set_trace()
  if(data[0]['service'] is None):
      answer = """Undortunately detailed directions are not available at the moment."""
  else:
      answer =  '. '.join(data[0]['directions'])
  return answer

