import { createRouter, createWebHistory} from 'vue-router';
import UserList from '../components/UserList.vue';
import Login from '../components/Login.vue';
import Loggedin from '../components/Loggedin.vue';
import Logout from '../components/Logout.vue';
import Signup from '../components/Signup.vue';
import Profile from '../components/Profile.vue';
import Home from '../components/Home.vue';
import ItemList from '../components/ItemList.vue';
import AddItem from '../components/addItem.vue';
import userSelling from '../components/sellingOverview.vue';
import itemPage from '../components/itemPage.vue';
import itemUpdate from '../components/itemUpdate.vue';
import deleteItem from '../components/deleteItem.vue';

import { useStore} from 'vuex';
import store from '../store';
import Cookies from 'js-cookie';

const routes = [
  { path: '/', component: ItemList },
  { path: '/home', component: Home},
  { path: '/login', component: Login},
  { path: '/loggedin', component: Loggedin, meta: {requiresAuth: true} },
  { path: '/logout', component: Logout, meta: {requiresAuth: true} }, //
  { path: '/profile', component: Profile, meta: {requiresAuth: true} },
  { path: '/signup', component: Signup },
  { path: '/user-list', component: UserList},
  { path: '/add-item', component:AddItem, meta: {requiresAuth: true}},
  { path: '/selling', component:userSelling, meta: {requiresAuth: true}},
  { path: '/item', component: itemPage},
  //param uses colon: means dynamic segment
  { path: '/item-update/:itemId', name:'item-update', component: itemUpdate, meta:{requiresAuth: true}, props:true},
  { path: '/delete-item', component:deleteItem, meta:{requiresAuth: true}}
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// navigation guard
router.beforeEach((to, from, next) => {
  const isLoggedIn = store.getters.getIsAuthenticated;
  console.log("routerGuard, is user logged in? ", isLoggedIn);
  //checks if the route needs authentication, to check for isAuthenticated
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    // This route requires authentication
    if (!isLoggedIn) {
      console.log("not logged in")
      next('/');
    } else {
      //proceedCo
      next();
    }
  } else {
    next();
  }
});
export default router;
