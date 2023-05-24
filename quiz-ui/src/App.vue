<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
    <div class="wrapper">
      <nav>
        <RouterLink to="/">Accueil</RouterLink>
        <RouterLink to="/start-new-quiz-page">Nouveau Quiz</RouterLink>
        <RouterLink to="/administration">Administration</RouterLink>
      </nav>
    </div>
  </header>

  <RouterView />
</template>

<style scoped>
header {
  line-height: 1.5;
  height: 5vh;
  margin-bottom: 2rem;
}

nav {
  width: 100%;
  font-size: 20px;
  text-align: center;
  margin-top: 2rem;
}

nav a.router-link-exact-active {
  color: rgb(238, 223, 149)
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  color: white;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:hover {
  -ms-transform: scale(1.15);
  transform: scale(1.15);
  background-color: transparent;
  color: rgb(239, 201, 14)
}


nav a:first-of-type {
  border: 0;
}
</style>
