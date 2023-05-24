import axios from "axios";

const instance = axios.create({
  baseURL: `${import.meta.env.VITE_API_URL}`,
  json: true
});

var token = null;

export default {
  async call(method, resource, data = null) {
    var headers = {
      "Content-Type": "application/json",
    };
    if (this.token != null) {
      headers.authorization = "Bearer " + this.token;
    }

    return instance({
      method,
      headers: headers,
      url: resource,
      data,
    })
      .then((response) => {
        return { status: response.status, data: response.data };
      })
      .catch((error) => {
        console.error(error);
      });
  },

  getQuizInfo() {
    return this.call("get", "quiz-info");
  },
  getAllQuestions() {
    return this.call("get", "questions/all");
  },
  getQuestion(position) {
    return this.call("get", `questions?position=${position}`);
  },
  submitQuiz(iData) {
    return this.call("post", "participations", iData);
  },

  addQuestion(question) {
    return this.call("post", "questions", question);
  },
  editQuestion(position, question) {
    return this.call("put", "questions/" + position, question);
  },

  deleteQuestion(question) {
    return this.call("delete", "questions/" + question);
  },


  login(password) {
    return this.call("post", "login", password);
  },

  deleteParticipants() {
    return this.call("delete", "participations/all");
  },
  resetQuestions() {
    return this.call("post", "repopulate-default");
  },
  resetEverything() {
    return this.call("post", "rebuild-db");
  }


};