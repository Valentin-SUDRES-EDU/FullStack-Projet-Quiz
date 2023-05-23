<template>
  <main>
    <h1>Quiz</h1>

    <div class="content" v-if="beginQuiz">
      <form @submit.prevent="startQuiz">
        <label for="playerName">Entrez votre nom :</label>
        <input v-model="playerName" type="text" id="playerName" required />
        <button type="submit">Commencer le Quiz</button>
      </form>
    </div>
    <div class="content" v-if="quizStarted">
      <div>
        <h2>{{ question.title }}</h2>
        <p>{{ question.text }}</p>
        <div v-for="(answer, idx) in question.possibleAnswers" :key="idx">
          <input type="radio" :id="'answer-' + idx" :name="'question-' + question.position" :value="idx + 1"
            v-model="playerAnswers[question.position - 1]" />
          <label :for="'answer-' + idx">{{ answer.text }}</label>
        </div>
        <button v-if="question.position < quizSize" @click="loadNextQuestion">Question suivante</button>
        <button v-else @click="submitQuiz">Soumettre le Quiz</button>
      </div>
    </div>
  </main>
</template>

<script>
import QuizApiService from "@/services/QuizApiService";

export default {
  name: "NewQuizPage",
  data() {
    return {
      playerName: "",
      beginQuiz: true,
      quizStarted: false,
      question: {},
      playerAnswers: [],
      quizSize: 0,
    };
  },
  async created() {
    try {
      const response = await QuizApiService.getQuizInfo();
      this.quizSize = response.data.size;
      this.playerAnswers = new Array(this.quizSize).fill(null);
    } catch (error) {
      console.error(error);
    }
  },
  methods: {
    startQuiz() {
      this.quizStarted = true;
      this.beginQuiz = false;
      this.loadNextQuestion();
    },
    async loadNextQuestion() {
      try {
        const position = this.question.position ? this.question.position + 1 : 1;
        const response = await QuizApiService.getQuestion(position);
        this.question = response.data;
      } catch (error) {
        console.error(error);
      }
    },
    async submitQuiz() {
      const iData = {
        playerName: this.playerName,
        answers: this.playerAnswers,
      };
      console.log(iData);
      try {
        const response = await QuizApiService.submitQuiz(iData);
        alert(`Votre score est de ${response.data.score} !`);
      } catch (error) {
        console.error(error);
      }
    },
  },
};
</script>

<style>
form {
  text-align: center;
  margin: 10px auto 10px auto;
  display: block;
}

form label {
  text-align: center;
  margin: 10px auto 10px auto;
  font-size: 20px;
}

form input {
  margin: 10px auto 10px auto;
  text-align: center;
  display: block;

}

form button {
  margin: 10px auto 10px auto;
  display: block;
}

input {
  margin-right: 10px;
}

button {
  margin-top: 20px;
}
</style>