import {createRouter, createWebHistory} from 'vue-router'
import Home from '@/pages/HomePage.vue'
import Login from '@/pages/LoginPage.vue'
import Cart from '@/pages/CartPage.vue'
import Order from '@/pages/OrderPage.vue'
import Orders from "@/pages/OrdersPage.vue";

const routes = [
    {path:'/', component: Home},
    {path:'/login', component: Login},
    {path:'/cart', component: Cart},
    {path:'/order', component: Order},
    {path: '/orders', component: Orders}
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router;