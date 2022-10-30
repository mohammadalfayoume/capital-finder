from http.server import BaseHTTPRequestHandler
from urllib import parse # it allow me to send a request with query params
import requests
class handler(BaseHTTPRequestHandler):

  def do_GET(self):
    s=self.path # /api/capital_finder?capital="amman"
    url_components=parse.urlsplit(s) # to separate query from the path
    query_string_list=parse.parse_qsl(url_components.query)
    dictionary=dict(query_string_list)

    if 'country' not in dictionary and 'capital' not in dictionary:
      message="please, provide us with country or capital query!!"
      
    if 'country' in dictionary:
      country=dictionary['country']
      url= f'https://restcountries.com/v3.1/name/{country}'
      req= requests.get(url)
      data=req.json()
      if data["message"]=='Not Found':
        message= "Invalid country name, try again"
        self.send_response(404)
      else:
        capital=data[0]['capital'][0]
        message= f'The capital of {country.capitalize()} is {capital}'
        self.send_response(200)

    if 'capital' in dictionary:
      capital=dictionary['capital']
      url= f'https://restcountries.com/v3.1/capital/{capital}'
      req= requests.get(url)
      data=req.json()
      if data["message"]=='Not Found':
        message= "Invalid capital name, try again"
        self.send_response(404)
      else:
        country=data[0]['name']['common']
        message= f'{capital.capitalize()} is the capital of {country}'
        self.send_response(200)

    
    self.send_header('Content-type', 'text/plain')
    self.end_headers()
    self.wfile.write(message.encode())
    return