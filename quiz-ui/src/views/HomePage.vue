<template>
  <h1>Home</h1>

  <router-link to="/start-new-quiz-page">Démarrer le quiz !</router-link>

  <table>
    <tr>
      <th>Name</th>
      <th>Score</th>
    </tr>
    <tr v-for="scoreEntry in this.registeredScores.scores" v-bind:key="scoreEntry.date">
      <td>{{ scoreEntry.playerName }}</td>
      <td>{{ scoreEntry.score }}</td>
    </tr>
  </table>
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

<style>
h1 {
  font-size: 40px;
  font-weight: bolder;
  margin-bottom: 2vh;
}

table {
  border: 2px solid black;
  border-collapse: collapse;
  text-align: center;
}

tr {
  height: 25px;
}

tr:nth-of-type(2) {
  background: gold;
}

tr:nth-of-type(3) {
  background: silver;
}

tr:nth-of-type(4) {
  background: #cd7f32;
}

th {
  font-weight: bold;
  color: white;
  background-color: black;
}

td {
  width: 100px;
  border: 1px solid black;
}
</style>