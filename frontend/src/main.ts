import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'

// 样式文件
import 'element-plus/dist/index.css'
import './styles/index.scss'
import './styles/input-fix.scss'

const app = createApp(App)

// 使用插件
app.use(createPinia())
app.use(router)

app.mount('#app') 