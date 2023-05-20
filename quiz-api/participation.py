import sqlite3
from jwt_utils import *

class Participation:	

	def ScoresCalculation():
		db_connection = sqlite3.connect('./db.db')
		db_connection.isolation_level = None

		cur = db_connection.cursor()

		cur.execute("""
			SELECT User.name, IFNULL(Score.total, 0) as score
			FROM User
			LEFT JOIN (
				SELECT Participation.user_id, COUNT(AnsweredQuestions.response_id) as total
				FROM Participation
				INNER JOIN AnsweredQuestions ON Participation.id = AnsweredQuestions.participation_id
				INNER JOIN Reponse ON AnsweredQuestions.response_id = Reponse.id
				WHERE Reponse.isCorrect = 1
				GROUP BY Participation.user_id
			) Score ON User.id = Score.user_id
			ORDER BY score DESC
		""")

		scores = [{"playerName": row[0], "score": row[1]} for row in cur.fetchall()]

		return scores
	

	def GetOrCreatePlayer(playerName):
		db_connection = sqlite3.connect('./db.db')
		db_connection.isolation_level = None

		cur = db_connection.cursor()

		# Check if user exists, if not create one
		cur.execute("SELECT id FROM User WHERE name=?", (playerName,))
		user_id = cur.fetchone()

		if user_id is None:
			cur.execute("INSERT INTO User (name) VALUES (?)", (playerName,))
			user_id = cur.lastrowid
		else:
			user_id = user_id[0]

		return user_id
	

	def SaveParticipation(playerName, answers):

		db_connection = sqlite3.connect('./db.db')
		db_connection.isolation_level = None

		cur = db_connection.cursor()

		cur.execute("SELECT COUNT(*) FROM Question")
		question_count = cur.fetchone()[0]

		if len(answers) != question_count:
			return "Wrong number of answers. Expected: "+str(question_count)+", received: "+str(len(answers))

		user_id = Participation.GetOrCreatePlayer(playerName)

		cur.execute("INSERT INTO Participation (user_id, date) VALUES (?, ?)", (user_id, datetime.datetime.now()))
		participation_id = cur.lastrowid

		cur.execute("SELECT id FROM Question ORDER BY position")
		questions = [row[0] for row in cur.fetchall()]

		score = 0
		for question_id, answer_index in zip(questions, answers):
			cur.execute("SELECT id, isCorrect FROM Reponse WHERE question_id=? ORDER BY id", (question_id,))
			responses = cur.fetchall()
			response_id = responses[answer_index - 1][0]
			isCorrect = responses[answer_index - 1][1]

			if isCorrect:
				score += 1

			cur.execute("INSERT INTO AnsweredQuestions (participation_id, question_id, response_id) VALUES (?, ?, ?)",
						(participation_id, question_id, response_id))
			
		return score


	def DeleteAllParticipations():
		db_connection = sqlite3.connect('./db.db')
		db_connection.isolation_level = None

		cur = db_connection.cursor()

		cur.execute("begin")

		cur.execute("DELETE FROM AnsweredQuestions")
		cur.execute("DELETE FROM Participation")
		cur.execute("DELETE FROM User")

		cur.execute("commit")

		cur.execute("SELECT * FROM Participation")
		Participation_row = cur.fetchall()

		if not Participation_row:
			return "All participations deleted successfully"
		else:
			return "Error deleting participations"

