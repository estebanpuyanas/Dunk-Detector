from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

gm = Blueprint('gm', __name__)

#------------------------------------------------------------
# Get all gms from the system: 

@gm.route('/gm', methods=['GET'])
def get_all_gm():
    cursor = db.get_db().cursor()
    cursor.execute('''
        SELECT g.id, g.firstName, g.middleName, g.lastName, g.teamId, t.name
        FROM general_managers g
        JOIN teams t on g.teamId = t.id 
    ''') 
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Get detail for a gm identified by gm_id:

@gm.route('/gm/<string:name>', methods=['GET'])
def get_gm_name(name):
    name = name.split()
    first_name = name[0]
    last_name = name[-1]
    current_app.logger.info(f'GET /gm/{name} route')
    cursor = db.get_db().cursor()
    cursor.execute('''
        SELECT id, firstName, middleName, lastName, mobile,
                email, teamId
        FROM general_managers
        WHERE firstName = %s AND lastName = %s
    ''', (first_name, last_name))
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


#------------------------------------------------------------
# Get detail for a gm identified by team name:

@gm.route('/gm/teams/<string:name>', methods=['GET'])
def get_gm_team(name):
    current_app.logger.info(f'GET /gm/teams/{name} route')
    cursor = db.get_db().cursor()
    cursor.execute('''
        SELECT g.id, g.firstName, g.middleName, g.lastName, g.mobile, g.email, g.teamId
        FROM general_managers g
        JOIN teams t ON g.id = t.generalManagerID
        WHERE t.name = %s
    ''', (name))
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


#------------------------------------------------------------
# Gets players agents:

@gm.route('/gm/agents/player/<string:name>', methods=['GET'])
def get_agent_player(name):
    name = name.split()
    first_name = name[0]
    last_name = name[-1]
    current_app.logger.info(f'GET/agents/player/{name} route')
    cursor = db.get_db().cursor()
    cursor.execute('''
        SELECT a.id, a.firstName, a.middleName, a.lastName, a.mobile, a.email
        FROM agents a
        JOIN players p ON a.id = p.agentId
        WHERE p.firstName = %s AND p.lastName = %s
    ''', (first_name, last_name))
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Gets coaches agents:

@gm.route('/gm/agents/coach/<string:name>', methods=['GET'])
def get_agent_coach(name):
    name = name.split()
    first_name = name[0]
    last_name = name[-1]
    current_app.logger.info(f'GET/agents/coach/{name} route')
    cursor = db.get_db().cursor()
    cursor.execute('''
        SELECT a.id, a.firstName, a.middleName, a.lastName, a.mobile, a.email
        FROM agents a
        JOIN coaches c ON a.id = c.agentId
         WHERE c.firstName = %s AND c.lastName = %s
    ''', (first_name, last_name))
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Get list of coaches:

@gm.route('/gm/players', methods=['GET'])
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
