from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import uuid

app = Flask(__name__)
api = Api(app)

root_uuid = uuid.UUID()

@app.before_first_request
def root_uuid_check():
    try:
        uuid_file = open("uuid")
        root_uuid = uuid.UUID(uuid_file.read())
        uuid_file.close()
    except:
        uuid_file = open("uuid", "wt")
        root_uuid = uuid.uuid4()
        uuid_file.write(str(root_uuid))

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

        place_id = 0


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
            }, 400
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
        parser = reqparse.RequestParser(bundle_errors=True)

        parser.add_argument('user', required=True) 
        parser.add_argument('rating', type=int, required=True)
        parser.add_argument('text', required=True)
        parser.add_argument('place_id', required=True)

        args=parser.parse_args()

        user = args['user']
        rating = args['rating']
        text = args['text']
        place_id = args['place_id']

        review_id = hash(user) + hash(text) + int(rating) + int(place_id) # allows user to post updated review if place improves or declines, but not duplicate reviews

        data = pd.read_csv('csv/places.csv')
        data = data.to_dict()

        if str(place_id) in list(data['place_id']): # verifies the place the review is for exists in db
            return {
                'message': f"Place id {place_id} does not exist."
            }, 400
        
        data.clear()
        data = pd.read_csv('csv/reviews.csv')
        
        if review_id in list(data['review_id']): # verifies review is not a duplicate
            return {
                'message': f"Review id {review_id} already exists (is this a duplicate review?)."
            }, 400

        else:
            new_data = pd.DataFrame({
                'review_id': [review_id],
                'user': [user],
                'rating': [rating],
                'text': [text]
            })
             # add the newly provided values
            data = data.append(new_data, ignore_index=True)
            # save back to CSV
            data.to_csv('csv/reviews.csv', index=False)
            return {'data': data.to_dict()}, 200  # returns updated data with 200 OK

    def put(self):
        return

    def delete(self):
        return
        
    pass

api.add_resource(Places, '/places') # /places is point of entry for locations
api.add_resource(Reviews, '/reviews') # /reviews is point of entry for reviews

if __name__ == '__main__':
    app.run()