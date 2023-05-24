<template>
  <div class="notification-container">
    <transition-group name="list">
      <div v-for="notification in notifications" :key="notification.id" class="notification" :class="notification.type">
        <h7>{{ notification.titre }}</h7>
        <p>{{ notification.texte }}</p>
      </div>

    </transition-group>
  </div>
</template>

<script>
export default {
  props: ['notifications'],
}
</script>

<style scoped>
.notification-container {
  position: fixed;
  top: 10px;
  right: 10px;
}

.notification {
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 5px;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
}

.notification.validation {
  background-color: rgba(0, 255, 0, 0.5);
  color: white
}

.notification.validation p {
  display: none;
}

.notification.erreur {
  background-color: rgba(255, 0, 0, 0.5);
  color: white
}

.notification.neutre {
  background-color: rgba(0, 0, 255, 0.5);
  color: white
}

.notification.neutre p {
  display: none;
}
</style>
