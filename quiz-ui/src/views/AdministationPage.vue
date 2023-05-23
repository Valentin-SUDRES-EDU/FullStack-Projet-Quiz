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
          <li v-for="(question, index) in this.questions" :key="index" class="question">
            <img :src="question.image" alt="Image de la question">
            <div class="question-card-text">
              <h2>{{ question.title }}</h2>
              <p>{{ question.text }}</p>
            </div>
            <div class="question-card-actions">
              <button @click="editQuestion(index)">Modifier</button>
              <button @click="deleteQuestion(index)">Supprimer</button>
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
          alert('Unable to Get Questions! Error: ' + res.data);
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
          alert('Unable to Reset Participation! Error: ' + res.data);
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
          alert('Unable to Reset Questions! Error: ' + res.data);
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
          alert('Unable to Reset Everything! Error: ' + res.data);
        }
      } catch (error) {
        console.error(error);
      }
    },
    editQuestion(index) {
      // Code pour éditer la question
    },
    deleteQuestion(index) {
      // Code pour supprimer la question
    }
  }
};
</script>

<style>
.question {
  display: flex;
  flex-direction: row;
  height: 100px;
  margin-bottom: 5px;
  border: 1px solid gray;
}

.question:nth-child(2n) {
  background-color: lightgray;
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
  height: 50px;
  line-height: 50px;
  margin: 0;
}

.question-card-text p {
  height: 50%;
  font-size: 15px;
  margin: 0;
  line-height: 50px;
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
}
</style>