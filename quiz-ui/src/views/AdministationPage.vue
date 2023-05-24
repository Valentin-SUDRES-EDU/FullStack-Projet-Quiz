<template>
  <main>
    <Notification :notifications="notifications" />
    <div>
      <h1>Panel d'Administration</h1>
      <button v-if="authenticated" @click="disconnect" class="disconnectButton">Se Déconnecter</button>
    </div>
    <div class="content prompt" v-if="!authenticated">
      <label for="playerName">Entrez le mot de passe :</label>
      <input type="password" v-model="password" placeholder="Password">
      <button @click="login">Login</button>
    </div>
    <div class="content" v-else>
      <h2>Gestion des Questions</h2>
      <edit-question-modal v-if="questionToEdit" :question="questionToEdit" @save="saveQuestion"
        @close="questionToEdit = null" />
      <div class="questionList">
        <ul>
          <li v-for="(question, index) in this.questions" :key="index" class="question">
            <img :src="question.image" alt="Image de la question">
            <div class="question-card-text">
              <h2>Question {{ question.position }} - {{ question.title }}</h2>
              <p>{{ question.text }}</p>
            </div>
            <div class="question-card-actions">
              <button @click="editQuestion(question)">
                <img draggable="false" src="./../assets/img/Button_Edit.png" alt="edit question button">
              </button>
              <button @click="deleteQuestion(question)">
                <img draggable="false" src="./../assets/img/Button_Erase.png" alt="delete question button">
              </button>
            </div>
          </li>
        </ul>
      </div>
      <button @click="addQuestion">Ajouter une question</button>

      <h2>Gestion des Données</h2>
      <button @click="ResetParticipation">Supprimer les participations</button>
      <button @click="RevertQuestions">Remettre les questions par défaut</button>
      <button @click="ResetEverything">Tout supprimer</button>
    </div>
  </main>

  <div v-if="questionToEdit" class="modal">
    <div>
      <h2 v-if="originalQuestion">Modifier la Question {{ originalQuestion.position }}</h2>
      <h2 v-else>Ajouter une Question</h2>
      <form @submit.prevent="submitForm" class="EditQuestionModal">
        <h4>Question</h4>
        <label>
          <span>Titre</span>
          <input type="text" v-model="questionToEdit.title">
        </label>
        <label>
          <span>Texte</span>
          <input type="text" v-model="questionToEdit.text">
        </label>
        <label>
          <span>Image</span>
          <input type="file" @change="handleFileUpload">
        </label>
        <label>
          <span>Position</span>
          <select v-model.number="questionToEdit.position">
            <option v-for="n in (isAddingQuestion ? questions.length + 1 : questions.length)" :key="n" :value="n">{{ n }}
            </option>
          </select>
        </label>
        <h4>Réponses</h4>
        <div class="answer" v-for="(answer, index) in questionToEdit.possibleAnswers" :key="index">
          <label>
            <span>Réponse {{ index + 1 }}</span>
            <input type="radio" :value="index" v-model="correctAnswerIndex">
            <input type="text" v-model="answer.text">
          </label>
        </div>
        <div>
          <button type="submit">Valider</button>
          <button type="button" @click="close">Annuler</button>
        </div>

      </form>
    </div>
  </div>
</template>

<script>
import QuizApiService from "@/services/QuizApiService";
import Notification from '@/components/Notification.vue'

