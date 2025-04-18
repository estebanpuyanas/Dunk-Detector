from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db
import pymysql.cursors
import datetime

players = Blueprint('players', __name__)

#------------------------------------------------------------
# Get all players from the system:
# TESTED - PASSING POSTMAN REQUEST

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
# Create a new player:
# TESTED - PASSING POSTMAN REQUEST

@players.route('/players', methods=['POST'])
def create_player():
    player_data = request.json
    query = """
        INSERT INTO players (firstName, middleName, lastName, agentId, position, teamId, height, weight, dob, injuryId)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    data = (
        player_data.get('firstName'),
        player_data.get('middleName'),
        player_data.get('lastName'),
        player_data.get('agentId'),
        player_data.get('position'),
        player_data.get('teamId'),
        player_data.get('height'),
        player_data.get('weight'),
        player_data.get('dob'),
        player_data.get('injuryId')
    )
    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()
    new_id = cursor.lastrowid
    response = make_response(jsonify({"id": new_id}), 201)
    return response
#------------------------------------------------------------
# Update player info for a particular player:
# The player id should be included in the JSON payload.
# TESTED - PASSING POSTMAN REQUEST

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
# Get detail for a single player identified by player_id:
# TESTED - PASSING POSTMAN REQUEST

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
# Get detail for a single player identified by team_id:
# TESTED - PASSING POSTMAN REQUEST

@players.route('/team_players/<int:team_id>', methods=['GET'])
def get_team_player(team_id):
    current_app.logger.info(f'GET /players/{team_id} route')
    cursor = db.get_db().cursor()
    cursor.execute('''
        SELECT id, firstName, middleName, lastName, 
               agentId, position, teamId, height, weight, dob, injuryId
        FROM players WHERE teamId = %s
    ''', (team_id,))
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response    
#------------------------------------------------------------
# Delete a player identified by player_id:
# TESTED - PASSING POSTMAN REQUEST

@players.route('/players/<int:player_id>', methods=['DELETE'])
def delete_player(player_id):
    current_app.logger.info(f'DELETE /players/{player_id} route')
    cursor = db.get_db().cursor()
    cursor.execute("DELETE FROM players WHERE id = %s", (player_id,))
    db.get_db().commit()
    return 'player deleted!'
#------------------------------------------------------------
# Update a player's information partially:
# TESTED - PASSING POSTMAN REQUEST (ONLY UPDATED 2 FIELDS, WILL NEED INCREMENTAL TESTING)

@players.route('/players/<int:player_id>', methods=['PATCH'])
def patch_player(player_id):
    player_data = request.json
    # Build update query dynamically based on sent keys.
    fields = []
    values = []
    allowed_fields = ['firstName', 'middleName', 'lastName', 'agentId', 'position', 'teamId', 'height', 'weight', 'dob', 'injuryId']
    for field in allowed_fields:
        if field in player_data:
            fields.append(f"{field} = %s")
            values.append(player_data[field])
    if not fields:
        return make_response(jsonify({"error": "No valid fields provided"}), 400)
    values.append(player_id)
    query = "UPDATE players SET " + ", ".join(fields) + " WHERE id = %s"
    cursor = db.get_db().cursor()
    cursor.execute(query, tuple(values))
    db.get_db().commit()
    response = make_response(jsonify({"message": "Player partially updated"}))
    response.status_code = 200
    return response
#------------------------------------------------------------

@players.route('/playerStats_minutes', methods=['GET'])
def get_playersStats_minutes():
    try:
        # Retrieve the minimum play minutes from the query parameters (default to 0)
        min_minutes = request.args.get('min_minutes', default=0, type=int)
    
        # Use dictionary cursor for JSON serialization ease
        cursor = db.get_db().cursor(pymysql.cursors.DictCursor)
    
        query = '''
            SELECT
                P.firstname,
                P.lastname,
                S.*,
                m.date AS match_date
            FROM players P
            JOIN statistics S ON P.id = S.playerId
            JOIN matches m ON S.matchId = m.id
            WHERE S.totalPlayTime >= SEC_TO_TIME(%s)
            ORDER BY m.date DESC;
        '''
    
        cursor.execute(query, (min_minutes * 60,))
        theData = cursor.fetchall()

        for row in theData:
            for key, value in row.items():
                if isinstance(value, datetime.timedelta):
                    row[key] = str(value) 

    
        return jsonify(theData), 200

    except Exception as e:
        current_app.logger.exception("Error fetching player stats minutes")
        # Return the error message in the JSON response for debugging purposes
        return jsonify({"error": str(e)}), 500