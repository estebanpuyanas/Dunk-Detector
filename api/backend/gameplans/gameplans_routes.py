from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

gameplans = Blueprint('gameplans', __name__)

#------------------------------------------------------------
# Get all game plans from the system:
# TESTED - PASSING POSTMAN REQUEST

@gameplans.route('/gameplans', methods=['GET'])
def get_gameplans():
    cursor = db.get_db().cursor()
    cursor.execute('''
        SELECT id, matchId, coachId, planDate, content
        FROM gameplans
    ''')
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Put a new game plan into the system:

@gameplans.route('/gameplans', methods=['POST'])
def create_gameplan():
    gameplan_data = request.json
    query = """
        INSERT INTO gameplans (matchId, coachId, planDate, content)
        VALUES (%s, %s, %s, %s)
    """
    data = (
        gameplan_data.get('matchId'),
        gameplan_data.get('coachId'),
        gameplan_data.get('planDate'),
        gameplan_data.get('content')
    )
    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()
    new_id = cursor.lastrowid
    response = make_response(jsonify({"id": new_id}), 201)
    return response
#------------------------------------------------------------
# Update game plan info given the id
@gameplans.route('/gameplans', methods=['PUT'])
def update_gameplan(gameplan_id):
    current_app.logger.info('PUT /gameplans route')
    gameplan_info = request.json
    gameplan_id = gameplan_info['id']
    query = """
        UPDATE gameplans 
        SET matchId = %s, coachId = %s,
            planDate = %s, content = %s
        WHERE id = %s
    """
    data = (
        gameplan_info.get('matchId'),
        gameplan_info.get('coachId'),
        gameplan_info.get('planDate'),
        gameplan_info.get('content'),
        gameplan_id
    )
    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()
    response = make_response(jsonify({"message": "Gameplan updated successfully"}), 200)
    return response
#------------------------------------------------------------

# Get detail for a single gameplan identified by gameplan_id: 
# TESTED - PASSING POSTMAN REQUEST 
@gameplans.route('/gameplans/<int:gameplan_id>', methods=['GET']) 
def get_gameplan(gameplan_id): 
    current_app.logger.info(f'GET /gameplans/{gameplan_id} route') 
    cursor = db.get_db().cursor() 
    cursor.execute(''' 
        SELECT id, matchId, coachId, planDate, content 
        FROM gameplans WHERE id = %s 
    ''', (gameplan_id,)) 
    theData = cursor.fetchall() 
    the_response = make_response(jsonify(theData)) 
    the_response.status_code = 200 
    return the_response
#------------------------------------------------------------
# Do dynamic partial update of user info for a user given the id:

@gameplans.route('/gameplans/<int:gameplan_id>', methods=['PATCH'])
def patch_gameplan(gameplan_id):
    gameplan_data = request.json
    fields = []
    values = []
    allowed_fields = ['matchId', 'coachId', 'planDate', 'content']
    for field in allowed_fields:
        if field in gameplan_data:
            fields.append(f"{field} = %s")
            values.append(gameplan_data[field])
    if not fields:
        return make_response(jsonify({"error": "No valid fields provided"}), 400)
    values.append(gameplan_id)
    query = "UPDATE gameplans SET " + ", ".join(fields) + " WHERE id = %s"
    cursor = db.get_db().cursor()
    cursor.execute(query, tuple(values))
    db.get_db().commit()
    response = make_response(jsonify({"message": "Gameplan partially updated"}))
    response.status_code = 200
    return response
#------------------------------------------------------------
# Delete user from the system given the id: 

@gameplans.route('/gameplans/<int:gameplan_id>', methods=['DELETE'])
def delete_gameplan(gameplan_id):
    cursor = db.get_db().cursor()
    cursor.execute('''
        DELETE FROM gameplans 
        WHERE id = %s
    ''', (gameplan_id,))
    db.get_db().commit()
    response = make_response(jsonify({"message": "Gameplan deleted successfully"}), 200)
    return response
#------------------------------------------------------------