<template>
  <h1>Home page</h1>

  <div v-for="scoreEntry in this.registeredScores.scores" v-bind:key="scoreEntry.date">
    {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
  </div>

  <router-link to="/start-new-quiz-page">Démarrer le quiz !</router-link>
</template>

<script>
import QuizApiService from "@/services/QuizApiService";

export default {
  name: "HomePage",
  data() {
    var registeredScores = []
    return {
      registeredScores
    };
  },
  async created() {
    try {
      const response = await QuizApiService.getQuizInfo();
      this.registeredScores = response.data;
    } catch (error) {
      console.error(error);
    }
  }
};
</script>

<style></style>