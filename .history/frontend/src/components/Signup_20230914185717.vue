<template>
  <div class="outer-container">
    <div class="form-card">
      <h2 class="headline">User Registration</h2>
      <h5>Already have an account? <router-link to="/login">Login</router-link></h5>


      <form @submit.prevent="signup">
        <input type="email"  class="text-field" v-model="this.email" placeholder="Email" required>
        <input type="password"  class="text-field" v-model="this.password" placeholder="Password" required>
        <input type="date" class="text-field" v-model="this.dob" placeholder="Date of Birth" required>
        <button type="submit" class="login-btn">Register</button>
        <div v-if="this.errorMessage" class="error-message">
          {{ this.errorMessage }}
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import '../style.css';
import { ref} from 'vue';
import { useStore } from 'vuex';

export default {
  data() {
    return {
      commonPasswords: ['password', 'password123', 'qwerty'],
      email: '',
      password: '',
      dob: '',
      errorMessage: '',
    };
  },
  methods: {
    validatePassword() {
      if (this.password.length < 8) {
        this.errorMessage = 'Password must be at least 8 characters long.';
        return false;
      }
      else if (/^\d+$/.test(this.password)) {
        this.errorMessage = 'Password cannot be entirely numeric.';
        return false;
      }
      else if (this.commonPasswords.includes(this.password.toLowerCase())) {
        this.errorMessage = 'Password is too common and easily guessable.';
        return false;
      }

      this.errorMessage = '';
      return true;
    },

    async signup(event) {
      event.preventDefault();

      while (!this.validatePassword()) {
        console.log('invalid credentials');
        return;
      }

      try {
        const response = await axios({
          method: 'post',
          url: 'http://127.0.0.1:8000/signup/',
          data: {
            email: this.email,
            password: this.password,
            dob: this.dob,
          },
          withCredentials: true,
        });
        console.log('signed up');
        this.$emit('signupSuccess', 'signup successful!');
        this.$router.push('/login');
      } catch (error) {
        console.error('Signup failed:', error);
        //check server response
        if (error.response && error.response.data && error.response.data.email) {
          this.errorMessage =
            'This email is already in use. Please choose a different one.';
        } else {
          // Handle other error cases, e.g., server unavailable - email invalid
          //this.errorMessage = 'Signup failed. Please try again later.';
          if(error.response.data){
            //this is JSON
            this.errorMessage = error.response.data.message
          }else{
            this.errorMessage = "Signup failed."
          }
          
        }
      }
    },
  },
};
</script>