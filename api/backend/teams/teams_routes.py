from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

teams = Blueprint('teams', __name__)

#------------------------------------------------------------
# Get roster for a team identified by team name:

@teams.route('/teams/<string:name>', methods=['GET'])
def get_roster(name):
    current_app.logger.info(f'GET /teams/{name} route')
    cursor = db.get_db().cursor()
    cursor.execute('''
        SELECT p.id, p.firstName, p.middleName, p.lastName, p.agentId, 
               p.Height, p.Weight, p.position, p.DOB, p.teamId, p.injuryId
        FROM players p
        JOIN teams t on t.id = p.teamId
        WHERE t.name = %s
    ''', (name,))
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response
#------------------------------------------------------------
# Get list for a teams and their ids:

@teams.route('/teams', methods=['GET'])
def get_teams():

    cursor = db.get_db().cursor()
    cursor.execute('''
        SELECT id, name, isCollege, isProfessional
        FROM teams
    ''')

    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response
