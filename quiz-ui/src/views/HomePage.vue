<template>
  <main>
    <h1>Accueil</h1>
    <div>
      <div>
        <router-link id="startQuizz" to="/start-new-quiz-page">Démarrer le quiz !</router-link>
      </div>
      <div>
        <div id="scores" class="content" v-if="this.registeredScores.length > 0">
          <p>Les Meilleurs Scores</p>
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
      </div>
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

<style scoped>
main div {
  display: flex;
  flex-direction: row-reverse;
}

main div div {
  width: 50%
}

a {
  vertical-align: baseline;
  width: 100%;
  line-height: 50px;
  text-align: center;
  margin-bottom: 10px;
  height: 50px;
  border: none;
  border-radius: 40px;
  font-size: 18px;
  color: white;
  font-weight: bolder;
  background: rgb(7, 7, 161);
  background: linear-gradient(90deg, rgba(7, 7, 161, 0.5) 0%, rgba(13, 104, 152, 0.5) 48%, rgba(0, 142, 171, 0.5) 100%);
}

a:hover {
  border: none;
  background: rgb(161, 139, 7);
  background: linear-gradient(-90deg, rgba(161, 139, 7, 0.5) 0%, rgba(0, 142, 171, 0.5) 100%);
}

#scores {
  width: 100%;
  display: block;
}

#scores table {
  border: 2px solid black;
  border-collapse: collapse;
  text-align: center;
  margin: auto;
}

#scores p {
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