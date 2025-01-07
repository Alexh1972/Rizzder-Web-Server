import requests
import json
import logging
from math import cos, asin, sqrt, pi
 
logger = logging.getLogger(__name__)
 
 
class Location():
    ip_address = ""
 
    def __init__(self, ip_address):
        self.ip_address = ip_address
 
    def getLatitudeAndLongitude(self):
        dict = self.getLocation()
 
        if dict['status'] == 'fail':
            return None, None
        return dict['lat'], dict['lon']
 
    def getLocation(self):
        url = 'http://ip-api.com/json/' + self.ip_address
        res = requests.get(url)
        dict = json.loads(res.text)
        logger.info("LOCATION FETCH - " + url + " - DATA - " + str(dict))
        return dict
 
 
def distance(lat1, lon1, lat2, lon2):
    r = 6371  # km
    p = pi / 180
 
    a = 0.5 - cos((lat2 - lat1) * p) / 2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return 2 * r * asin(sqrt(a))
