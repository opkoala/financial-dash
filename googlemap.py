# Citation for the usage of using googlemaps from python
# Date Nov/15/2024
# Adapted From
#https://github.com/googlemaps/google-maps-services-python/tree/master/googlemaps

# Citation for the usage of creating a geocode
# Date Nov/15/2024
# Adapted From
#https://developers.google.com/maps/documentation/geocoding/requests-geocoding

#Citation for the geocoding addresses using google maps api
#Date Nov/15/2024
#Adapted from
#https://learn-sims.org/geospatial/geocoding-addresses-using-the-google-maps-api/

#Citation for HTTP Status code in microservices environemnts
#Date Nov/16/2024
#Adapted from
#https://dev.to/rbravo/understanding-http-status-codes-in-microservice-environments-a-guide-to-200-201-400-401-404-and-500-43i7

#Citation for HTTP Methods
#Date Nov/16/2024
#Adapted from
#https://restfulapi.net/http-methods/

import googlemaps
from flask import Flask, jsonify, request

app = Flask(__name__)

# Initialize the Google Maps client with API key
gmaps = googlemaps.Client(key="")

@app.route("/", methods=["GET"])
def index():
    """Create the index page and notify if the server is running"""
    return "Server is running!"

@app.route('/get_coordinates', methods=['GET'])
def get_coordinates():
    """Get coordinates where query is the parameter"""
    query = request.args.get('map_query')
    
    # Print the received query
    print(f"Received {query}")
    
    if query:
        geocode_result = gmaps.geocode(query)
        
        if geocode_result:
            location = geocode_result[0]['geometry']['location']
            return jsonify({'latitude': location['lat'], 'longitude': location['lng']})
        else:
            # If geocode result is empty or invalid
            return jsonify({"error": "Location does not exist"}), 404
    else:
        # If query is missing or invalid
        return jsonify({"error": "Invalid data or incorrect parameters"}), 400


if __name__ == '__main__':
    app.run(port=50215)