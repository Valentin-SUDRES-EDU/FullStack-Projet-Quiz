<template>
  <main>
    <h1>Admin Panel</h1>
    <div class="content prompt" v-if="!authenticated">
      <label for="playerName">Entrez le mot de passe :</label>
      <input type="password" v-model="password" placeholder="Password">
      <button @click="login">Login</button>
    </div>
    <div class="content" v-else>
      <h2>Manage Questions</h2>
      <edit-question-modal v-if="questionToEdit" :question="questionToEdit" @save="saveQuestion"
        @close="questionToEdit = null" />
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
          </li>
        </ul>
      </div>

      <h2>Manage Data</h2>
      <button @click="ResetParticipation">Reset Participation</button>
      <button @click="RevertQuestions">Revert Changes to Questions</button>
      <button @click="ResetEverything">Reset All</button>
    </div>
  </main>

  <div v-if="questionToEdit" class="modal">
    <div>
      <h2>Modifier la Question {{ originalQuestion.position }}</h2>
      <form @submit.prevent="submitForm" class="EditQuestionModal">
        <h4>Question</h4>
        <label>
          <span>Titre</span>
          <input type="text" v-model="questionToEdit.title">
        </label>
        <label>
          <span>Texte</span>
          <input type="text" v-model="questionToEdit.text">
        </label>
        <label>
          <span>Image</span>
          <input type="file" @change="handleFileUpload">
        </label>
        <label>
          <span>Position</span>
          <select v-model.number="questionToEdit.position">
            <option v-for="n in 25" :key="n" :value="n">{{ n }}</option>
          </select>
        </label>
        <h4>Réponses</h4>
        <div class="answer" v-for="(answer, index) in questionToEdit.possibleAnswers" :key="index">
          <label>
            <span>Réponse {{ index + 1 }}</span>
            <input type="radio" :value="index" v-model="correctAnswerIndex">
            <input type="text" v-model="answer.text">
          </label>
        </div>
        <div>
          <button type="submit">Valider</button>
          <button type="button" @click="close">Annuler</button>
        </div>

      </form>
    </div>
  </div>
</template>

<script>
import QuizApiService from "@/services/QuizApiService";

export default {

  data() {
    return {
      password: '',
      authenticated: false,
      token: '',
      questions: [],
      questionToEdit: null,
      originalQuestion: null,
      correctAnswerIndex: null
    }
  },

  created() {
    const token = window.sessionStorage.getItem('token');
    if (token) {
      this.token = token;
      QuizApiService.token = this.token;
      this.authenticated = true;
      this.GetAllQuestions();
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

          window.sessionStorage.setItem('token', this.token);
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

    editQuestion(question) {
      this.originalQuestion = question;
      this.questionToEdit = JSON.parse(JSON.stringify(question));
      this.correctAnswerIndex = question.possibleAnswers.findIndex(answer => answer.isCorrect);
    },

    handleFileUpload(e) {
      const file = e.target.files[0];
      const reader = new FileReader();
      reader.onload = () => {
        this.questionToEdit.image = reader.result;
      };
      reader.readAsDataURL(file);
    },

    async submitForm() {
      this.questionToEdit.possibleAnswers.forEach((answer, index) => {
        answer.isCorrect = (index === this.correctAnswerIndex);
      });

      const res = await QuizApiService.editQuestion(this.originalQuestion.position, this.questionToEdit);
      if (res.status === 204) {
        alert('Question Updated');
        this.GetAllQuestions();
      } else {
        alert('Unable to update question! Error: ' + res.data.error);
      }
      this.questionToEdit = null;
    },

    close() {
      this.questionToEdit = null;
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

<style scoped>
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
  margin-right: 5px;
  object-fit: cover;
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

.modal {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal>div {
  background: #fff;
  padding: 20px;
  border-radius: 5px;
  width: 80%;
  max-width: 500px;
}

.EditQuestionModal {
  display: flex;
  flex-direction: column;
}

.EditQuestionModal h4 {
  margin-top: 15px;
}

.EditQuestionModal label {
  width: 100%;
  margin-bottom: 10px;
  height: 30px;
}

.EditQuestionModal div {
  width: 100%;
  margin-bottom: 5px;
}

.EditQuestionModal label span {
  display: inline-block;
  width: 30%;
}

.EditQuestionModal label input,
.EditQuestionModal label select {
  display: inline-block;
  width: 60%;
  height: 30px;
}

.answer label span {
  display: inline-block;
  width: 20%;
}

.answer label input:nth-child(2n) {
  display: inline-block;
  width: 10%;
  height: 15px;
}

.answer label input:nth-child(3n) {
  display: inline-block;
  width: 60%;
}
</style>