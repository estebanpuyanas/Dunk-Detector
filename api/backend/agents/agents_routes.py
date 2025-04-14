from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

agents = Blueprint('agents', __name__)

@agents.route('/agents/<int:player_id>', methods=['GET'])
def get_agent_player(player_id):
    current_app.logger.info(f'GET/agents/player/{player_id} route')
    cursor = db.get_db().cursor()
    cursor.execute('''
        SELECT id, firstName, middleName, lastName, mobile, email
        FROM agents a
        JOIN (SELECT agentId
              FROM players
              WHERE id = %) p ON a.id = p.agentId
    ''', (player_id,))
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

@agents.route('/agents/<int:coach_id>', methods=['GET'])
def get_agent_coach(coach_id):
    current_app.logger.info(f'GET/agents/coach/{coach_id} route')
    cursor = db.get_db().cursor()
    cursor.execute('''
        SELECT id, firstName, middleName, lastName, mobile, email
        FROM agents 
        JOIN (SELECT id as player_id
              FROM players)
        WHERE coach_id = %s
    ''', (coach_id,))
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response