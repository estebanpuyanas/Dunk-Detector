from flask import Blueprint, request, jsonify, current_app
from backend.db_connection import db
import pymysql.cursors

reports = Blueprint('reports', __name__)

@reports.route('/reports', methods=['GET'])
def get_reports():
    try:
        # Use a DictCursor so fetchall() returns a list of dicts
        cursor = db.get_db().cursor(pymysql.cursors.DictCursor)
        cursor.execute('SELECT * FROM reports')
        data = cursor.fetchall()
        return jsonify(data), 200

    except Exception as e:
        current_app.logger.exception("Error fetching reports")
        return jsonify({"error": str(e)}), 500


@reports.route('/reports', methods=['POST'])
def create_report():
    data = request.get_json()
    if not data.get('authorId') or not data.get('reportDate') or not data.get('content') or not data.get('reportType'):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        cursor = db.get_db().cursor()
        cursor.execute(
            '''INSERT INTO reports 
               (authorId, reportDate, content, reportType, playerId, matchId, playerRating)
               VALUES (%s, %s, %s, %s, %s, %s, %s)''',
            (
                data['authorId'], data['reportDate'], data['content'], data['reportType'],
                data.get('playerId'), data.get('matchId'), data.get('playerRating')
            )
        )
        db.get_db().commit()
        return jsonify({"message": "Report created successfully"}), 201

    except Exception as e:
        current_app.logger.exception("Error creating report")
        return jsonify({"error": str(e)}), 500


@reports.route('/reports/<int:id>', methods=['PATCH'])
def patch_report_by_id(id):
    data = request.get_json()
    set_clauses = []
    values = []

    # Build SET clause dynamically
    for field in ('authorId', 'reportDate', 'content', 'reportType', 'playerId', 'matchId', 'playerRating'):
        if field in data:
            set_clauses.append(f"{field} = %s")
            values.append(data[field])

    if not set_clauses:
        return jsonify({"error": "No fields to update"}), 400

    values.append(id)
    sql = f"UPDATE reports SET {', '.join(set_clauses)} WHERE id = %s"

    try:
        cursor = db.get_db().cursor()
        cursor.execute(sql, tuple(values))
        db.get_db().commit()
        return jsonify({"message": "Report updated successfully"}), 200

    except Exception as e:
        current_app.logger.exception("Error updating report")
        return jsonify({"error": str(e)}), 500


@reports.route('/reports/<int:id>', methods=['DELETE'])
def delete_report_by_id(id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute('DELETE FROM reports WHERE id = %s', (id,))
        db.get_db().commit()
        return jsonify({"message": "Report deleted successfully"}), 200

    except Exception as e:
        current_app.logger.exception("Error deleting report")
        return jsonify({"error": str(e)}), 500
