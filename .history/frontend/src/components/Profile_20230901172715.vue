<!--okay so the issue was that the profile pic needs to be uploaded as a FILE type to the server, but on frontend i need it in URL form
so now, this.imageUrl is what holds the full url(because in vuex when the user is updated i saved it as full URL too),
 while this.updatedData.image holds the FILE-->
<template>
    <div v-if="profile">
        <h2>MY PROFILE</h2>
        <form @submit="updateProfile">
            <div>
                <!--the profile pic uses data imageURL so its seperate frm the other data-->
                <!--change to this.imageUrl later-->
                <div>
                    <img :src="imageUrl" alt="Profile Picture" v-if="updatedData.image" class="profile-picture"/>
                </div>
                <input type="file" @change="onFileChange">
            </div>
            <div>
                <label>Email:</label>
                <input type="email"  v-model="updatedData.email" required>
            </div>
            <div>
                <label>Password: </label>
                <input type="password" v-model="updatedData.password" required>
            </div>
            <div>
                <p class="error-message"> {{ errorMessage }}</p>
                <label>Current Password:</label>
                <input type="password" v-model="currentPassword">
            </div>
            <div>
                <label>New Password:</label>
                <input type="password" v-model="newPassword">
            </div>
            <div>
                <label>Confirm New Password:</label>
                <input type="password" v-model="confirmPassword" >
            </div>
            <div>
                <label>Date of Birth:</label>
                <input type="date" v-model="updatedData.dob" required>
            </div>
            <div>
                <label>Bio:</label>
                <textarea v-model="updatedData.bio" maxlength="250"></textarea>
            </div>
            <button type="submit" >Update Profile</button>
        </form>
    </div>
</template>

<script>
import axios from 'axios';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
import { mapMutations, mapGetters, mapState } from 'vuex';
import Cookies from 'js-cookie';
import { computed, onMounted, onUnmounted, ref , watch,} from 'vue';

