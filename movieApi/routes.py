from flask import Blueprint, request
from flask_restful import Resource, Api
from .extensions import db

middleware = Blueprint('api', __name__, url_prefix='/api')
api = Api(middleware)

class BookMovieTicket(Resource):
    def post(self):
        req = request.get_json()

        if 'name' not in req:
            return {'error': 'Username not provided'}, 400
        if 'phone' not in req:
            return {'error': 'Phone number not provided'}, 400
        if 'timing' not in req:
            return {'error': 'Ticket timing not provided'}, 400

        try:
            ticket_collection = db.movie_tickets.tickets
            ticket_id = ticket_collection.insert_one({
                'name': req['name'],
                'phone': req['phone'],
                'timing': req['timing']
            })
        except Exception as e:
            return {'error': e.__str__()}, 500
        
        return {'message': 'Ticket Booked', 'ticket_id': str(ticket_id.inserted_id)}, 201

api.add_resource(BookMovieTicket, '/book')
