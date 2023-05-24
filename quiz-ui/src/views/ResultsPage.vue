<template>
  <main>
    <h1>Votre Score</h1>
    <p v-if="score != null">Vous avez obtenu {{ this.score }} points</p>
    <p v-else>Soumission des réponses en cours...</p>

    <router-link to="/">Revenir à l'accueil</router-link>
  </main>
</template>

<script>
import QuizApiService from "@/services/QuizApiService";

export default {
  name: 'ResultsPage',
  data() {
    return {
      score: null,
    }
  },
  created() {
    this.submitQuiz();
  },
  methods: {
    async submitQuiz() {
      let answersData = {};
      answersData.playerName = localStorage.getItem("playerName");
      answersData.answers = [];
      for (let i = 1; i < 26; i++) {
        answersData.answers.push(localStorage.getItem("q" + i) / 1);
      }

      try {
        const response = await QuizApiService.submitQuiz(answersData);
        this.score = response.data.score;
      } catch (error) {
        console.error(error);
      }
    },
  },


};
</script>

<style scoped>
/* Vos styles ici */
</style>