export default{
          /*
    data() {
    return {
      profile: {},
      updatedData:{}, //dynamic object to hold new values - sent in patch

      currentPassword: '',
      newPassword: '',
      confirmPassword: '',
      errorMessage:'',
      
    };
  },*/
  setup(){
    const store = useStore();
    const {isAuthenticated, getCSRFToken} = mapGetters(['getIsAuthenticated', 'getCSRFToken']);
    const {clearCSRFToken, clearUser, setUser, updateUser} = mapMutations(['clearCSRFToken', 'clearUser', 'setUser', 'updateUser']);

    //previously inside of data(){return{}}
    const profile = ref({});
    const updatedData = ref({}); // dynamic object to hold new values - sent in patch
    const updating = ref(false); // supposed to stop the user from editing while changes made but I haven't used it yet
    const currentPassword = ref('');
    const newPassword = ref('');
    const confirmPassword = ref('');
    const errorMessage = ref('');
    const user = computed(() =>  store.state.user);
    const imageUrl = ref('');
    const csrfToken = computed(() =>  store.state.csrfToken);

    const getImageUrl = async(event) =>{
        imageUrl.value = "http://127.0.0.1:8000" + user.value.image;    //vuex store the image as a URL
    };
    //define image as computed to be reactive
    const imageUrlComputed = computed(() => {
        console.log("computed image", imageUrl.value);
        //if user isn't changing image , it needs url added to beginning. If its being uploaded, the update vuex method alreadyy turns it iinti
        return imageUrl.value;
    });
    //this watches if the vuex user image value changes at any point to update this.imageUrl too - in template it will update   
    const stopWatch = watch(() => user.value?.image, (newImage)=>{
        //user.value && user.value.image
        if(newImage){
            console.log("user obj is", user.value.image);
            console.log('image has changed in vuex:', newImage);
            //THIS IS WHAT IS RETRIEVED FROM USER PROFILE
            imageUrl.value =  newImage;//'http://127.0.0.1:8000' +
        }
        else{
            console.log("stopping the watchh --")
            stopWatch();
        }
    });
    onMounted(() => {
        getUserProfile();
    });
    onUnmounted(() => {
        console.log("profile being unmounted");
        stopWatch();
    });

    const getUserProfile = async() =>{
        //const getCsrfToken = getCSRFToken();
        //const getCsrfToken = store.state.csrfToken;
        console.log("csrftoekn", csrfToken);

        const sessionId = Cookies.get('sessionid');
        console.log('getUser session', sessionId);
        try {
            const response = await axios({
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
            });

            profile.value = { ...response.data };
            console.log('profile data', JSON.stringify(profile.value));
            updatedData.value = { ...profile.value };

            console.log(JSON.stringify(updatedData.value));
            // Update the imageUrl with the image URL retrieved from the profile data
            console.log("M GETTING THE USER - DO I HAVE IMAGE? ", updatedData.value.image)
            if (profile.value.image) {
                imageUrl.value = 'http://127.0.0.1:8000' + profile.value.image;
                console.log('getUser updates imageUrl to:', imageUrl.value);
            }
        } catch (error) {
            console.log('getUserProfile error:', error);
        }
    };
    const onFileChange=(event)=>{
        const file = event.target.files[0];

        const newImageUrl = `http://127.0.0.1:8000/media/${file.name}`;
        console.log("onFileChange ", newImageUrl, "file name is:", file.name);

        axios
            .get(newImageUrl)
            .then(() => {
            imageUrl.value = newImageUrl;
            })
            .catch(() => {
            console.log('image not on backend yet');
            });
        console.log("onFileChange, file:", file);
        updatedData.value.image = file;
    };

    const updateProfile = async (event) => {
        console.log("updating profile");
        event.preventDefault();

        try {
            const changedFields = {};
            for (const key in updatedData.value) {
                if (updatedData.value[key] !== profile.value[key]) {
                changedFields[key] = updatedData.value[key];
                }
            }

            if (currentPassword.value && newPassword.value) {
                if (newPassword.value !== confirmPassword.value) {
                    errorMessage.value = 'New password and confirmation password do not match.';
                    return;
                } else {
                    changedFields.currentPassword = currentPassword.value;
                    changedFields.newPassword = newPassword.value;
                }
            }

            const formData = new FormData();
            for (const key in changedFields) {
                formData.append(key, changedFields[key]);
            }

            //const csrfToken = getCSRFToken();
            console.log('update csrf', csrfToken);
            const sessionId = Cookies.get('sessionid');
            console.log('update sess', sessionId);

            const id = profile.value.id;
            console.log('user id', id);

            //if using string interpolation, you need backticks not normal ""
            const url = `http://127.0.0.1:8000/profile/${id}/`;
            const response = await axios({
                method: 'put',
                url: url,
                data: formData,
                headers: {
                'X-CSRFToken': csrfToken,
                'X-SessionID': sessionId,
                'Content-type': 'multipart/form-data',
                },
                withCredentials: true,
            });

            errorMessage.value = ''; // cleared because it's successful
            console.log("UpdateUser Successful, Image is", updatedData.value.image);
            console.log("formData is", JSON.stringify(formData), "changedFields is", changedFields);
            
            //updating user vuex
            store.commit('updateUser', changedFields); // Update with only the changed fields
            //emit('updateSuccess', 'update successful!');
        } catch (error) {
            if (error.response && error.response.data) {
                errorMessage.value = error.response.data.error;
                console.log(errorMessage);
                console.log(error);
                updating.value = false;
            } else {
                errorMessage.value = 'An error occurred. Please try again later.';
                console.log(error);
            }
        }
  };


    return{
        isAuthenticated,
        getCSRFToken,
        clearCSRFToken,
        clearUser,
        setUser,
        updateUser,
        csrfToken,
        profile,
        updatedData,
        imageUrl: imageUrlComputed,
        updating,
        currentPassword,
        newPassword,
        confirmPassword,
        errorMessage,
        getImageUrl,
        getUserProfile,
        onFileChange,
        updateProfile,
        stopWatch,
    }
  },
  /*
  mounted(){
    this.getUserProfile();
    //this.getImageUrl(); //gets the right image
  },
  */
};  //end of export
</script>

<style>
    .error-message{
        color: red;
    }
    .profile-picture{
        width: 200px;
        height: auto;
        border-radius: 60%;
    }
</style>