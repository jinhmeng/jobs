## Project

The goal of this project is to create an API for finding the nearest g shop by providing an
address.

A list of g shops with their geo locations are stored in a text file. The file (default: locations.csv) is in comma separated value format with 5 columns and looks like:
id, name, address, latitude, longitude

After reading in the initial data set, the script build a server with a REST API that can 
1) create a new shop, return the details of a shop given its id, update, or delete a shop. 
2) take in an address and returns the nearest shop that is currently in the list. 
Return the response in JASON

Create:
Accepts name, address, latitude, and longitude, adds a new g shop to the data set, and returns the id of the new  shop.

Read:
Accepts an id and returns the id, name, address, latitude, and longitude of the g shop with that id, or an appropriate error if it is not found.

Update:
Accepts an id and new values for the name, address, latitude, or longitude fields, updates the g shop with that id, or returns an appropriate error if it is not found.

Delete:
Accepts an id and deletes the g shop with that id, or returns an error if it is not found

Find nearest:
Accepts an address and returns the closest g shop by straight line distance.

## Installation

The following python libraries need to be pre-installed:
1. pip install flask
2. pip install geopy

## Start the Server

python iserver.py -f <text-file-with-store-information>

Example:

jmeng$ python iserver.py -f location.csv
Data initiated in database
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
Data initiated in database
 * Debugger is active!
 * Debugger PIN: 516-434-060


## REST API

1) Display all store data in the database
curl -i -H "Content-Type: application/json" http://localhost:5000/selectall

2) Display store data for a given store id
curl -i -H "Content-Type: application/json" http://localhost:5000/select/<store-id>

Example:
jmeng$ curl -i -H "Content-Type: application/json" http://localhost:5000/select/10
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 212
Server: Werkzeug/0.12.1 Python/2.7.10
Date: Thu, 27 Apr 2017 21:11:23 GMT

{
  "data": {
    "address": "1 Ferry Building Ste 7", 
    "id": 10, 
    "latitude": "37.79590475625579", 
    "longitude": "-122.39393759555746", 
    "name": "Blue Bottle Coffee"
  }, 
  "message": "found"
}

jmeng$ curl -i -H "Content-Type: application/json" http://localhost:5000/select/100
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 29
Server: Werkzeug/0.12.1 Python/2.7.10
Date: Thu, 27 Apr 2017 21:13:11 GMT

{
  "message": "not found"
}

3) Delete a store from database for a given store id
curl -i -H "Content-Type: application/json" http://localhost:5000/delete/<store-id>

Example:
jmeng$ curl -i -H "Content-Type: application/json" http://localhost:5000/delete/1

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 42
Server: Werkzeug/0.12.1 Python/2.7.10
Date: Thu, 27 Apr 2017 21:16:52 GMT

{
  "message": "deleted",
  "new_db_count": 47, 
  "old_db_count": 48
}

4) Update store data for a given store id
curl -i -H "Content-Type: application/json" -X POST -d '<store-data-in-json>' http://localhost:5000/update/<store-id>

Example:
jmeng$ curl -i -H "Content-Type: application/json" -X POST -d '{"address":"6 moraga way", "name":"new name"}' http://localhost:5000/update/1
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 384
Server: Werkzeug/0.12.1 Python/2.7.10
Date: Thu, 27 Apr 2017 21:26:50 GMT

{
  "message": "updated", 
  "new_data": {
    "address": "6 moraga way", 
    "id": 1, 
    "latitude": "37.782394430549445", 
    "longitude": "-122.40997343121123", 
    "name": "new name"
  }, 
  "old_data": {
    "address": "986 Market St", 
    "id": 1, 
    "latitude": "37.782394430549445", 
    "longitude": "-122.40997343121123", 
    "name": "Equator Coffees & Teas"
  }
}

5) Find the nearest shop for a given address
curl -i -H "Content-Type: application/json" -X POST -d '{"address":"<address>"}' http://localhost:5000/find_nearest

Example:
jmeng$ curl -i -H "Content-Type: application/json" -X POST -d '{"address":"252 Guerrero St, San Francisco, CA 94103"}' http://localhost:5000/find_nearest
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 283
Server: Werkzeug/0.12.1 Python/2.7.10
Date: Thu, 27 Apr 2017 22:12:13 GMT

{
  "address": "252 Guerrero St, San Francisco, CA 94103", 
  "message": "found coffee shop", 
  "nearest_shop": {
    "address": "375 Valencia St", 
    "id": 28, 
    "latitude": "37.76702438676065", 
    "longitude": "-122.42195860692624", 
    "name": "Four Barrel Coffee"
  }
}

