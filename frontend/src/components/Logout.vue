<template>
  <button @click="logout">Logout</button>
</template>

<script>
import axios from 'axios';
import { mapMutations, mapGetters, mapState } from 'vuex';
import Cookies from 'js-cookie';
import store from '../store';

/*logout button send post request to the logout/ endoint on the django */
export default {
  name: 'Logout',
  methods: {
    async logout(event) {
      event.preventDefault();
      console.log("Logout: ", store.getters.getIsAuthenticated);
      if(store.getters.getIsAuthenticated){
        const csrfToken = this.getCSRFToken();
        console.log("logout csrf", csrfToken);

        const sessionId = Cookies.get('sessionid');
        console.log("logout session", sessionId);

        try{
          const response = await axios({
            method: 'post',
            url: 'http://127.0.0.1:8000/logout/',
            headers: {
              //custom header
              'X-CSRFToken': csrfToken,
              'X-SessionID': sessionId,
              'Content-type': 'application/json',
          },
          //sends ccookie credentials
          withCredentials: true, 
        });

        console.log('Logout successful', response.data);
        this.clearUser();
        this.clearCSRFToken();
        store.commit('setAuthenticated', false);
        Cookies.remove('sessionid');
        Cookies.remove('csrftoken');
        
        this.$emit('logoutSuccess', 'Logout successful!');
        } catch (error) {
          // Handle the login error
          console.error('Logout failed. haha:',error.message);
        } 
      } else{
        console.log('User is not authenticated, cannot logout.');
      }
    },
    ...mapGetters(['isAuthenticated', 'getCSRFToken']),
    ...mapMutations(['clearCSRFToken', 'clearUser', 'setAuthenticated']),
    ...mapState(['csrfToken']),
  },
};
</script>