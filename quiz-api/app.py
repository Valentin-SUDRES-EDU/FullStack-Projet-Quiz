from flask import Flask, request
from flask_cors import CORS
from jwt_utils import *
from question import *
from participation import *
import hashlib

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
	x = 'world'
	return f"Hello, {x}"

@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
	
	try:
		question_count = Question.GetQuestionsCount()
	except ValueError:
		return {"error": ValueError}, 402

	try:
		scores = Participation.ScoresCalculation()
	except ValueError:
		return {"error": ValueError}, 402

	return {"size": question_count, "scores": scores}, 200


@app.route('/login', methods=['POST'])
def Login():
	payload = request.get_json()

	hashed = hashlib.md5(payload['password'].encode('UTF-8')).digest()
	if hashed == b'\xebC\xbb\xd3 \x89p\xa7\x9ef\xae\x15z\x8d3\x96':
		return {"token": build_token()}, 200
	else:
		return 'Unauthorized', 401
	

@app.route('/questions/<int:question_id>', methods=['GET'])
def RecupererQuestionParID(question_id):

	try:
		value = Question.GetQuestionByID(question_id)
	except ValueError:
		return {"error": ValueError}, 402

	if value == None:
		return {"error": "No corresponding question found with this id"}, 404
	else:
		return value, 200


@app.route('/questions', methods=['GET'])
def RecupererQuestionParPosition():
	
	question_position = request.args.get('position', default = 1, type = int)
	
	try:
		value = Question.GetQuestionByPosition(question_position)
	except ValueError:
		return {"error": ValueError}, 402
	
	if value == None:
		return {"error": "No corresponding question found with this position"}, 404
	else:
		return value, 200

	
@app.route('/questions', methods=['POST'])
def AjouterQuestion():
	
	try:
		TestConnection(request)
	except ValueError:
		return 'Unauthorized', 401

	payload = request.get_json()
	try:
		value = Question.Add(payload)
	except ValueError:
		return {"error": ValueError}, 402

	return {"id": value}, 200


@app.route('/questions/<int:question_id>', methods=['PUT'])
def MettreAJourQuestion(question_id):
    try:
        TestConnection(request)
    except ValueError:
        return 'Unauthorized', 401

    question_details = request.get_json()
    
    try:
        value = Question.UpdateQuestion(question_id, question_details)
    except ValueError:
        return {"error": ValueError}, 402

    if value == "Error updating question":
        return {"error": "No corresponding question found with this position, unable to update"}, 404
    else:
        return value, 204


@app.route('/questions/<int:question_id>', methods=['DELETE'])
def SupprimerQuestion(question_id):

	try:
		TestConnection(request)
	except ValueError:
		return 'Unauthorized', 401

	try:
		value = Question.DeleteQuestionByIDAndUpdatePositions(question_id)
	except ValueError:
		return {"error": ValueError}, 402

	if value == "Error deleting question":
		return {"error": "No corresponding question found with this position, unable to delete"}, 404
	else:
		return value, 204


@app.route('/questions/all', methods=['DELETE'])
def SupprimerToutesQuestions():

	try:
		TestConnection(request)
	except ValueError:
		return 'Unauthorized', 401
	
	try:
		value = Question.DeleteAllQuestions()
	except ValueError:
		return {"error": ValueError}, 402

	return value, 204


@app.route('/participations/all', methods=['DELETE'])
def SupprimerToutesParticipations():

	try:
		TestConnection(request)
	except ValueError:
		return 'Unauthorized', 401
	
	try:
		value = Participation.DeleteAllParticipations()
	except ValueError:
		return {"error": ValueError}, 402

	return {}, 204



@app.route('/participations', methods=['POST'])
def recordParticipation():
    
	data = request.get_json()
	playerName = data.get("playerName")
	answers = data.get("answers")

	try:
		score = Participation.SaveParticipation(playerName, answers)
	except ValueError:
		return {"error": ValueError}, 402
	
	try:
		score = int(score)
	except ValueError:
		return {"error": score}, 400

	return {"playerName": playerName, "score": score}, 200
		


def TestConnection(request):
	token = request.headers.get('Authorization')
	if (token == None):
		raise ValueError
	token = token.replace('Bearer ', '')
	decode_token(token)



if __name__ == "__main__":
    app.run()
    

