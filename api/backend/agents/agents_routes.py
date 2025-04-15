from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

agents = Blueprint('agents', __name__)


@agents.route('/agents/player/<string:name>', methods=['GET'])
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



@agents.route('/agents/coach/<string:name>', methods=['GET'])
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