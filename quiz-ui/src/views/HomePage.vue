<template>
  <h1>Home page</h1>
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
    console.log("Composant Home page 'created'");
    registeredScores = QuizApiService.getQuizInfo();
  }
};
</script>