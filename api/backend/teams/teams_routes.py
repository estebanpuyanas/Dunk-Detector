from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

teams = Blueprint('teams', __name__)

#------------------------------------------------------------
# Get roster for a team identified by team name:

@teams.route('/teams/<int:name>', methods=['GET'])
def get_roster(name):
    cursor = db.get_db().cursor()
    cursor.execute('''
        SELECT id, firstName, middleName, lastName, agentId, 
                   Height, Weight, position, DOB, teamId, injuryId
        FROM players p
        JOIN (SELECT name, id
        FROM teams) t on t.id = p.teamId
        WHERE name = %s
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
        SELECT name, isCollege, isProfessional
        FROM teams
    ''')

    theData = cursor.fetchall()
    try:
        return jsonify(formatted_data), 200
    except Exception as e:
        # Add error logging
        current_app.logger.error(f"Error getting teams: {str(e)}")
        return jsonify({"error": str(e)}), 500