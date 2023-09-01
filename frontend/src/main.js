import { createApp } from 'vue'
import App from './App.vue'
import router from './router/index';
import './style.css';
import axios from 'axios';
import store from './store.js';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';
import Cookies from 'js-cookie';

//main entry point - across refreshes this will update the vuex store from the uploaded cookie

const app = createApp(App);
app.use(store); //vuex
app.use(router);
app.config.globalProperties.$http = axios;
//Mount APP on the dom
app.mount('#app');