export default {

  data() {
    return {
      password: '',
      authenticated: false,
      token: '',
      questions: [],
      questionToEdit: null,
      originalQuestion: null,
      correctAnswerIndex: null,
      isAddingQuestion: false,
      notifications: [],
    }
  },

  components: {
    Notification
  },

  created() {
    const token = window.sessionStorage.getItem('token');
    if (token) {
      this.token = token;
      QuizApiService.token = this.token;
      this.authenticated = true;
      this.GetAllQuestions();
    }
  },

  methods: {

    async login() {
      this.addNotification('Connexion en cours...', '', 'neutre');
      try {
        const res = await QuizApiService.login({ "password": this.password });
        if (res.status === 200) {
          this.authenticated = true;
          this.token = res.data.token;
          QuizApiService.token = this.token;
          this.GetAllQuestions();
          window.sessionStorage.setItem('token', this.token);

          this.addNotification('Connection Réussie', '', 'validation');
        } else {
          this.addNotification('Impossible de se connecter', 'Erreur: ' + res.data, 'erreur');
        }
      } catch (error) {
        console.error(error);
      }
    },

    disconnect() {
      this.addNotification('Déconnexion...', '', 'neutre');
      this.token = null;
      window.sessionStorage.removeItem('token');
      QuizApiService.token = this.token;
      location.reload();

      this.addNotification('Déconnection Réussie', '', 'validation');
    },

    addNotification(titre, texte, type) {
      this.notifications.push({
        titre: titre,
        texte: texte,
        type: type,
        id: Date.now()
      });

      setTimeout(() => {
        this.notifications.shift();
      }, 5000);
    },

    async GetAllQuestions() {
      try {
        const res = await QuizApiService.getAllQuestions();
        if (res.status === 200) {
          this.questions = res.data;
        } else if (res.status === 401) {
          this.disconnect();
        } else {
          alert('Unable to Get Questions!', 'Erreur: ' + res.data.error, 'erreur');
        }
      } catch (error) {
        console.error(error);
      }
    },

    async ResetParticipation() {
      this.addNotification('Suppression des participations', '', 'neutre');
      try {
        const res = await QuizApiService.deleteParticipants();
        if (res.status === 204) {
          this.addNotification('Participations supprimées avec succès', '', 'validation');
        } else if (res.status === 401) {
          this.disconnect();
        } else {
          this.addNotification('Impossible de supprimer les participations !', 'Erreur: ' + res.data.error, 'erreur');
        }
      } catch (error) {
        console.error(error);
      }
    },

    async RevertQuestions() {
      this.addNotification('Restauration des questions par défaut...', '', 'neutre');
      try {
        const res = await QuizApiService.resetQuestions();
        if (res.status === 200) {
          this.addNotification('Restauration des questions par défaut effectuée', '', 'validation');
          this.GetAllQuestions();
        } else if (res.status === 401) {
          this.disconnect();
        } else {
          this.addNotification('Impossible de restaurer les questions par défaut !', 'Erreur: ' + res.data.error, 'erreur');
        }
      } catch (error) {
        console.error(error);
        this.addNotification('Impossible de remettre les questions par défaut !', '', 'erreur');
      }
    },

    async ResetEverything() {
      this.addNotification('Remise à zéro...', '', 'neutre');
      try {
        const res = await QuizApiService.resetEverything();
        if (res.status === 200) {
          this.addNotification('Remise à zéro effectuée', '', 'validation');
          this.questions = []
        } else if (res.status === 401) {
          this.disconnect();
        } else {
          this.addNotification('Impossible de remettre tout à zéro !', 'Erreur: ' + res.data.error, 'erreur');
        }
      } catch (error) {
        console.error(error);
        this.addNotification('Impossible de remettre tout à zéro !', '', 'erreur');
      }
    },

    addQuestion() {
      this.isAddingQuestion = true;
      this.originalQuestion = null;
      this.questionToEdit = {
        title: "",
        text: "",
        image: "",
        position: this.questions.length + 1,
        possibleAnswers: [
          { text: "", isCorrect: false },
          { text: "", isCorrect: false },
          { text: "", isCorrect: false },
          { text: "", isCorrect: false }
        ]
      };
      this.correctAnswerIndex = null;
    },

    editQuestion(question) {
      this.isAddingQuestion = false;
      this.originalQuestion = question;
      this.questionToEdit = JSON.parse(JSON.stringify(question));
      this.correctAnswerIndex = question.possibleAnswers.findIndex(answer => answer.isCorrect);
    },

    handleFileUpload(e) {
      const file = e.target.files[0];
      const reader = new FileReader();
      reader.onload = () => {
        this.questionToEdit.image = reader.result;
      };
      reader.readAsDataURL(file);
    },

    async submitForm() {
      this.questionToEdit.possibleAnswers.forEach((answer, index) => {
        answer.isCorrect = (index === this.correctAnswerIndex);
      });

      let res;
      if (this.originalQuestion) {
        this.addNotification('Modification de la question en cours', '', 'neutre');
        res = await QuizApiService.editQuestion(this.originalQuestion.position, this.questionToEdit);
      } else {
        this.addNotification("Ajout d'une nouvelle question", '', 'neutre');
        res = await QuizApiService.addQuestion(this.questionToEdit);
      }

      if (res.status === 200 || res.status === 204) {
        this.addNotification(this.originalQuestion ? 'Question modifiée' : 'Question ajoutée', '', 'validation');
        this.close();
        this.GetAllQuestions();
      } else if (res.status === 401) {
        this.disconnect();
      } else {
        this.addNotification(this.originalQuestion ? 'Impossible de modifier la question...' : "Impossible d'ajouter la question...", 'Erreur: ' + res.data.error, 'erreur');
        alert('Unable to update or create question! Error: ' + res.data.error);
      }
      this.isAddingQuestion = false;
    },


    close() {
      this.questionToEdit = null;
      this.isAddingQuestion = false;
    },

    async deleteQuestion(question) {
      this.addNotification('Suppression de la question en cours', '', 'neutre');
      try {
        const res = await QuizApiService.deleteQuestion(question.position);
        if (res.status === 204) {
          this.addNotification('Question supprimée', '', 'validation');
          this.GetAllQuestions();
        } else if (res.status === 401) {
          this.disconnect();
        } else {
          this.addNotification('Impossible de supprimer la question...', 'Erreur: ' + res.data.error, 'erreur');
        }
      } catch (error) {
        this.addNotification('Impossible de supprimer la question...', '', 'erreur');
        console.error(error);
      }
    }
  }
};
</script>

