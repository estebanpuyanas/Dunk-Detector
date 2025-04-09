from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

reports = Blueprint('reports', __name__)

@reports.route('/reports', methods=['GET'])
def get_reports():
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT * FROM reports''')
    reports_data = cursor.fetchall()

    column_headers = [x[0] for x in cursor.description]

    theData = []
    for row in reports_data:
        row_data = {}
        for i in range(len(column_headers)):
            row_data[column_headers[i]] = row[i]
        theData.append(row_data)

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

@reports.route('/reports', methods=['POST'])
def create_report():
    data = request.get_json()

    # Validate required fields
    if not data.get('authorId') or not data.get('reportDate') or not data.get('content') or not data.get('reportType'):
        return jsonify({"error": "Missing required fields"}), 400

    # Insert the new report into the database
    cursor = db.get_db().cursor()
    cursor.execute('''INSERT INTO reports (authorId, reportDate, content, reportType, playerId, matchId, playerRating)
                      VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                   (data['authorId'], data['reportDate'], data['content'], data['reportType'],
                    data.get('playerId'), data.get('matchId'), data.get('playerRating')))

    db.get_db().commit()
    return jsonify({"message": "Report created successfully"}), 201


@reports.route('/reports', methods=['PUT'])
def update_report():
    data = request.get_json()

    # Validate required fields
    if not data.get('id') or not data.get('authorId') or not data.get('reportDate') or not data.get('content') or not data.get('reportType'):
        return jsonify({"error": "Missing required fields"}), 400

    # Update the report
    cursor = db.get_db().cursor()
    cursor.execute('''UPDATE reports SET authorId = %s, reportDate = %s, content = %s, reportType = %s,
                      playerId = %s, matchId = %s, playerRating = %s WHERE id = %s''',
                   (data['authorId'], data['reportDate'], data['content'], data['reportType'],
                    data.get('playerId'), data.get('matchId'), data.get('playerRating'), data['id']))

    db.get_db().commit()
    return jsonify({"message": "Report updated successfully"}), 200

@reports.route('/reports/<int:id>', methods=['GET'])
def get_report_by_id(id):
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT * FROM reports WHERE id = %s''', (id,))
    report = cursor.fetchone()

    if not report:
        return jsonify({"error": "Report not found"}), 404

    column_headers = [description[0] for description in cursor.description]
    report_data = {column_headers[i]: report[i] for i in range(len(column_headers))}

    return jsonify(report_data), 200

@reports.route('/reports/<int:id>', methods=['PATCH'])
def patch_report_by_id(id):
    data = request.get_json()

    # Check for update fields
    update_values = []
    set_clause = []

    if 'authorId' in data:
        set_clause.append("authorId = %s")
        update_values.append(data['authorId'])
    if 'reportDate' in data:
        set_clause.append("reportDate = %s")
        update_values.append(data['reportDate'])
    if 'content' in data:
        set_clause.append("content = %s")
        update_values.append(data['content'])
    if 'reportType' in data:
        set_clause.append("reportType = %s")
        update_values.append(data['reportType'])
    if 'playerId' in data:
        set_clause.append("playerId = %s")
        update_values.append(data['playerId'])
    if 'matchId' in data:
        set_clause.append("matchId = %s")
        update_values.append(data['matchId'])
    if 'playerRating' in data:
        set_clause.append("playerRating = %s")
        update_values.append(data['playerRating'])

    set_clause.append("WHERE id = %s")
    update_values.append(id)

    cursor = db.get_db().cursor()
    cursor.execute(f'''UPDATE reports SET {', '.join(set_clause)}''', tuple(update_values))

    db.get_db().commit()
    return jsonify({"message": "Report updated successfully"}), 200

@reports.route('/reports/<int:id>', methods=['DELETE'])
def delete_report_by_id(id):
    cursor = db.get_db().cursor()
    cursor.execute('''DELETE FROM reports WHERE id = %s''', (id,))

    db.get_db().commit()
    return jsonify({"message": "Report deleted successfully"}), 200