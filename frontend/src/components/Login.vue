<template>
    <div class="outer-container">
      <div class="form-card">
        <h2 class="headline">User Login</h2>
        <h5> Or alternatively, <router-link to="/signup">create an account</router-link></h5>

        <div v-if="loading" class="loading">
          <div class="progress-circular"></div>
        </div>
        
        <form @submit="login">
          <div class="form-container">
            <input class="text-field" type="email" v-model="email" placeholder="Email" required>
            <input class="text-field" type="password" v-model="password" placeholder="Password" required>
            <button type="submit" class="login-btn">Log In</button>
            <div v-if="errorMessage" class="error-message">
              {{ errorMessage }}
            </div>
          </div>
        </form>

    </div>
  </div>
</template>

<script>
  import axios from 'axios';
  import {ref} from 'vue';
  import { mapMutations, mapActions, useStore } from 'vuex';
  import { useRouter } from 'vue-router';
  import '../style.css';
  import Cookies from 'js-cookie';

  export default {
    name: 'Login',
    data(){
      return {
        email: '',
        password: '',
        loading: false,
        user: null,
        errorMessage: '',
      };
    },
    methods: {
    async login(event) {
      
        event.preventDefault();
        this.loading = true;

        if (!this.email || !this.password) {
        console.error('Email and password are required');
        return;
        }
        try{
          const response = await axios({
            method: 'post',
            url: 'http://127.0.0.1:8000/login/',
            data: {
              email: this.email,
              password: this.password,
            },
            withCredentials: true,
          });

          if (response.data.csrf_token){
            const csrfToken = response.data.csrf_token;
            const sessionId = response.data.session_id
            console.log('CSRF Token:', csrfToken);
            console.log("session id: ", sessionId);
            this.setCSRFToken(csrfToken);
            //this line sets isAuthenticated to true - login is a vuex action
            this.$store.dispatch('login');

            // Set CSRF token as a cookie and include it in the custom header
            Cookies.set('csrftoken', csrfToken, { httpOnly: true, sameSite: 'none', secure: true}); //  = cookie only sent over HTTPS, httpOnly is a security measure but it stops it from being accessed in frntend
            Cookies.set('sessionid', sessionId, { sameSite: 'none', secure: true}); //
            //Cookies.set('isAuthenticated', true, { httpOnly: true }); //, 
            //localStorage.setItem('isAuthenticated', 'true');

            // Handle the successful login response
           
            //
            const profileResponse = await axios({
              method: 'get',
                url: 'http://127.0.0.1:8000/profile/',
                headers: {
                //custom header
                'X-CSRFToken': csrfToken,
                'X-SessionID': sessionId,
                'Content-type': 'application/json',
            },
            //sends ccookie credentials
            withCredentials: true, 
            })
            const user = { ...profileResponse.data};
            //since this is from the server, not vuex, it'll return img url with only relative path
            if (user.image){
              user.image = 'http://127.0.0.1:8000' + user.image;
            }
            console.log(JSON.stringify(user));
            //the code above sets the logged in users profile information
            this.setUser(user);
            
            this.$router.push('/');
          } else{
            console.error('CSRF token not found in the response data');
          }

          //return response;
          console.log(response.data);
          this.$emit('loginSuccess', 'Login successful!');
          } catch (error) {   //  this is where the try{} ends
            console.error(error);
            //check server response
            if (error.response && error.response.data) {
              console.log("error");
              this.errorMessage = error.response.data.non_field_errors[0];
            }else{
              this.errorMessage = "An error occured.";
            }
          } finally {
            this.loading = false;
          }
      },
      ...mapMutations(['setCSRFToken', 'setUser']),
    },
  };
</script>