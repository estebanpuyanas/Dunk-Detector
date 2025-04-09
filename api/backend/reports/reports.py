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

