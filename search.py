import requests
from app.models import Service
import json
import pdb
import traceback


def get_route(address, service):

    request_string = 'https://maps.googleapis.com/maps/api/directions/json?origin=' + address +'&destination='+service.house+'%20'+service.street + '%20San%20Francisco&key=AIzaSyD_nj66yBswG4f3erU5foaVxAsJagST-9M&mode=walking'
    response = requests.get(request_string)
    #if response status code
    response = json.loads(response.text)
    pdb.set_trace()
    route = (response['routes'][0]['legs'][0]['distance']['text'].split(" ")[0],
             response['routes'][0]['legs'][0]['duration']['text'])
    return route

def get_closest_service(service_type, address):
  try:
    address = address.split(" ")
    house = address[0]
    street = address[1]
    city = 'San%20Francisco'
    address_string = house+'%20'+street+'%20'+city

    if(service_type == 'shelter'):
      options = Service.query.filter(Service.service_type=='shelter').all()
      min_distance = 10000
      min_duration = 10000
      min_distance_service = None

      for service in options:
        route = get_route(address_string, service)
        if float(route[0]) < min_distance:
          min_distance_service = service
          min_distance = route[0]
          min_duration = route[1]

    return((min_distance_service, min_distance, min_duration))
  except:
    traceback.print_exc()
    return('ERROR')


