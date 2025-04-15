#!/usr/bin/env python3
import os
import random
import pymysql
from datetime import timedelta
from dotenv import load_dotenv

# 1. Load your .env so we can pick up DB credentials
load_dotenv(dotenv_path="./api/.env")

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("MYSQL_ROOT_PASSWORD", "jeffrex123")
DB_NAME = os.getenv("DB_NAME", "dunkDetector")

def random_time(min_seconds=1800, max_seconds=2400):
    """Return a MySQL TIME string between min_seconds and max_seconds."""
    secs = random.randint(min_seconds, max_seconds)
    td = timedelta(seconds=secs)
    return str(td)

def main():
    # 2. Connect to MySQL
    conn = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = conn.cursor()

    # 3. Define which new match IDs to seed
    new_matches = [21, 22, 23, 24, 25]
    num_players = 30

    for match_id in new_matches:
        for player_id in range(1, num_players + 1):
            stats = {
                "playerId":     player_id,
                "matchId":      match_id,
                "totalPoints":  random.randint(0, 35),
                "fieldGoals":   random.randint(0, 15),
                "threePointers":random.randint(0, 10),
                "steals":       random.randint(0, 5),
                "blocks":       random.randint(0, 3),
                "rebounds":     random.randint(0, 12),
                "assists":      random.randint(0, 10),
                "turnovers":    random.randint(0, 5),
                "freeThrows":   random.randint(0, 10),
                "totalPlayTime": random_time(),
                "fouls":        random.randint(0, 6),
            }
            cursor.execute("""
                INSERT INTO statistics 
                  (playerId, matchId, totalPoints, fieldGoals, threePointers,
                   steals, blocks, rebounds, assists, turnovers, freeThrows,
                   totalPlayTime, fouls)
                VALUES
                  (%(playerId)s, %(matchId)s, %(totalPoints)s, %(fieldGoals)s, %(threePointers)s,
                   %(steals)s, %(blocks)s, %(rebounds)s, %(assists)s, %(turnovers)s, %(freeThrows)s,
                   %(totalPlayTime)s, %(fouls)s)
            """, stats)

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Seeded statistics for players 1–{num_players} in matches {new_matches}")

if __name__ == "__main__":
    main()
