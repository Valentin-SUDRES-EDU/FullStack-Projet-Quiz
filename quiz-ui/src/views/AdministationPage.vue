<template>
  <div id="admin">
    <h1>Admin Panel</h1>
    <div v-if="!authenticated">
      <input type="password" v-model="password" placeholder="Password">
      <button @click="login">Login</button>
    </div>
    <div v-else>
      <h2>Manage Questions</h2>
      <!-- Ici vos fonctionnalités d'administration (ajout, suppression, réorganisation des questions) -->
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      password: '',
      authenticated: false,
      token: ''
    }
  },
  methods: {
    async login() {
      try {
        const res = await axios.post('http://localhost:5000/login', { password: this.password });
        if (res.status === 200) {
          this.authenticated = true;
          this.token = res.data.token;
          axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`;
        } else {
          alert('Invalid password');
        }
      } catch (error) {
        console.error(error);
      }
    }
  }
}
</script>
