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
      <QuestionsManager @quiz-end="submitQuiz" />
    </div>
  </main>
</template>

<script>
import QuestionsManager from "@/components/QuestionsManager.vue";
import QuizApiService from "@/services/QuizApiService";

export default {
  name: "NewQuizPage",
  components: {
    QuestionsManager,
  },
  data() {
    return {
      playerName: "",
      beginQuiz: true,
      quizStarted: false,
    };
  },
  methods: {
    startQuiz() {
      localStorage.setItem('playerName', this.playerName);
      this.quizStarted = true;
      this.beginQuiz = false;
    },
    async submitQuiz(playerAnswers) {
      const playerName = localStorage.getItem('playerName');
      const quizData = {
        playerName,
        answers: playerAnswers,
      };
      try {
        const response = await QuizApiService.submitQuiz(quizData);
        alert(`Votre score est de ${response.data.score} !`);
      } catch (error) {
        console.error(error);
      }
    },
  },
};
</script>

<style scoped>
form {
  display: flex;
  flex-direction: column;
}

form label {
  text-align: center;
  margin-bottom: 20px;
  height: 50px;
  font-weight: bolder;
  font-size: 25px;
  line-height: 50px;
}

form input {
  text-align: center;
  font-weight: bolder;
  font-size: 25px;
  line-height: 50px;
  height: 50px;
  margin-bottom: 20px;
  border: 1.5px solid rgba(13, 104, 152, 0.5);
  border-radius: 40px;
}
</style>
