from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

gm = Blueprint('gm', __name__)

#------------------------------------------------------------
# Get all gms from the system: 

@gm.route('/gm', methods=['GET'])
def get_all_gm():
    cursor = db.get_db().cursor()
    cursor.execute('''
        SELECT id, firstName, middleName, lastName, teamId 
        FROM gm 
    ''') 
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Get detail for a gm identified by gm_id:

@gm.route('/gm/<int:gm_id>', methods=['GET'])
def get_gm_id(gm_id):
    current_app.logger.info(f'GET /gm/{gm_id} route')
    cursor = db.get_db().cursor()
    cursor.execute('''
        SELECT id, firstName, middleName, lastName, mobile,
                email, teamId
        FROM general_managers WHERE id = %s
    ''', (gm_id,))
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


#------------------------------------------------------------
# Get detail for a gm identified by team_id:

@gm.route('/gm/<int:gm_id>', methods=['GET'])
def get_gm_team(name):
    current_app.logger.info(f'GET /gm/team/{name} route')
    cursor = db.get_db().cursor()
    cursor.execute('''
        SELECT id, firstName, middleName, lastName, mobile, email, teamId
        FROM general_managers g
        JOIN (SELECT name, generalManagerID
        FROM teams) t on g.id = t.generalManagerID
        WHERE name = %s
    ''', (name,))
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
#Put a new gm into the system:

@gm.route('/gm', methods=['POST'])
def create_gm():
    gm_data = request.json
    query = """
        INSERT INTO gm (firstName, middleName, lastName, mobile, email, teamId)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    data = (
        gm_data.get('firstName'),
        gm_data.get('middleName'),
        gm_data.get('lastName'),
        gm_data.get('mobile'),
        gm_data.get('email'),
        gm_data.get('teamId')
    )
    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()
    new_id = cursor.lastrowid
    response = make_response(jsonify({"id": new_id}), 201)
    return response
#------------------------------------------------------------
# Do dynamic partial update of gm info for a gm given the id:

@gm.route('/gm/<int:gm_id>', methods=['PATCH'])
def patch_gm(gm_id):
    gm_data = request.json
    fields = []
    values = []
    allowed_fields = ['team', 'email', 'mobile']
    for field in allowed_fields:
        if field in gm_data:
            fields.append(f"{field} = %s")
            values.append(gm_data[field])
    if not fields:
        return make_response(jsonify({"error": "No valid fields provided"}), 400)
    values.append(gm_id)
    query = "UPDATE gm SET " + ", ".join(fields) + " WHERE id = %s"
    cursor = db.get_db().cursor()
    cursor.execute(query, tuple(values))
    db.get_db().commit()
    response = make_response(jsonify({"message": "The following fields were updated for GM id" + str(gm_id) + ": " + ", ".join(fields)}))
    response.status_code = 200
    return response
