import sqlite3
import json

class Question:
	def __init__(self, position, title, text, image, possible_answers):
		self.position = position
		self.title = title
		self.text = text
		self.image = image
		self.possible_answers = possible_answers



	def to_json(self):
		return {
			"position": self.position,
			"title": self.title,
			"text": self.text,
			"image": self.image,
			"possibleAnswers": [
				{
					"text": answer["text"],
					"isCorrect": bool(answer["isCorrect"])
				}
				for answer in self.possible_answers
			]
		}


	@classmethod
	def from_json(cls, json_data):
		question = cls(
			position=json_data["position"],
			title=json_data["title"],
			text=json_data["text"],
			image=json_data["image"],
			possible_answers=json_data["possibleAnswers"]
		)
		return question
	

	# --- Getting Question ---

	def GetQuestionsCount():
		db_connection = sqlite3.connect('./db.db')
		db_connection.row_factory = sqlite3.Row

		cur = db_connection.cursor()

		cur.execute("SELECT COUNT(*) FROM Question")
		question_count = cur.fetchone()[0]

		return question_count
	

	def GetQuestionByID(question_id: int):
		db_connection = sqlite3.connect('./db.db')
		db_connection.row_factory = sqlite3.Row

		cur = db_connection.cursor()

		cur.execute(f"SELECT * FROM Question WHERE id=?", (question_id,))
		question_row = cur.fetchone()

		cur.execute(f"SELECT * FROM Reponse WHERE question_id=?", (question_id,))
		answer_rows = cur.fetchall()

		if not question_row or not answer_rows:
			return None

		question = Question(
			position=question_row["position"],
			title=question_row["title"],
			text=question_row["text"],
			image=question_row["image"],
			possible_answers=[
				{
					"text": answer_row["text"],
					"isCorrect": bool(answer_row["isCorrect"])
				}
				for answer_row in answer_rows
			]
		)

		return json.dumps(question.to_json())

	
	def GetQuestionByPosition(position: int):
		db_connection = sqlite3.connect('./db.db')
		db_connection.row_factory = sqlite3.Row

		cur = db_connection.cursor()

		cur.execute(f"SELECT * FROM Question WHERE position=?", (position,))
		question_row = cur.fetchone()

		if not question_row:
			return None

		question_id = question_row["id"]

		cur.execute(f"SELECT * FROM Reponse WHERE question_id=?", (question_id,))
		answer_rows = cur.fetchall()

		question = Question(
			position=question_row["position"],
			title=question_row["title"],
			text=question_row["text"],
			image=question_row["image"],
			possible_answers=[
				{
					"text": answer_row["text"],
					"isCorrect": bool(answer_row["isCorrect"])
				}
				for answer_row in answer_rows
			]
		)

		return json.dumps(question.to_json())



	# --- Adding Question ---

	def Add(question):
		db_connection = sqlite3.connect('./db.db')
		cur = db_connection.cursor()
		
		cur.execute("begin")

		q = Question.from_json(question)

		cur.execute("SELECT MAX(position) FROM Question")
		max_position = cur.fetchone()[0] or 0

		if q.position <= max_position:
			for position in range(max_position, q.position - 1, -1):
				cur.execute("UPDATE Question SET position = position + 1 WHERE position = ?", (position,))

		cur.execute("INSERT INTO Question (position, title, text, image) VALUES (?, ?, ?, ?)",
					(q.position, q.title, q.text, q.image))

		new_question_id = cur.lastrowid
		
		for answer in q.possible_answers:
			sql = f"insert into Reponse (question_id, text, isCorrect) values (?, ?, ?)"
			values = (new_question_id, answer["text"], int(answer["isCorrect"]))
			cur.execute(sql, values)

		cur.execute("commit")

		return new_question_id






	# --- Updating Question ---
	def UpdateQuestion(id, question):
		db_connection = sqlite3.connect('./db.db')
		cur = db_connection.cursor()

		cur.execute("begin")

		q = Question.from_json(question)

		cur.execute("SELECT id FROM Question WHERE position = ?", (q.position,))
		existing_question_row = cur.fetchone()

		cur.execute("SELECT position FROM Question WHERE id = ?", (id,))
		ancient_question_position = cur.fetchone()

		if existing_question_row and ancient_question_position:
			cur.execute("UPDATE Question SET position = -1 WHERE id = ?", (existing_question_row[0],))

		cur.execute("UPDATE Question SET position = ?, title = ?, text = ?, image = ? WHERE id = ?",
					(q.position, q.title, q.text, q.image, id))

		if existing_question_row and ancient_question_position:
			cur.execute("UPDATE Question SET position = ? WHERE id = ?",
						(ancient_question_position[0], existing_question_row[0],))

		cur.execute("DELETE FROM Reponse WHERE question_id = ?", (id,))

		for answer in q.possible_answers:
			sql = f"insert into Reponse (question_id, text, isCorrect) values (?, ?, ?)"
			values = (id, answer["text"], int(answer["isCorrect"]))
			cur.execute(sql, values)
			
		cur.execute("commit")

		cur.execute("SELECT * FROM Question WHERE id = ?", (id,))
		question_row = cur.fetchone()

		if question_row:
			return "Question updated successfully"
		else:
			return "Error updating question"




	# --- Deleting question ---

	def DeleteQuestionById(id: int):
		db_connection = sqlite3.connect('./db.db')
		db_connection.isolation_level = None

		cur = db_connection.cursor()

		cur.execute("begin")

		cur.execute("SELECT * FROM Question WHERE id=?", (id,))
		question_row = cur.fetchone()

		if not question_row:
			return "Error deleting question"			

		cur.execute("DELETE FROM Reponse WHERE question_id=?", (id,))
		cur.execute("DELETE FROM Question WHERE id=?", (id,))

		cur.execute("commit")

		cur.execute("SELECT * FROM Question WHERE id=?", (id,))
		question_row = cur.fetchone()

		if not question_row:
			return "Question deleted successfully"
		else:
			return "Error deleting question"
		

	def UpdateQuestionPositionsAfterDelete(id: int):
		db_connection = sqlite3.connect('./db.db')
		db_connection.isolation_level = None

		cur = db_connection.cursor()

		cur.execute("SELECT position FROM Question WHERE id=?", (id,))
		question_position = cur.fetchone()
		if not question_position:
			return "Question does not exist"

		cur.execute("begin")

		cur.execute("UPDATE Question SET position = position - 1 WHERE position > ?", (question_position[0],))

		cur.execute("commit")
		return "Position updated successfully"


	def DeleteQuestionByIDAndUpdatePositions(id: int):
			message = Question.DeleteQuestionById(id)

			if message == "Question deleted successfully":
				Question.UpdateQuestionPositionsAfterDelete(id)
			else:
				return "Error deleting question"
			
			return "Question deleted and positions updated successfully"

	
	def DeleteAllQuestions():
		db_connection = sqlite3.connect('./db.db')
		db_connection.isolation_level = None

		cur = db_connection.cursor()

		cur.execute("begin")

		cur.execute("DELETE FROM Reponse")
		cur.execute("DELETE FROM Question")

		cur.execute("commit")

		cur.execute("SELECT * FROM Question")
		question_row = cur.fetchall()

		if not question_row:
			return "All questions deleted successfully"
		else:
			return "Error deleting questions"

