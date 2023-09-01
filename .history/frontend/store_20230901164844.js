//this is for vuex - storing state
import { createStore } from 'vuex';

export default createStore({
  state() {
    return {
      loggedInMessage: '',
      isAuthenticated: false,
      csrfToken: null,
      user: null,
      logoUrl: 'src/assets/daruma1.png',
      itemId: null,
    };
  },
  mutations: {
    setLoggedInMessage(state, message) {
      state.loggedInMessage = message;
      state.isAuthenticated = true;
    },
    clearLoggedInMessage(state) {
      state.loggedInMessage = '';
      state.isAuthenticated = false;
    },
    setCSRFToken(state, csrfToken) {
      state.csrfToken = csrfToken;
    },
    clearCSRFToken(state) {
      state.csrfToken = null; // Set the CSRF token to null or whatever default value you want
    },
    setAuthenticated(state, value) {
      state.isAuthenticated = value;
      console.log("authenticated now set to ", state.isAuthenticated);
      /*saving it to local store so that it can persist even through full page refreshes
      right now, naviagting to profile isn't possible because state is wiped so it sees authenticated = false*/
    },
    setUser(state, user){
      state.user = user;
    },
    updateUser(state, updatedUser){
      //updatedUser is the full complete user obj - before i sent updatedData but now im sending formData
      if(updatedUser.image){
        const image = updatedUser.image;

        console.log("inside of vuex update, image is", image, "or the name is:", image.name);
        if (image instanceof File){
          updatedUser.image = `http://127.0.0.1:8000/media/${updatedUser.image.name}`;
          console.log("new image is a file ,s createObjectURL =", updatedUser.image);
          }else if (typeof image === 'String'){
            console.log("new image is not a file");
          }
      }
      
      state.user = {...state.user, ...updatedUser};
      console.log("updating user in vuex", JSON.stringify(state.user));
      
      /*
      if (updatedUser.image instanceof File){
        console.log("updated image in vuex", updatedUser.image.name);
        updatedUser.image = `http://127.0.0.1:8000/media/${updatedUser.image.name}`;
        //updatedUser.image = updatedUser.image.name;
      }//
      console.log("updated user in vuex", updatedUser);
      state.user = updatedUser;*/
    },
    clearUser(state) {
      state.isAuthenticated = false;
      state.user = null;
    },
    setItem(state, id){
      state.itemId = id;
    },
    clearItem(state){
      state.itemId = null;
    },
  },
  getters: {
    getCSRFToken(state) {
      return state.csrfToken;
    },
    getIsAuthenticated(state){
      //instead of getting it from state.isAuthenticated, it can be changed to retrieve from document cookie
      console.log("get authenticated", state.isAuthenticated);
      return state.isAuthenticated;
    },
    getItemId(state){
      console.log("get current item", state.itemId);
      return state.itemId;
    }
  },
  actions: {
    setCSRFTokenAction({commit}, csrfToken) {
      commit('setCSRFToken', csrfToken)
    },
    login({ commit }) {
      commit('setAuthenticated', true);
    },
    // This action can be used to set the isAuthenticated state to false when the user logs out
    logout({ commit }) {
      // Perform your logout logic here
      // For example, after successful logout:
      commit('setAuthenticated', false);
    },
    updateUser({commit}, updatedUser){
      commit('updateUser', updatedUser);
    },
  },
  modules: {},
});