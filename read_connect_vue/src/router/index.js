import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Dashboard from '../views/dashboard/Dashboard.vue'
import SignUp from '../views/SignUp.vue'
import Login from '../views/Login.vue'
import MyAccount from '../views/MyAccount.vue'
import BooksStore from '../views/dashboard/Books.vue'

import store from '../store'

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  },
  {
    path: '/sign-up/vue/',
    name: 'Signup',
    component: SignUp
  },
  {
    path: '/login/vue/',
    name: 'Login',
    component: Login
  },
  {
    path: '/dashboard/user_profile/',
    name: 'Dashboard',
    component: Dashboard,
    props: (route) => ({ userProfile: route.params.userProfile }), // Accept the parameter
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/dashboard/my-account/',
    name: 'MyAccount',
    component: MyAccount,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/dashboard/books-store-vue/',
    name: 'BooksStore',
    component: BooksStore,
    props: true,
    meta: {
      requireLogin: true
    }
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  console.log('Checking route:', to.name);
  if (to.matched.some(record => record.meta.requireLogin) && !store.state.isAuthenticated) {
    console.log('User is not authenticated, redirecting to login');
    next({ name: 'Login' }); // Navigate to the Login route by name
  } else {
    console.log('User is authenticated or route does not require login');
    next();
  }
});



export default router
