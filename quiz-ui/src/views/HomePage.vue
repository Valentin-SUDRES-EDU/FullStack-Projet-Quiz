<template>
  <main>
    <h1>Home</h1>
    <router-link to="/start-new-quiz-page">Démarrer le quiz !</router-link>

    <div class="content" v-if="this.registeredScores.length > 0">
      Les Meilleurs Scores
      <table>
        <tr>
          <th>Name</th>
          <th>Score</th>
        </tr>
        <tr v-for="scoreEntry in this.registeredScores" v-bind:key="scoreEntry.date">
          <td>{{ scoreEntry.playerName }}</td>
          <td>{{ scoreEntry.score }}</td>
        </tr>
      </table>
    </div>
    <div class="content" v-else>
      Aucune participation... pour le moment. Soyez le premier à participer !
    </div>
  </main>
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
      this.registeredScores = response.data.scores;
    } catch (error) {
      console.error(error);
    }
  }
};
</script>

<style>
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