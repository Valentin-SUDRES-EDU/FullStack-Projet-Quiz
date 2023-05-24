<template>
  <div>
    <h4>Question {{ question.position }} - {{ question.title }}</h4>
    <h3>{{ question.text }}</h3>
    <img v-if="question.image" :src="question.image" alt="Question image" />
    <div>
      <button class="answers" v-for="(answer, idx) in question.possibleAnswers" :key="idx"
        @click="$emit('answer-selected', idx)">
        {{ answer.text }}
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: "QuestionDisplay",
  props: {
    question: {
      type: Object,
      required: true,
    },
  },
  emits: ['answer-selected']
};
</script>

<style scoped>
img {
  max-height: 200px;
  border: 1px solid black;
  margin: 50px auto;
}

.answers {
  width: 100%;
  height: 40px;
  border: 0;
  background: lightblue;
  margin-bottom: 10px;
}
</style>
