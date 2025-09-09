import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import Antd, { ConfigProvider } from 'ant-design-vue'
import es_ES from 'ant-design-vue/es/locale/es_ES';

import App from './App.vue'
import router from './router/index.js'

import 'ant-design-vue/dist/reset.css';

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.use(Antd)
app.component('a-config-provider', ConfigProvider);

app.config.globalProperties.$antConfigProvider = {
  locale: es_ES,
};

app.mount('#app')
