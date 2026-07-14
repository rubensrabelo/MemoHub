import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../../modules/landing-page/views/HomeView.vue'
import KnowledgeListView from '../../modules/knowledge/views/KnowledgeListView.vue'

const routes = [
  {
    path: '/',
    name: 'landing',
    component: HomeView
  },
  {
    path: '/app',
    name: 'knowledge',
    component: KnowledgeListView
  }
]

export const router = createRouter({
  history: createWebHistory(),
  routes
})
