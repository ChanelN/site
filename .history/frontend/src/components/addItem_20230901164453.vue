<template>
    <div class="outer-container">
        <div class="form-card">
            <h2 class="headline">Create item</h2>
        
        <form @submit.prevent="addItem">
        <input type="text"  class="text-field" v-model="title" placeholder="Title" required>
        <textarea class="text-field" v-model="description" placeholder="Description"/>
        <input type="number" step=".01" class="text-field" v-model="starting_price" placeholder="price" required>
        <img :src="picture" alt="itemImage" v-if="picture"/>
        <input type="file" @change="onFileChange">
        <input type="datetime-local" class="text-field" v-model="end_time" placeholder="End of auction date" required>
        <div>
        <label>Category:</label>
        <select v-model="category" required>
            <option value="LAP">Laptop</option>
            <option value="CON">Console</option>
            <option value="GAD">Gadget</option>
            <option value="GAM">Game</option>
            <option value="TEL">Tv</option>
            <option value="JWL">Jewelry</option>
            <option value="ART">Art and collectibles</option>
            <option value="COL">collectibles and memorabilia</option>
            <option value="FAS">Fashion and accessories</option>
            <option value="BKS">Books</option>
            <option value="HOM">Home or Garden</option>
            <option value="TOY">Toy and hobbies</option>
        </select>
        </div>

        <button type="submit" class="login-btn">Finish</button>
        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>
        </form>
        </div>
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
    //the creator field needs to be automatically set to the current user id - get from vuex?
    setup(){
        const store = useStore();
        const router = useRouter();
        const {isAuthenticated, getCSRFToken} = mapGetters(['getIsAuthenticated', 'getCSRFToken']);
        const {clearCSRFToken, clearUser, setUser, updateUser} = mapMutations(['clearCSRFToken', 'clearUser', 'setUser', 'updateUser']);

        const title = ref('');
        const description = ref('');
        const starting_price = ref('');
        const picture = ref(null);
        const end_time = ref('');
        const category = ref('');

        const itemUrl = ref('');
        const errorMessage = ref('');
        const user = computed(() => store.state.user);
        const csrfToken = computed(() =>  store.state.csrfToken);
        const sessionId = Cookies.get('sessionid');

        const onFileChange=(event)=>{
            const file = event.target.files[0];
            const newItemUrl = 'http://127.0.0.1:8000/media/${file.name}';
            console.log("onFileChange ", newItemUrl, "file name is:", file.name);
            console.log("user email", user.value.email);

            axios
                .get(newItemUrl)
                .then(() => {
                    //url on bckend
                    itemUrl.value = newItemUrl;
                })
                .catch(() => {
                console.log('image not on backend yet');
                });
            console.log("onFileChange, file:", file);
            picture.value = file;
        };

        const addItem = async(event) => {
            console.log("csrf in AddItem", csrfToken);
            console.log("sessionID in AddItem", sessionId);

            console.log("test: title is: ", title.value);
            console.log("starting pirce", starting_price.value);
            console.log("picture is ", picture.value);

            const formData = new FormData();
            formData.append('title', title.value);
            if(description.value!==''){formData.append('description', description.value);}
            formData.append('starting_price', starting_price.value);
            if(picture.value!== null){formData.append('picture', picture.value);}
            formData.append('end_time', end_time.value);
            formData.append('category', category.value);
            formData.append('creator', user.value.id);

            //printing out the form
            function formDataToObject(formData) {
            const object = {};

            for (const [key, value] of formData.entries()) {
                object[key] = value;
            }

            return object;
            }
            const formDataObject = formDataToObject(formData);
            console.log("new formdata is",JSON.stringify(formDataObject, null, 2));
            try{
                //items => the viewset without authentication 
                //send form data to http://127.0.0.1:8000/item/add-item/
                const response = await axios({
                    method: 'post',
                    url: "http://127.0.0.1:8000/item/add-item/",
                    data: formData,
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'X-SessionID': sessionId,
                        'Content-type': 'multipart/form-data',
                    },
                    withCredentials: true,
                })

                errorMessage.value = '';
                console.log("SUCCESSFULLY ADDED ITEM", response.data);
                //possible to add loading img before pushing
                store.commit('setItem', response.data.item_id); //set in vuex
                router.push('/item');
            } catch(error){
                console.log("add item error", error);
                if (error.response && error.response.data) {
                    console.log(error.response.data);
                    errorMessage.value = error.response.data;
                } 
            }
        };

        return{
            isAuthenticated,
            getCSRFToken,
            clearCSRFToken,
            updateUser,
            csrfToken,
            title,
            description,
            starting_price,
            picture,
            end_time,
            category,
            errorMessage,
            itemUrl,
            user,
            sessionId,
            onFileChange,
            addItem,
        }
    }
}
</script>