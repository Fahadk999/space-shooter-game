import  sqlite3

# learing databases from this
class ScoreDatabase:
    def __init__(self, dbName="highscore.db") -> None:
        self.dbName = dbName
        self.createTable()

    def getConnection (self):
        # creates connectoin to sqlite db file
        return sqlite3.connect(self.dbName)

    def createTable (self):
        # creates table 
        with self.getConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS leaderboard (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    playerName TEXT NOT NULL,
                    score INTEGER NOT NULL,
                    dateAchived DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def addScore (self, playerName, score):
        with self.getConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO leaderboard (playerName, score)
                VALUES (?, ?)
            """, (playerName, score))
            conn.commit()

    def getTopScores (self, limit=5):
        with self.getConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SElECT playerName, score
                FROM leaderboard
                ORDER BY score DESC
                LIMIT ?
            """, (limit,))
            return cursor.fetchall()