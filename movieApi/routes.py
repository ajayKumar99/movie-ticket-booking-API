from flask import Blueprint, request
from flask_restful import Resource, Api
from .extensions import db

middleware = Blueprint('api', __name__, url_prefix='/api')
api = Api(middleware)

def convert_time(time):
    hh, mm = time.split(':')
    return hh.strip() + ':' + mm.strip()


class BookMovieTicket(Resource):
    def post(self):
        req = request.get_json()

        if 'name' not in req:
            return {'error': 'Username not provided'}, 400
        if 'phone' not in req:
            return {'error': 'Phone number not provided'}, 400
        if 'timing' not in req:
            return {'error': 'Ticket timing not provided'}, 400

        time_val = convert_time(req['timing'])
        print(time_val)

        try:
            timing_map = db.movie_tickets.timing_map
            exists = timing_map.find_one({
                'time': time_val
            })
            if exists:
                if exists['bookings'] == 20:
                    return {'error': 'Maximum booking limit for this time exeeded'}, 400
            timing_map.update_one({
                    'time': time_val
                }, {
                    '$inc': {
                        'bookings': 1
                    }
                }, upsert=True)
            ticket_collection = db.movie_tickets.tickets
            ticket_id = ticket_collection.insert_one({
                'name': req['name'].strip(),
                'phone': req['phone'].strip(),
                'timing': time_val
            })
        except Exception as e:
            return {'error': e.__str__()}, 500
        
        return {'message': 'Ticket Booked', 'ticket_id': str(ticket_id.inserted_id)}, 201

api.add_resource(BookMovieTicket, '/book')
