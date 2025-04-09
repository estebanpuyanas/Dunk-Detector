from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

users = Blueprint('users', __name__)

#------------------------------------------------------------
# Get all users from the system: 
# TESTED - PASSING POSTMAN REQUEST

@users.route('/users', methods=['GET'])
def get_all_users():
    cursor = db.get_db().cursor()
    cursor.execute('''
        SELECT id, firstName, middleName, lastName,
                mobile, email, role 
        FROM users 
    ''') 
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    return the_response
#------------------------------------------------------------
#Put a new user into the system:
# TESTED - PASSING POSTMAN REQUEST

@users.route('/users', methods=['POST'])
def create_user():
    user_data = request.json
    query = """
        INSERT INTO users (firstName, middleName, lastName, mobile, email, role)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    data = (
        user_data.get('firstName'),
        user_data.get('middleName'),
        user_data.get('lastName'),
        user_data.get('mobile'),
        user_data.get('email'),
        user_data.get('role')
    )
    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()
    new_id = cursor.lastrowid
    response = make_response(jsonify({"id": new_id}), 201)
    return response
#------------------------------------------------------------
# Update user info for a user given the id:
# TESTED - PASSING POSTMAN REQUEST

@users.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    current_app.logger.info('PUT /users/<user_id> route')
    user_info = request.json
    query = """
        UPDATE users 
        SET firstName = %s, middleName = %s, lastName = %s,
            mobile = %s, email = %s, role = %s
        WHERE id = %s
    """
    data = (
        user_info.get('firstName'),
        user_info.get('middleName'),
        user_info.get('lastName'),
        user_info.get('mobile'),
        user_info.get('email'),
        user_info.get('role'),
        user_id
    )
    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()
    response = make_response(jsonify({"message": "User updated successfully"}), 200)
    return response
#------------------------------------------------------------
# Do dynamic partial update of user info for a user given the id:
# TESTED - PASSING POSTMAN REQUEST 

@users.route('/users/<int:user_id>', methods=['PATCH'])
def patch_user(user_id):
    user_data = request.json
    fields = []
    values = []
    allowed_fields = ['firstName', 'middleName', 'lastName', 'mobile', 'email', 'role']
    for field in allowed_fields:
        if field in user_data:
            fields.append(f"{field} = %s")
            values.append(user_data[field])
    if not fields:
        return make_response(jsonify({"error": "No valid fields provided"}), 400)
    values.append(user_id)
    query = "UPDATE users SET " + ", ".join(fields) + " WHERE id = %s"
    cursor = db.get_db().cursor()
    cursor.execute(query, tuple(values))
    db.get_db().commit()
    response = make_response(jsonify({"message": "The following fields were updated for user id " + str(user_id) + ": " + ", ".join(fields)})) #fix the formatting on reponse. 
    response.status_code = 200
    return response
#------------------------------------------------------------
# Delete user from the system given the id: 
# TESTED - PASSING POSTMAN REQUEST

@users.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    cursor = db.get_db().cursor()
    cursor.execute('''
        DELETE FROM users 
        WHERE id = %s
    ''', (user_id,))
    db.get_db().commit()
    response = make_response(jsonify({"message": "User deleted successfully"}), 200)
    return response
#------------------------------------------------------------