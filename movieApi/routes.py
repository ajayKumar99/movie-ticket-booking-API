from flask import Blueprint, request, flash
from flask_restful import Resource, Api
from bson.objectid import ObjectId
import datetime
from dateutil import *
from dateutil.tz import *
from .extensions import db

middleware = Blueprint('api', __name__, url_prefix='/api')
api = Api(middleware)

def convert_time(time):
    d = datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M")
    return d

def get_no_of_bookings(time_val):
    n_bookings = db.movie_tickets.tickets.find({
                'timing': time_val
            }).count()
    if n_bookings == 20:
        return False
    return True

class TicketManagementAPI(Resource):
    def post(self):
        req = request.get_json()

        if 'name' not in req or req['name'] == '':
            return {'error': 'Username not provided'}, 400
        if 'phone' not in req or req['phone'] == '':
            return {'error': 'Phone number not provided'}, 400
        if 'timing' not in req or req['timing'] == '':
            return {'error': 'Ticket timing not provided'}, 400

        try:
            time_val = convert_time(req['timing'])
        except ValueError as v:
            return {'error': v.__str__()}

        try:
            if not get_no_of_bookings(time_val):
                return {'error': 'Maximum booking limit for this time exeeded'}, 400
            
            utc_zone = tz.tzutc()
            local_zone = tz.tzlocal()
            expiry_time = time_val
            expiry_time = expiry_time.replace(tzinfo=local_zone)
            expiry_time = expiry_time.astimezone(utc_zone) + datetime.timedelta(hours=8)

            ticket_collection = db.movie_tickets.tickets
            ticket_id = ticket_collection.insert_one({
                'name': req['name'].strip(),
                'phone': req['phone'].strip(),
                'timing': time_val,
                'expiresAt': expiry_time
            })
        except Exception as e:
            flash(e.__str__())
            return {'error': 'Database error. Please try again later'}, 500
        
        return {'message': 'Ticket Booked', 'ticket_id': str(ticket_id.inserted_id)}, 201

    def put(self):
        req = request.get_json()

        if 'ticket_id' not in req or req['ticket_id'] == '':
            return {'error': 'Ticket ID to update not provided'}, 400
        
        if not ObjectId.is_valid(req['ticket_id']):
            return {'error': 'Invalid ticket ID'}, 400

        if 'timing' not in req or req['timing'] == '':
            return {'error': 'Updated time not provided'}, 400

        try:
            time_val = convert_time(req['timing'])
        except ValueError as v:
            return {'error': v.__str__()}

        try:
            ticket_collection = db.movie_tickets.tickets
            exists = ticket_collection.find_one({
                '_id': ObjectId(req['ticket_id'])
            })
            if not exists:
                return {'error': "This ticket doesn't exists"}, 400

            if not get_no_of_bookings(time_val):
                return {'error': 'Maximum booking limit for this time exeeded'}, 400

            utc_zone = tz.tzutc()
            local_zone = tz.tzlocal()
            expiry_time = time_val
            expiry_time = expiry_time.replace(tzinfo=local_zone)
            expiry_time = expiry_time.astimezone(utc_zone) + datetime.timedelta(hours=8)

            ticket_collection.update_one({
                '_id': ObjectId(req['ticket_id'])
            }, {
                '$set': {
                    'timing': time_val,
                    'expiresAt': expiry_time
                }
            })
        except Exception as e:
            flash(e.__str__())
            return {'error': 'Database error. Please try again later'}, 500
        
        return {'message': 'Ticket timing updated', 'ticket_id': req['ticket_id']}, 201

    def get(self):
        req = request.get_json()
        
        if 'ticket_id' in req and req['ticket_id'] != '':
            if not ObjectId.is_valid(req['ticket_id']):
                return {'error': 'Invalid ticket ID'}, 400
            try:
                ticket_collection = db.movie_tickets.tickets
                exists = ticket_collection.find_one({
                    '_id': ObjectId(req['ticket_id'])
                })
                if not exists:
                    return {'error': "Ticket doesn't exists"}
                utc_zone = tz.tzutc()
                local_zone = tz.tzlocal()
                expiry_time = exists['expiresAt']
                expiry_time = expiry_time.replace(tzinfo=utc_zone)
                expiry_time = expiry_time.astimezone(local_zone)

                exists['_id'] = str(exists['_id'])
                exists['timing'] = exists['timing'].strftime("%Y-%m-%dT%H:%M")
                exists['expiresAt'] = expiry_time.strftime("%Y-%m-%dT%H:%M")
                return {"data": exists}, 200
            except Exception as e:
                flash(e.__str__())
                return {'error': 'Database error. Please try again later'}, 500

        if 'timing' not in req or req['timing'] == '':
            return {'error': 'Time for which data to be fetched not provided'}, 400

        payload = []
        
        try:
            ticket_collection = db.movie_tickets.tickets
            tickets = list(ticket_collection.find({
                'timing': convert_time(req['timing'])
            }))

            for ticket in tickets:
                utc_zone = tz.tzutc()
                local_zone = tz.tzlocal()
                expiry_time = ticket['expiresAt']
                expiry_time = expiry_time.replace(tzinfo=utc_zone)
                expiry_time = expiry_time.astimezone(local_zone)

                ticket['_id'] = str(ticket['_id'])
                ticket['timing'] = ticket['timing'].strftime("%Y-%m-%dT%H:%M")
                ticket['expiresAt'] = expiry_time.strftime("%Y-%m-%dT%H:%M")
                payload.append(ticket)

        except Exception as e:
            flash(e.__str__())
            return {'error': 'Database error. Please try again later'}, 500

        return {'tickets': payload}, 200

    def delete(self):
        req = request.get_json()

        if 'ticket_id' not in req or req['ticket_id'] == '':
            return {'error': 'Ticket ID to be deleted not provided'}, 400

        if not ObjectId.is_valid(req['ticket_id']):
            return {'error': 'Invalid ticket ID'}, 400
        
        try:
            ticket_collection = db.movie_tickets.tickets
            exists = ticket_collection.find_one({
                '_id': ObjectId(req['ticket_id'])
            })
            if not exists:
                return {'error': "Ticket doesn't exists"}, 400
            ticket_collection.delete_one({
                '_id': ObjectId(req['ticket_id'])
            })
    
        except Exception as e:
            flash(e.__str__())
            return {'error': 'Database error. Please try again later'}, 500

        return {'message': 'Ticket with id-' + req['ticket_id'] + ' deleted successfully'}, 200


api.add_resource(TicketManagementAPI, '/v1/ticket')