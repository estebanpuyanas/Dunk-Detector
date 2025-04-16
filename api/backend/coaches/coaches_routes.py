from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

coaches = Blueprint('coaches', __name__)

#------------------------------------------------------------
# Get all coaches from the system:

@coaches.route('/coaches', methods=['GET'])
def get_players():
    cursor = db.get_db().cursor()
    cursor.execute('''
        SELECT id, firstName, middleName, lastName, mobile, email, teamId, agentId
        FROM coaches
    ''')
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response