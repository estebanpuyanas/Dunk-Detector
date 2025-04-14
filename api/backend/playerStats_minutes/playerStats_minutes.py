from flask import Blueprint, request, jsonify, make_response, current_app
import pymysql.cursors
import datetime

from backend.db_connection import db

playerStatsByMinutes = Blueprint('playersStats_minutes', __name__)

@playerStatsByMinutes.route('/playerStats_minutes', methods=['GET'])
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
                S.*
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
