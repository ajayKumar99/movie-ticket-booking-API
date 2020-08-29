from flask import Blueprint, request, flash
from flask_restful import Resource, Api
from bson.objectid import ObjectId
from .extensions import db

middleware = Blueprint('api', __name__, url_prefix='/api')
api = Api(middleware)

def convert_time(time):
    hh, mm = time.split(':')
    return hh.strip() + ':' + mm.strip()

def update_time(time_val):
    n_bookings = db.movie_tickets.tickets.find({
                'timing': time_val
            }).count()
    if n_bookings == 20:
        return False
    return True


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

        try:
            if not update_time(time_val):
                return {'error': 'Maximum booking limit for this time exeeded'}, 400
            
            ticket_collection = db.movie_tickets.tickets
            ticket_id = ticket_collection.insert_one({
                'name': req['name'].strip(),
                'phone': req['phone'].strip(),
                'timing': time_val
            })
        except Exception as e:
            flash(e.__str__())
            return {'error': 'Database error. Please try again later'}, 500
        
        return {'message': 'Ticket Booked', 'ticket_id': str(ticket_id.inserted_id)}, 201

api.add_resource(BookMovieTicket, '/book')

class UpdateTicket(Resource):
    def put(self):
        req = request.get_json()

        if 'ticket_id' not in req:
            return {'error': 'Ticket ID to update not provided'}, 400
        
        if not ObjectId.is_valid(req['ticket_id']):
            return {'error': 'Invalid ticket ID'}, 400

        if 'timing' not in req:
            return {'error': 'Updated time not provided'}, 400

        time_val = convert_time(req['timing'])

        try:
            ticket_collection = db.movie_tickets.tickets
            exists = ticket_collection.find_one({
                '_id': ObjectId(req['ticket_id'])
            })
            if not exists:
                return {'error': "This ticket doesn't exists"}, 400

            if not update_time(time_val):
                return {'error': 'Maximum booking limit for this time exeeded'}, 400

            ticket_collection.update_one({
                '_id': ObjectId(req['ticket_id'])
            }, {
                '$set': {
                    'timing': req['timing']
                }
            })
        except Exception as e:
            flash(e.__str__())
            return {'error': 'Database error. Please try again later'}, 500
        
        return {'message': 'Ticket timing updated', 'ticket_id': req['ticket_id']}, 201

api.add_resource(UpdateTicket, '/update_timing')

class GetTicketsByTime(Resource):
    def get(self):
        req = request.get_json()
        payload = []
        if 'timing' not in req:
            return {'error': 'Time for which data to be fetched not provided'}, 400
        
        try:
            ticket_collection = db.movie_tickets.tickets
            tickets = list(ticket_collection.find({
                'timing': req['timing']
            }))

            for ticket in tickets:
                ticket['_id'] = str(ticket['_id'])
                payload.append(ticket)

        except Exception as e:
            flash(e.__str__())
            return {'error': 'Database error. Please try again later'}, 500

        return {'tickets': payload}

api.add_resource(GetTicketsByTime, '/get_tickets_by_time')

class DeleteTicket(Resource):
    def delete(self):
        req = request.get_json()

        if 'ticket_id' not in req:
            return {'error': 'Ticket ID to be deleted not provided'}, 400

        if not ObjectId.is_valid(req['ticket_id']):
            return {'error': 'Invalid ticket ID'}, 400
        
        try:
            ticket_collection = db.movie_tickets.tickets
            exists = ticket_collection.find_one({
                '_id': ObjectId(req['ticket_id'])
            })
            if not exists:
                return {'error': "Ticket doesn't exists"}
            ticket_collection.delete_one({
                '_id': ObjectId(req['ticket_id'])
            })
    
        except Exception as e:
            flash(e.__str__())
            return {'error': 'Database error. Please try again later'}, 500

        return {'message': 'Ticket with id-' + req['ticket_id'] + ' deleted successfully'}
        
api.add_resource(DeleteTicket, '/delete_ticket')

class GetTicketDetails(Resource):
    def get(self):
        req = request.get_json()

        if 'ticket_id' not in req:
            return {'error': 'Ticket ID to be deleted not provided'}, 400

        if not ObjectId.is_valid(req['ticket_id']):
            return {'error': 'Invalid ticket ID'}, 400
        try:
            ticket_collection = db.movie_tickets.tickets
            exists = ticket_collection.find_one({
                '_id': ObjectId(req['ticket_id'])
            })
            if not exists:
                return {'error': "Ticket doesn't exists"}
            exists['_id'] = str(exists['_id'])
            return {"data": exists}
        except Exception as e:
            flash(e.__str__())
            return {'error': 'Database error. Please try again later'}, 500

api.add_resource(GetTicketDetails, '/get_ticket')
        