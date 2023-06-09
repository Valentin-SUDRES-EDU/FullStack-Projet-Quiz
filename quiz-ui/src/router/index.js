import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import NewQuizPage from '../views/NewQuizPage.vue'
import AdministrationPage from '../views/AdministationPage.vue'
import ResultsPage from '../views/ResultsPage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'HomePage',
      component: HomePage
    },
    {
      path: '/start-new-quiz-page',
      name: 'NewQuizPage',
      component: NewQuizPage
    },
    {
      path: '/results',
      name: 'ResultsPage',
      component: ResultsPage
    },
    {
      path: '/administration',
      name: 'AdministrationPage',
      component: AdministrationPage
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    }
  ]
})

export default router
