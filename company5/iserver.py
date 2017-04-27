import argparse
from datetime import datetime
import json
from flask import Flask, jsonify, request
from geopy.geocoders import Nominatim
from geopy.distance import vincenty

# global variables
coffee_shop_db = {}
geolocator = Nominatim()

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, Coffee Shop!"

# show all the data in the coffee shop database and total number of shops
@app.route('/selectall', methods=['GET'])
def get_tasks_selectall():
    response = {
        "total": len(coffee_shop_db),
        "data": coffee_shop_db
    }
    return jsonify(response)

# display the shop data in the database, for a given shop_id
@app.route('/select/<int:shop_id>', methods=['GET'])
def get_tasks_select(shop_id):
    if shop_id in coffee_shop_db:
        response = {
            'message': 'found',
            'data':    coffee_shop_db[shop_id]
        }
    else:
        response = {
            'message': 'not found'
        }
    
    return jsonify(response)

# delete the shop based on shop_id from coffee shop database
@app.route('/delete/<int:shop_id>', methods=['GET'])
def get_tasks_delete(shop_id):
    if shop_id in coffee_shop_db:
        old_count = len(coffee_shop_db)
        del coffee_shop_db[shop_id]
        response = {
            "message": "deleted",
            "old_db_count": old_count,
            "new_db_count": len(coffee_shop_db)
        }
    else:
        response = {
            'message': 'not found'
        }

    return jsonify(response)

# update shop data in the database, for a given shop_id
@app.route('/update/<int:shop_id>', methods=['POST'])
def get_tasks_update(shop_id):
    if shop_id in coffee_shop_db:
        old_data = coffee_shop_db[shop_id].copy()
        new_data = {
            "id": shop_id,
            'name': request.json.get("name", old_data["name"]),
            'address': request.json.get("address", old_data["address"]),
            'latitude': request.json.get("latitude", old_data["latitude"]),
            'longitude': request.json.get("longitude", old_data["longitude"]),
        }

        coffee_shop_db[shop_id] = new_data

        response = {
            "message": "updated",
            "old_data": old_data,
            "new_data": new_data
        }
    else:
        response = {
            'message': 'not found'
        }

    return jsonify(response)

# for a given address, find the nearest shop in the database
@app.route('/find_nearest', methods=['POST'])
def get_tasks_find_nearest():
    address = request.json.get("address")

    location_geo = None
    try:
        location = geolocator.geocode(address)
        location_geo = (location.latitude, location.longitude)
    except:
        response = {
            "address": address,
            "message": "address not valid" 
        }    
 
    if location_geo:
        # find the shop with min distance in miles
        nearest_shop_miles = 100000
        for id in coffee_shop_db:
            shop_geo = (coffee_shop_db[id]["latitude"], coffee_shop_db[id]["longitude"])
            shop_distance = vincenty(location_geo, shop_geo).miles
     
            if shop_distance < nearest_shop_miles:
                nearest_shop_miles = shop_distance
                nearest_shop = coffee_shop_db[id]

        response = {
            "address": address,
            "nearest_shop": nearest_shop,
            "message": "found coffee shop"
        }

    return jsonify(response)

# 
def get_args():
    parser = argparse.ArgumentParser(
            description = "coffee shop database",
            epilog = "something"
          )
    parser.add_argument("-f", "--input-file", help="Input File for initialize the database", dest="i_file", required=False)

    parser.set_defaults(i_file="location.csv")

    return parser.parse_args()

# initialize the shop database from file
def load_db (afile):
    try:
        # assumption: input file in current directory
        i_data = open(afile, 'r').readlines()
    except IOError as e:
        print "read file error"
        return

    db = {}

    for line in i_data:
        # the input data example:
        ## id, name, address, latitude, longitude
        ## 1, Equator Coffees & Teas, 986 Market St, 37.782394430549445, -122.40997343121123

        #print line
        o_message = ""
        i_fields = line.rstrip('\n').decode('utf-8').split(', ')
        #print i_fields[1]
        coffee_shop = {
            'id':   int(i_fields[0]),
            'name': i_fields[1],
            'address': i_fields[2],
            'latitude': i_fields[3],
            'longitude': i_fields[4]
        }

        db[int(i_fields[0])] = coffee_shop

    return db

#
if __name__ == '__main__':
    args = get_args()

    coffee_shop_db = load_db (args.i_file)
    print "Coffee Shop initiated in database"
    #print(json.dumps(coffee_shop_db, indent=2))

    app.run(debug=True)
