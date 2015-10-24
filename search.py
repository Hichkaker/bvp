import requests
from app.models import Service
import json
import pdb
import traceback
import re

def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

def get_route(address, service):

    request_string = 'https://maps.googleapis.com/maps/api/directions/json?origin=' + address +'&destination='+service.house+'%20'+service.street + '%20San%20Francisco&key=AIzaSyD_nj66yBswG4f3erU5foaVxAsJagST-9M&mode=walking'
    response = requests.get(request_string)
    #if response status code
    response = json.loads(response.text)
    directions = []

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
    house = address[0]
    street = address[1]
    city = 'San%20Francisco'
    address_string = house+'%20'+street+'%20'+city

    if(service_type == 'shelter'):
      options = Service.query.filter(Service.service_type=='shelter').all()
      min_distance_service = {'distance': 1000000}

      for service in options:
        service_data = get_route(address_string, service)
        if float(service_data['distance']) < float(min_distance_service['distance']):
          min_distance_service = service_data

    return(min_distance_service)
  except:
    traceback.print_exc()
    return('ERROR')

def to_string(data):
  answer = 'The closest {} service to your location is ~{} away at {} {}. For directions press 5.'.format(
    data['service'].service_type, data['duration'], data['service'].house, data['service'].street )
  return answer
