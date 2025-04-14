from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

matches = Blueprint('matches', __name__)

#------------------------------------------------------------
# Get all matches from the system: 

@matches.route('/matches', methods=['GET']) 
def get_all_matches():
    cursor = db.get_db().cursor()
    cursor.execute('''
        SELECT id, homeTeamId, awayTeamId, date, time,
                location, homeScore, awayScore, finalScore 
        FROM matches 
    ''') 
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    return the_response

#------------------------------------------------------------
# Get detail for a single match identified by match_id:

@matches.route('/matches/<int:match_id>', methods=['GET'])
def get_match(match_id):
    current_app.logger.info(f'GET /matches/{match_id} route')
    cursor = db.get_db().cursor()
    cursor.execute('''
        SELECT id, homeTeamId, awayTeamId, date, time,
                location, homeScore, awayScore, finalScore
        FROM matches WHERE id = %s
    ''', (match_id,))
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


#------------------------------------------------------------
# Get detail for all matches of a team identified by team_id:

@matches.route('/matches/<int:match_id>', methods=['GET'])
def get_matches(team_id):
    current_app.logger.info(f'GET /matches/{team_id} route')
    cursor = db.get_db().cursor()
    cursor.execute('''
        SELECT id, homeTeamId, awayTeamId, date, time,
                location, homeScore, awayScore, finalScore
        FROM matches WHERE homeTeamid = %s OR awayTeamId = %s 
    ''', (team_id,))
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
#Put a new match into the system:

@matches.route('/matches', methods=['POST'])
def create_match():
    match_data = request.json
    query = """
        INSERT INTO matches (homeTeamId, awayTeamId, date, time, location, homeScore, awayScore, finalScore)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    data = (
        match_data.get('homeTeamId'),
        match_data.get('awayTeamId'),
        match_data.get('date'),
        match_data.get('time'),
        match_data.get('location'),
        match_data.get('homeScore'),
        match_data.get('awayScore'),
        match_data.get('finalScore')
    )
    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()
    new_id = cursor.lastrowid
    response = make_response(jsonify({"id": new_id}), 201)
    return response
#------------------------------------------------------------
# Do dynamic partial update of a match info for a match given the id:

@matches.route('/matches/<int:match_id>', methods=['PATCH'])
def patch_match(match_id):
    match_data = request.json
    fields = []
    values = []
    allowed_fields = ['homeScore', 'awayScore', 'finalScore']
    for field in allowed_fields:
        if field in match_data:
            fields.append(f"{field} = %s")
            values.append(match_data[field])
    if not fields:
        return make_response(jsonify({"error": "No valid fields provided"}), 400)
    values.append(match_id)
    query = "UPDATE matches SET " + ", ".join(fields) + " WHERE id = %s"
    cursor = db.get_db().cursor()
    cursor.execute(query, tuple(values))
    db.get_db().commit()
    response = make_response(jsonify({"message": "The following fields were updated for match id" + str(match_id) + ": " + ", ".join(fields)}))
    response.status_code = 200
    return response