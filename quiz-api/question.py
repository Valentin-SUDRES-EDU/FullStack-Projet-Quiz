import sqlite3
import json
import base64

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
	

	def ReInitialize():
		db_connection = sqlite3.connect('./db.db')

		cur = db_connection.cursor()

		cur.execute("begin")

		cur.execute("""DROP TABLE IF EXISTS AnsweredQuestions""")
		cur.execute("""DROP TABLE IF EXISTS Participation""")
		cur.execute("""DROP TABLE IF EXISTS User""")
		cur.execute("""DROP TABLE IF EXISTS Reponse""")
		cur.execute("""DROP TABLE IF EXISTS Question""")

		cur.execute("""CREATE TABLE "Question" (
			"id"	INTEGER NOT NULL DEFAULT 1 UNIQUE,
			"position"	INTEGER NOT NULL DEFAULT 1 UNIQUE,
			"title"	TEXT NOT NULL,
			"text"	TEXT NOT NULL,
			"image"	TEXT NOT NULL,
			PRIMARY KEY("id" AUTOINCREMENT)
		)""")

		cur.execute("""CREATE TABLE "Reponse" (
			"id"	INTEGER NOT NULL UNIQUE,
			"question_id"	INTEGER NOT NULL,
			"text"	TEXT NOT NULL,
			"isCorrect"	INTEGER NOT NULL,
			FOREIGN KEY("question_id") REFERENCES "Question"("id"),
			PRIMARY KEY("id" AUTOINCREMENT)
		)""")

		cur.execute("""CREATE TABLE "User" (
			"id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
			"name" TEXT NOT NULL
		)""")

		cur.execute("""CREATE TABLE "Participation" (
			"id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
			"user_id" INTEGER,
			"date" TEXT NOT NULL,
			FOREIGN KEY("user_id") REFERENCES "User"("id")
		)""")

		cur.execute("""CREATE TABLE "AnsweredQuestions" (
			"id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
			"participation_id" INTEGER,
			"question_id" INTEGER,
			"response_id" INTEGER,
			FOREIGN KEY("participation_id") REFERENCES "Participation"("id"),
			FOREIGN KEY("question_id") REFERENCES "Question"("id"),
			FOREIGN KEY("response_id") REFERENCES "Reponse"("id")
		)""")

		cur.execute("commit")

	def image_to_data_url(filename):
		ext = filename.split('.')[-1]
		prefix = f'data:image/{ext};base64,'
		with open(filename, 'rb') as f:
			img = f.read()
		return prefix + base64.b64encode(img).decode('utf-8')

	def PopulateQuiz():
		db_connection = sqlite3.connect('./db.db')
		db_connection.row_factory = sqlite3.Row

		cur = db_connection.cursor()

		cur.execute("begin")

		cur.execute("""INSERT INTO "Question" ("position", "title", "text", "image") VALUES 
		(1, "Voie Lactée", "Combien d'étoiles la Voie Lactée abrite-t-elle ?", ? ),

		(2, "Soleil", "Combien de temps prend le Soleil pour orbiter autour de la Voie Lactée ?", ? ),
		(3, "Soleil", "À quelle classe d'étoile appartient le Soleil?", ? ),
		(4, "Soleil", "Quel élément chimique est le composant majeur du Soleil?", ? ),

		(5, "Trous noirs", "Quel est le phénomène physique impliqué dans la lente perte de masse des trous noirs ?", ? ),
		(6, "Trous noirs", "En 2019, une équipe internationale photographiait pour la première fois un trou noir. Comment s'appelle ce trou noir ?", ? ),

		(7, "Définition", "Qu'est ce qu'un Magnétar ?", ? ),
		(8, "Définition", "Qu'est ce que la limite de Roche ?", ? ),
		(9, "Définition", "Quel est le nom d'une mégastructure hypothétique qui permettrait de capturer l'énergie d'une étoile ?", ? ),
		(10, "Définition", "Qu'est ce qu'un sursaut gamma ?", ? ),
		(11, "Définition", "L'Année-Lumière sert à mesurer :", ? ),
		(12, "Définition", "Quel évènement produit une supernova?", ? ),
		(13, "Définition", "Qu'est ce que le verrouillage gravitationnel ?", ? ),

		(14, "Distance", "Quelle est la distance Terre-Lune, 50000km près ?", ? ),
		(15, "Distance", "Combien de temps met la lumière du soleil à nous parvenir ?", ?),

		(16, "Satellite", "Qui a découvert Titan, un satellite de Saturne ?", ? ),
		(17, "Satellite", "Quels sont les noms des satellites galiléens de Jupiter  ?", ? ),
		(18, "Satellite", "Quel satellite de Saturne sépare son anneau A et son anneau B ?", ? ),
		(19, "Satellite", "Quel est le nom du plus gros satellite de Pluton ?", ? ),

		(20, "Grandeur", "Quelle est la taille de Jupiter par rapport à la Terre ?", ? ),

		(21, "Exploration spatiale", "Quelle sonde est actuellement la plus éloignée de la Terre ?", ? ),
		(22, "Exploration spatiale", "Quel est le dernier homme à avoir marché sur la Lune (en 2023) ?", ? ),

		(23, "Comète", "Quelle comète est représentée sur la tapisserie de Bayeux ?", ? ),

		(24, "Etoiles", "Qu'est-ce que UY Scuti ?", ? ),
		(25, "Etoiles", "Quelle est l'étoile la plus proche de notre système solaire ?", ? )

		""", (
			Question.image_to_data_url("src/img/q1.jpg"),
   			Question.image_to_data_url("src/img/q2.jpg"),
			Question.image_to_data_url("src/img/q3.jpg"),
			Question.image_to_data_url("src/img/q4.jpg"),
			Question.image_to_data_url("src/img/q5.jpg"),
			Question.image_to_data_url("src/img/q6.jpg"),
			Question.image_to_data_url("src/img/q7.jpg"),
			Question.image_to_data_url("src/img/q8.jpg"),
			Question.image_to_data_url("src/img/q9.jpg"),
			Question.image_to_data_url("src/img/q10.jpg"),
			Question.image_to_data_url("src/img/q11.jpg"),
			Question.image_to_data_url("src/img/q12.jpg"),
			Question.image_to_data_url("src/img/q13.jpg"),
			Question.image_to_data_url("src/img/q14.jpg"),
			Question.image_to_data_url("src/img/q15.jpg"),
			Question.image_to_data_url("src/img/q16.jpg"),
			Question.image_to_data_url("src/img/q17.jpg"),
			Question.image_to_data_url("src/img/q18.jpg"),
			Question.image_to_data_url("src/img/q19.jpg"),
			Question.image_to_data_url("src/img/q20.jpg"),
			Question.image_to_data_url("src/img/q21.jpg"),
			Question.image_to_data_url("src/img/q22.jpg"),
			Question.image_to_data_url("src/img/q23.jpg"),
			Question.image_to_data_url("src/img/q24.jpg"),
			Question.image_to_data_url("src/img/q25.jpg"),
		))


		cur.execute("""INSERT INTO "Reponse" ("question_id", "text", "isCorrect") VALUES 

		(1, "Entre 100.000 et 200.000", 0),
		(1, "Entre 100 et 400 millions", 0),
		(1, "Entre 1 et 2 milliards", 0),
		(1, "Entre 200 et 400 milliards", 1),

		(2, "365 jours", 0),
		(2, "1 000 ans", 0),
		(2, "250 millions d'années", 1),
		(2, "2 milliards d'années", 0),

		(3, "Naine jaune", 1),
		(3, "Géante rouge", 0),
		(3, "Naine blanche", 0),
		(3, "Géante bleue", 0),

		(4, "Oxygène", 0),
		(4, "Carbone", 0),
		(4, "Hydrogène", 1),
		(4, "Hélium", 0),

		(5, "La relativité d'Einstein", 0),
		(5, "Le rayonnement de Hawking", 1),
		(5, "L'écoulement de Bernoulli", 0),
		(5, "La thermodynamique de Thomson", 0),

		(6, "M87*", 1),
		(6, "Sagittarius A*", 0),
		(6, "TON 618", 0),
		(6, "Cygnus X-3", 0),

		(7, "Une structure théorique permettant, grâce à d'immenses aimants, de déplacer une étoile", 0),
		(7, "Les restes d'une étoile massive, pivotant sur elle même à grande vitesse", 1),
		(7, "Un des appareils expérimentaux créés dans le but d'étudier le champ magnétique terrestre", 0),
		(7, "Une exoplanète majoritairement formée de matériaux ferreux", 0),

		(8, "La distance minimale à laquelle un satellite naturel serait détruit par le corps céleste autour duquel il orbite", 1),
		(8, "La masse critique au dessus de laquelle un corps céleste devient une planète tellurique", 0),
		(8, "La distance maximale d'une planète tellurique à son étoile la plus proche", 0),
		(8, "La taille limite d'un astéroïde afin qu'il ne cause pas d'évènement d'extinction de l'espèce", 0),

		(9, "L'Etoile de la Mort", 0),
		(9, "Cylindre O'Neill", 0),
		(9, "Sphère de Dyson", 1),
		(9, "Sphère de Bernal", 0),

		(10, "Une manière de détecter une planète orbitant autour d'une étoile", 0),
		(10, "Un mécanisme permettant de photographier l'univers profond", 0),
		(10, "Une explosion stellaire parmi les évènements les plus violents de notre univers", 1),
		(10, "Une technologie développée pour l'observation spatiale, désormais utilisée en médecine classique", 0),

		(11, "La vitesse", 0),
		(11, "Le mouvement", 0),
		(11, "Le temps", 0),
		(11, "La distance", 1),

		(12, "La collision entre deux galaxies", 0),
		(12, "L'implosion d'une étoile en fin de vie", 1),
		(12, "La désintégration d'un corps céleste dans une étoile", 0),
		(12, "La collision entre deux étoiles", 0),

		(13, "Un phénomène à cause duquel un satellite présente toujours la même face au corps qu'il orbite ", 1),
		(13, "Une technique pour calculer une trajectoire vers un corps céleste ", 0),
		(13, "Un phénomène qui permet aux satellites de ne pas s'écraser sur la Terre ", 0),
		(13, "Ce qui arrive aux planètes qui orbitent autour d'un trou noir", 0),

		(14, "300.000 km", 0),
		(14, "400.000 km", 1),
		(14, "500.000 km", 0),
		(14, "600.000 km", 0),

		(15, "8 secondes", 0),
		(15, "8 minutes", 1),
		(15, "8 heures", 0),
		(15, "8 jours", 0),

		(16, "Christiaan Huygens", 1),
		(16, "Johannes Kepler", 0),
		(16, "Jean-Dominique Cassini", 0),
		(16, "Isaac Newton", 0),

		(17, "Io, Europe, Ganymède et Callisto", 1),
		(17, "Titan, Encelade, Japet, Thétys", 0),
		(17, "Triton, Thalassa, Hippocampe, Galatée", 0),
		(17, "Titania, Miranda, Obéron, Umbriel", 0),

		(18, "Encelade", 0),
		(18, "Europe", 0),
		(18, "Mimas", 1),
		(18, "Titan", 0),

		(19, "La Lune", 0),
		(19, "Phobos", 0),
		(19, "Styx", 0),
		(19, "Charon", 1),

		(20, "20 fois plus grande que la Terre", 0),
		(20, "42 fois plus grande que la Terre ", 0),
		(20, "11 fois plus grande que la Terre", 1),
		(20, "600 fois plus grande que la Terre", 0),

		(21, "Le télescope James-Webb", 0),
		(21, "Voyager 1", 1),
		(21, "New Horizons", 0),
		(21, "Pioneer 10", 0),

		(22, "Neil Armstrong", 0),
		(22, "Charles Duke", 0),
		(22, "Alan Shepard", 0),
		(22, "Gene Cernan", 1),

		(23, "La comète de Hale-Bopp", 0),
		(23, "La comète Neowise", 0),
		(23, "La comète de Halley", 1),
		(23, "La comète Oumuamua", 0),

		(24, "La neuvième planète du Système Solaire", 0),
		(24, "Un satellite de Jupiter", 0),
		(24, "Une galaxie hélicoïdale", 0),
		(24, "Une des plus grosses étoiles connues", 1),

		(25, "UY Scuti", 0),
		(25, "Proxima Centauri", 1),
		(25, "Kepler-186", 0),
		(25, "Priate", 0)
		""")

		cur.execute("commit")

	# --- Getting Question ---

	def GetQuestionsCount():
		db_connection = sqlite3.connect('./db.db')
		db_connection.row_factory = sqlite3.Row

		cur = db_connection.cursor()

		cur.execute("SELECT COUNT(*) FROM Question")
		question_count = cur.fetchone()[0]

		return question_count


	def GetQuestions():
		db_connection = sqlite3.connect('./db.db')
		db_connection.row_factory = sqlite3.Row

		cur = db_connection.cursor()

		cur.execute("SELECT * FROM Question ORDER BY position")
		question_rows = cur.fetchall()

		questions = []
		for question_row in question_rows:
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

			questions.append(question.to_json())

		return json.dumps(questions)
	

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