<style scoped>
h1 {
  float: left;
  width: 70%;
}

.disconnectButton {
  width: 20%;
  float: right;
}

h2 {
  margin: 20px auto;
}

.questionList {
  overflow: auto;
  max-height: 30vh;
}

.question {
  display: flex;
  flex-direction: row;
  min-height: 100px;
  margin-bottom: 5px;
  border: 1px solid gray;
  padding: 5px;
}

.question:nth-child(2n) {
  background-color: lightcyan;
}

.question img {
  height: 100px;
  width: 100px;
  margin-right: 5px;
  object-fit: cover;
}

.question-card-text {
  display: flex;
  flex-direction: column;
  height: 100%;
  flex: 1;
}

.question-card-text h2 {
  font-size: 15px;
  height: 30px;
  line-height: 30px;
  margin: 0;
}

.question-card-text p {
  height: 70%;
  font-size: 15px;
  margin: 0;
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
  border: 0;
  background-color: initial;
  margin: 0;
  padding: 5px;
}

.question-card-actions button img {
  display: block;
  margin: 0 auto;
  height: 100%;
  width: 100%;
}

.modal {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal>div {
  background: #fff;
  padding: 20px;
  border-radius: 5px;
  width: 80%;
  max-width: 500px;
}

.EditQuestionModal {
  display: flex;
  flex-direction: column;
}

.EditQuestionModal h4 {
  margin-top: 15px;
}

.EditQuestionModal label {
  width: 100%;
  margin-bottom: 10px;
  height: 30px;
}

.EditQuestionModal div {
  width: 100%;
  margin-bottom: 5px;
}

.EditQuestionModal label span {
  display: inline-block;
  width: 30%;
}

.EditQuestionModal label input,
.EditQuestionModal label select {
  display: inline-block;
  width: 60%;
  height: 30px;
}

.answer label span {
  display: inline-block;
  width: 20%;
}

.answer label input:nth-child(2n) {
  display: inline-block;
  width: 10%;
  height: 15px;
}

.answer label input:nth-child(3n) {
  display: inline-block;
  width: 60%;
}
</style>