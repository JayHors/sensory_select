from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast

app = Flask(__name__)
api = Api(app)

class Places(Resource):
    def get(self):
        data = pd.read_csv('csv/places.csv')
        data = data.to_dict()
        return {'data': data}, 200
    
    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)

        parser.add_argument('name', required=True) 
        parser.add_argument('lat', type=float, required=True)
        parser.add_argument('long', type=float, required=True)

        args=parser.parse_args()

        place_name = args['name']
        place_lat = args['lat']
        place_long = args['long']
        place_name_hash = hash(place_name)
        place_id = int(place_lat) + int(place_long) + place_name_hash


        new_data = pd.DataFrame({
            'place_id': [place_id],
            'name': [place_name],
            'lat_long': [[place_lat, place_long]],
            'reviews': [[]]
        })

        data = pd.read_csv('csv/places.csv')
        if place_id in list(data['place_id']):
            return {
                'message': f"Place id {place_id} already exists."
            }, 401
        else:
            # add the newly provided values
            data = data.append(new_data, ignore_index=True)
            # save back to CSV
            data.to_csv('csv/places.csv', index=False)
            return {'data': data.to_dict()}, 200  # return data with 200 OK
    
    def put(self):
        return
    
    def delete(self):
        return

    pass

class Reviews(Resource):
    def get(self):
        data = pd.read_csv('csv/reviews.csv')
        data = data.to_dict()
        return {'data': data}, 200
    
    def post(self):
        return

    def put(self):
        return

    def delete(self):
        return
        
    pass

api.add_resource(Places, '/places') # /places is point of entry for locations
api.add_resource(Reviews, '/reviews') # /reviews is point of entry for reviews

if __name__ == '__main__':
    app.run()