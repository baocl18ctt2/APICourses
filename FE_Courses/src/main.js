import Vue from 'vue'
import App from './App.vue'
// Thêm phần định nghĩa main.css
import './styles/main.css'
// Thêm url router
import './axios'
// Thêm thư viện boostrap
import './app'
// Thêm thư viện fontawesome
import '@fortawesome/fontawesome-free/css/all.css'
import '@fortawesome/fontawesome-free/js/all.js'

Vue.config.productionTip = false
    // Cài đặt và import vue-router
import VueRouter from 'vue-router'
import routes from './routes';
// Khởi tạo router
const router = new VueRouter({
    mode: 'history',
    routes // short for `routes: routes`
});
// Sử dụng view-router
Vue.use(VueRouter)

new Vue({
    router,
    render: h => h(App),
}).$mount('#app')