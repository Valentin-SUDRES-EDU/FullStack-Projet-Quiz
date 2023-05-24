<template>
  <div>
    <div class="question">
      <div>
        <h4>Question {{ question.position }} - {{ question.title }}</h4>
        <h3>{{ question.text }}</h3>
      </div>
      <img v-if="question.image" :src="question.image" alt="Question image" />
    </div>
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
.question {
  display: flex;
  flex-direction: row;
  margin-bottom: 50px;
  align-content: space-between;
  justify-content: space-between;
  align-items: center;
}

.question div {
  display: flex;
  flex-direction: column;
}

.question div h4 {
  margin-bottom: 20px;
}

.question img {
  max-height: 200px;
  margin-left: 50px;
}

.answers {
  width: 100%;
  margin-bottom: 10px;
  height: 50px;
  border: none;
  border-radius: 40px;

  background: rgb(7, 7, 161);
  background: linear-gradient(90deg, rgba(7, 7, 161, 0.5) 0%, rgba(13, 104, 152, 0.5) 48%, rgba(0, 142, 171, 0.5) 100%);
}

.answers:hover {
  border: none;
  background: rgb(161, 139, 7);
  background: linear-gradient(-90deg, rgba(161, 139, 7, 0.5) 0%, rgba(0, 142, 171, 0.5) 100%);
}
</style>
