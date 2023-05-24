<template>
  <div>
    <!-- <h3>Question {{ currentQuestion.position }} / {{ totalNumberOfQuestion }}</h3> -->
    <QuestionDisplay :question="currentQuestion" @answer-selected="answerClickedHandler" />
  </div>
</template>

<script>
import QuestionDisplay from './QuestionDisplay.vue';
import QuizApiService from '@/services/QuizApiService';

export default {
  name: "QuestionsManager",
  components: {
    QuestionDisplay,
  },
  data() {
    return {
      currentQuestion: {},
      totalNumberOfQuestion: 0,
    };
  },
  created() {
    this.loadQuizInfo();
    this.loadQuestionByPosition(1);
  },
  methods: {
    async loadQuizInfo() {
      try {
        const response = await QuizApiService.getQuizInfo();
        this.totalNumberOfQuestion = response.data.size;
      } catch (error) {
        console.error(error);
      }
    },
    async loadQuestionByPosition(position) {
      try {
        const response = await QuizApiService.getQuestion(position);
        this.currentQuestion = response.data;
      } catch (error) {
        console.error(error);
      }
    },
    answerClickedHandler(answerIndex) {
      localStorage.setItem('q' + this.currentQuestion.position, answerIndex + 1);

      if (this.currentQuestion.position < this.totalNumberOfQuestion) {
        this.loadQuestionByPosition(this.currentQuestion.position + 1);
      } else {
        this.endQuiz();
      }
    },
    async endQuiz() {
      this.$router.push('/results');
    },
  },
};
</script>

<style scoped></style>
