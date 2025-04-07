from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

players = Blueprint('players', __name__)

#------------------------------------------------------------
# Get all players from the system
@players.route('/players', methods=['GET'])
def get_players():
    cursor = db.get_db().cursor()
    cursor.execute('''
        SELECT id, firstName, middleName, lastName, 
               agentId, position, teamId, height, weight, dob, injuryId
        FROM players
    ''')
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Create a new player
@players.route('/players', methods=['POST'])
def create_player():
    new_player_data = request.json
    query = '''
        INSERT INTO players (firstName, middleName, lastName, agentId, position, teamId, height, weight, dob, injuryId)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    data = (
        new_player_data['firstName'],
        new_player_data.get('middleName'),
        new_player_data['lastName'],
        new_player_data['agentId'],
        new_player_data['position'],
        new_player_data['teamId'],
        new_player_data['height'],
        new_player_data['weight'],
        new_player_data['dob'],
        new_player_data.get('injuryId')
    )
    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()
    new_id = cursor.lastrowid
    response = make_response(jsonify({'id': new_id}), 201)
    return response

#------------------------------------------------------------
# Update player info for a particular player.
# The player id should be included in the JSON payload.
@players.route('/players', methods=['PUT'])
def update_player():
    current_app.logger.info('PUT /players route')
    player_info = request.json
    player_id = player_info['id']
    query = '''
        UPDATE players
        SET firstName = %s, middleName = %s, lastName = %s, agentId = %s,
            position = %s, teamId = %s, height = %s, weight = %s, dob = %s, injuryId = %s
        WHERE id = %s
    '''
    data = (
        player_info['firstName'],
        player_info.get('middleName'),
        player_info['lastName'],
        player_info['agentId'],
        player_info['position'],
        player_info['teamId'],
        player_info['height'],
        player_info['weight'],
        player_info['dob'],
        player_info.get('injuryId'),
        player_id
    )
    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()
    return 'player updated!'

#------------------------------------------------------------
# Get detail for a single player identified by player_id
@players.route('/players/<int:player_id>', methods=['GET'])
def get_player(player_id):
    current_app.logger.info(f'GET /players/{player_id} route')
    cursor = db.get_db().cursor()
    cursor.execute('''
        SELECT id, firstName, middleName, lastName, 
               agentId, position, teamId, height, weight, dob, injuryId
        FROM players WHERE id = %s
    ''', (player_id,))
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Delete a player identified by player_id
@players.route('/players/<int:player_id>', methods=['DELETE'])
def delete_player(player_id):
    current_app.logger.info(f'DELETE /players/{player_id} route')
    cursor = db.get_db().cursor()
    cursor.execute("DELETE FROM players WHERE id = %s", (player_id,))
    db.get_db().commit()
    return 'player deleted!'