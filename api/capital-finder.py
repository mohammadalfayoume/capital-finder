from http.server import BaseHTTPRequestHandler
from urllib import parse # it allow me to send a request with query params
import requests
class handler(BaseHTTPRequestHandler):

  def do_GET(self):
    s=self.path # /api/capital_finder?capital="amman"
    print(s)
    url_components=parse.urlsplit(s) # to separate query from the path
    query_string_list=parse.parse_qsl(url_components)
    dictionary=dict(query_string_list)

    if 'country' in dictionary:
      country=dictionary['country']
      url= f'https://restcountries.com/v3.1/name/{country}'
      req= requests.get(url)
      data=req.json()
      capital=data[0]['capital'][0]
      message= f'The capital of {country} is {capital}'
    else:
      message= "Invalid country name, try again"

    if 'capital' in dictionary:
      capital=dictionary['capital']
      url= f'https://restcountries.com/v3.1/capital/{capital}'
      req= requests.get(url)
      data=req.json()
      country=data[0]['name']['common']
      message= f'{capital} is the capital of {country}'
    else:
      message= "Invalid country name, try again"



    self.send_response(200)
    self.send_header('Content-type', 'text/plain')
    self.end_headers()
    self.wfile.write(message.encode())
    return