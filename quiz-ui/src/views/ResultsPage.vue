<template>
  <main>
    <h1>Votre Score</h1>
    <p v-if="score != null" id="votreScore">Vous avez obtenu {{ this.score }} points !</p>
    <p v-else>Soumission des réponses en cours...</p>

    <div v-if="score == 25" class="divCom">
      <p>Soit vous êtes le créateur de ce quiz, soit vous êtes le meilleur des quizonautes !</p>
    </div>

    <div v-if="score > 20 && score < 25" class="divCom">
      <p>Félicitations ! Vous êtes un quizonaute aguerri, bientôt l'Univers n'aura plus de secret pour vous !</p>
    </div>

    <div v-if="score > 13 && score <= 20" class="divCom">
      <p>Bien joué ! Vous êtes un quizonaute averti, mais attention aux astéroides !</p>
    </div>

    <div v-if="score < 13 && score > 5" class="divCom">
      <p>Vous êtes un quizonaute débutant, potassez un peu avant de grimper dans votre fusée !</p>
    </div>

    <div v-if="score <= 5" class="divCom">
      <p>Vous n'êtes pas encore un quizonaute, mais ça va venir !</p>
    </div>

    

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

a {
  display:inline-block;
  vertical-align: baseline;
  width: 100%;
  line-height: 50px;
  text-align: center;
  margin-top: 20px;
  margin-bottom: 10px;
  height: 50x;
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

#votreScore{
  font-size: 25px;
  font-weight: bold;
  color:#3b45dd;
  
}
.divCom{
  font-size: 19px;

}
</style>
