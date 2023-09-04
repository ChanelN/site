<script>
/*import components here*/
import { defineComponent, ref , onBeforeUnmount, computed, onMounted} from 'vue';
import { mapGetters, mapState, useStore } from 'vuex';
import { useRouter } from 'vue-router';
import UserList from './components/UserList.vue';
import Logout from './components/Logout.vue';
import Login from './components/login.vue';
import signup from './components/signup.vue';
import Loggedin from './components/Loggedin.vue';
import Home from './components/Home.vue';
import ItemList from './components/ItemList.vue';
import AddItem from './components/addItem.vue';
import sellingOverview from './components/sellingOverview.vue';
import itemPage from './components/itemPage.vue';

//setup is for reactive data properties - the setup() returns obj containing
//data and functions you want to use in the componenets
export default {
  name: 'App',
  components: {
    UserList,
    Logout,
    Login,
    Loggedin,
    signup,
    Home,
    ItemList,
    AddItem,
    sellingOverview,
    itemPage,
},
computed:{
    shouldShowNavBar() {
      // Get the current route path from the Vue Router
      const currentRoute = this.$route.path;
      // Add the route paths for which the navigation bar should be hidden
      const hiddenRoutes = ['/login','/signup',];
      // Check if the current route is in the hiddenRoutes array
      return !hiddenRoutes.includes(currentRoute);
    },
    logoUrl(){
        const store = useStore();
        return store.state.logoUrl;
    },
},
setup() {
    const store = useStore();
    const router = useRouter();
    const loggedInMessage = ref('');
    const isDropdownVisible = ref(false);
    const user = computed(() =>  store.state.user);
    const isAuthenticated = computed(() => store.state.isAuthenticated);
    const getCSRFToken = mapGetters(['getCSRFToken']);
    const csrfToken = mapState(['csrfToken']);

    /*
    vue 3 cant use event listeners in multi page app
    */
   //successful login
    const handleLoginSuccess = (message) => {
      console.log("app.vue handleLogin", message);

      loggedInMessage.value = message;
      store.commit('setLoggedInMessage', message); // Store the message in Vuex
      //router.push('/');
    };

    //when the session expires
    onBeforeUnmount(() => {
      store.commit('clearLoggedInMessage');
      //should clear user and all
      router.push('/'); // Redirect to '/' on session expiry
    });

    const handleLogout = (message) => {
      isDropdownVisible.value = false;
      loggedInMessage.value = message;
      store.commit('clearLoggedInMessage'); // Clear the message in Vuex on logout
      router.push('/');
    };
    const showDropdown = () => {
      isDropdownVisible.value = true;
    };

    const hideDropdown = () => {
      isDropdownVisible.value = false;
    };

    const goHomepage = async() =>{
      router.push('/');
    };

    return {
      loggedInMessage,
      handleLoginSuccess,
      handleLogout,
      isAuthenticated,
      showDropdown,
      hideDropdown,
      isDropdownVisible,
      user,
      getCSRFToken,
      csrfToken,
      goHomepage,
    };
  },
};
</script>

<template>
  <nav class="navbar" v-if="shouldShowNavBar">
    <img :src="logoUrl" class="logo-img" @click="goHomepage"/>

    <div class="navbar-links">
      <router-link to="/login" v-if="!isAuthenticated" @loginSuccess="handleLoginSuccess">Login</router-link>
      <router-link to="/signup"  v-if="!isAuthenticated">Signup</router-link>
      <router-link to="/" v-if="isAuthenticated">HOME</router-link>
      <router-link to="/add-item" v-if="isAuthenticated">Sell</router-link>
      <router-link to="/selling" v-if="isAuthenticated">My items</router-link>  
    </div>
    

    <div class="dropdown" v-if="isAuthenticated" @mouseover="showDropdown" @mouseleave="hideDropdown">
      <img v-if="user" :src="user.image" alt="User Profile" class="profile-pic" />
      <span v-if="user" class="dropdown-content">Hello, {{ user.email }}</span>
          

      <div v-if="isDropdownVisible" class="dropdown-content">
        <router-link to="/profile">Account Settings</router-link>
        <Logout @logoutSuccess="handleLogout"/>
      </div>
    </div>
  </nav>
  <router-view ></router-view>
</template>

<style>
/* Styles for the user profile picture */
.profile-pic {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  margin-left: 8px;
}
</style>