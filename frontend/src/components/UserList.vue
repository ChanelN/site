//lets make this my users list thing
/*
sessions use cookies stored on client- store session cookie
on client and send on ever request to API to be authent
*/
<script>
import axios from 'axios';
export default {
  data() {
    return {
      users: [],
      email: "",
      password: "",
      dob: "",
      pic: "",
    };
  },
  created(){
    this.getUsers();
  },
  methods: {
    async getUsers() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/users/');
        this.users = response.data;
          
      } catch(error){
        console.log(error);
      }
    },
  },
};
</script>

<template>
  <div class="hello">
    <h1 class="title">Users</h1> 
    <div class="list">
      <ul class="list_content">
        <!--<pre>{{ users }}</pre>-->
        <li v-for="user in users" :key="user.email">
          <h4>{{ user.email }}</h4>
          <h4>{{ user.password }}</h4>
          <h4>{{ user.dob }}</h4>
        </li>
      </ul>
    </div>
  </div>
</template>