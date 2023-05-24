<template>
  <main>
    <h1>Admin Panel</h1>
    <div class="content" v-if="!authenticated">
      <input type="password" v-model="password" placeholder="Password">
      <button @click="login">Login</button>
    </div>
    <div class="content" v-else>
      <h2>Manage Questions</h2>
      <div>
        <ul>
          <li draggable="true" v-for="(question, index) in this.questions" :key="index" class="question">
            <img draggable="false" :src="question.image" alt="Image de la question">
            <div draggable="false" class="question-card-text">
              <h2 draggable="false">Question {{ question.position }} - {{ question.title }}</h2>
              <p draggable="false">{{ question.text }}</p>
            </div>
            <div draggable="false" class="question-card-actions">
              <button draggable="false" @click="editQuestion(question)"><img draggable="false"
                  src="./../assets/img/Button_Edit.png" alt="edit question button"></button>
              <button draggable="false" @click="deleteQuestion(question)"><img draggable="false"
                  src="./../assets/img/Button_Erase.png" alt="delete question button"></button>
            </div>
            <div draggable="false" class="question-card-actions">
              <button v-if="index > 0" draggable="false" @click="moveQuestionUp(question)">
                <img draggable="false" src="./../assets/img/Button_ArrowUp.png" alt="move question up button">
              </button>
              <button v-if="index < questions.length - 1" draggable="false" @click="moveQuestionDown(question)">
                <img draggable="false" src="./../assets/img/Button_ArrowDown.png" alt="move question down button">
              </button>
            </div>

          </li>
        </ul>
      </div>

      <h2>Manage Data</h2>
      <button @click="ResetParticipation">Reset Participation</button>
      <button @click="RevertQuestions">Revert Changes to Questions</button>
      <button @click="ResetEverything">Reset All</button>
    </div>
  </main>
</template>

<script>
import QuizApiService from "@/services/QuizApiService";

export default {
  data() {
    return {
      password: '',
      authenticated: false,
      token: '',
      questions: []
    }
  },
  methods: {
    async login() {
      try {
        const res = await QuizApiService.login({ "password": this.password });
        if (res.status === 200) {
          this.authenticated = true;
          this.token = res.data.token;
          QuizApiService.token = this.token;
          this.GetAllQuestions();

        } else {
          alert('Invalid password');
        }
      } catch (error) {
        console.error(error);
      }
    },

    async GetAllQuestions() {
      try {
        const res = await QuizApiService.getAllQuestions();
        if (res.status === 200) {
          this.questions = res.data;
        } else {
          alert('Unable to Get Questions! Error: ' + res.data.error);
        }
      } catch (error) {
        console.error(error);
      }
    },

    async ResetParticipation() {
      try {
        const res = await QuizApiService.deleteParticipants();
        if (res.status === 204) {
          alert('Participation successfully deleted');
        } else {
          alert('Unable to Reset Participation! Error: ' + res.data.error);
        }
      } catch (error) {
        console.error(error);
      }
    },
    async RevertQuestions() {
      try {
        const res = await QuizApiService.resetQuestions();
        if (res.status === 200) {
          alert('Questions successfully reseted');
          this.GetAllQuestions();
        } else {
          alert('Unable to Reset Questions! Error: ' + res.data.error);
        }
      } catch (error) {
        console.error(error);
      }
    },
    async ResetEverything() {
      try {
        const res = await QuizApiService.resetEverything();
        if (res.status === 200) {
          alert('Everything successfully deleted');
          this.questions = []
        } else {
          alert('Unable to Reset Everything! Error: ' + res.data.error);
        }
      } catch (error) {
        console.error(error);
      }
    },


    async moveQuestionUp(question) {
      let currentPosition = question.position;
      question.position--;
      try {
        const res = await QuizApiService.editQuestion(currentPosition, question);
        if (res.status === 204) {
          alert('Question Moved Up');
          this.GetAllQuestions();
        } else {
          alert('Unable to move question! Error: ' + res.data.error);
          question.position++;
        }
      } catch (error) {
        console.error(error);
      }
    },
    async moveQuestionDown(question) {
      let currentPosition = question.position;
      question.position++;
      try {
        const res = await QuizApiService.editQuestion(currentPosition, question);
        if (res.status === 204) {
          alert('Question Moved Down');
          this.GetAllQuestions();
        } else {
          alert('Unable to move question! Error: ' + res.data.error);
          question.position--;
        }
      } catch (error) {
        console.error(error);
        question.position--;
      }
    },
    async editQuestion(question) {
      // Code pour éditer la question
    },
    async deleteQuestion(question) {
      try {
        const res = await QuizApiService.deleteQuestion(question.position);
        if (res.status === 204) {
          alert('Question Deleted');
          this.GetAllQuestions();
        } else {
          alert('Unable to delete question! Error: ' + res.data.error);
        }
      } catch (error) {
        console.error(error);
      }
    }
  }
};
</script>

<style>
.question {
  display: flex;
  flex-direction: row;
  min-height: 100px;
  margin-bottom: 5px;
  border: 1px solid gray;
  padding: 5px;
}

.question:nth-child(2n) {
  background-color: lightcyan;
}

.question img {
  height: 100px;
  width: 100px;
}

.question-card-text {
  display: flex;
  flex-direction: column;
  height: 100%;
  flex: 1;
}

.question-card-text h2 {
  font-size: 15px;
  height: 30px;
  line-height: 30px;
  margin: 0;
}

.question-card-text p {
  height: 70%;
  font-size: 15px;
  margin: 0;
}

.question-card-actions {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.question-card-actions button {
  height: 50%;
  width: 50px;
  overflow: hidden;
  border: 0;
  background-color: initial;
  margin: 0;
  padding: 5px;
}

.question-card-actions button img {
  display: block;
  margin: 0 auto;
  height: 100%;
  width: 100%;
}
</style>