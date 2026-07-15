import { createApp } from 'vue'

import App from './App.vue'
import { router } from './core/router'

import './style.css'

const app = createApp(App)

app.use(router)
app.mount('#app')
