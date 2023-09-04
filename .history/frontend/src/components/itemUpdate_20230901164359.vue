<!--lets specific users update the item they click on, using the itemID-->
<template>
    <div class="outer-container">
        <div class="form-card">
            <h2 class="headline">Listing details</h2>
            <form @submit.prevent="updateItem">
                <input type="text" class="text-field" v-model="updatedData.title" placeholder="Title" required>
                <textarea class="text-field" v-model="updatedData.description" placeholder="Description"/>
                <input type="number" step=".01" class="text-field" v-model="updatedData.starting_price" placeholder="price" required>
                
                <img class="page-img" :src="itemUrl" alt="itemImage" v-if="updatedData.picture"/>
                <input type="file" @change="onFileChange">

                <input type="datetime-local" class="text-field" v-model="updatedData.end_time" placeholder="End of auction date" required>
                <div>
                    <label>Category:</label>
                    <select v-model="updatedData.category" required>
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

                <button type="submit" class="login-btn">Update</button>
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
import { useRoute, useRouter } from 'vue-router';
import { mapMutations, mapGetters} from 'vuex';
import Cookies from 'js-cookie';
import { computed, defineComponent, onMounted, onUnmounted, onUpdated, ref , watch,} from 'vue';

//the reason my image isn't uploading is because in profile vue
//i use the user vuex store to get the new imageURL
//here i have nothing saved in vuex - HOW should i get new item image
export default {
    setup(){
        const store = useStore();
        const router = useRouter();
        const  route = useRoute();

        const {isAuthenticated, getCSRFToken, getItemId} = mapGetters(['getIsAuthenticated', 'getCSRFToken', 'getItemId']);
        const {clearCSRFToken, updateUser, clearItem} = mapMutations(['clearCSRFToken', 'clearUser', 'setUser', 'updateUser', 'clearItem']);

        const itemUrl = ref(''); //stores the img with base URL
        const errorMessage = ref('');

        const user = computed(() => store.state.user);
        const csrfToken = computed(() =>  store.state.csrfToken);
        const sessionId = Cookies.get('sessionid');
        //const itemId = computed(() => store.state.itemId);
        //these 2 are for getting current and update info
        const currentItem = ref({});
        const updatedData = ref({});

        onMounted(()=>{
            getCurrentItem();
        });
        onUnmounted(() => {
            stopWatch();
        });

        const getImageUrl = async(event)=>{
            //console.log("get image returns", itemUrl.value);
            //console.log("updated pic", updatedData.value.picture);
            console.log("getImageUrkl");
            itemUrl.value = "http://127.0.0.1:8000" + updatedData.value.picture;
        };
        const imageUrlComputed = computed(()=>{
            console.log("computed image", itemUrl.value);
            return itemUrl.value;
        });
        const stopWatch = watch(() => updatedData.value?.picture, (newImage) => {
            if(newImage){
                //since onFileChange changes value of updatedData pic, => now a file
                //instead of a url to display -- since its not waiting for the upload
                console.log("updated user image has changed", updatedData.value.picture)
                console.log("the value is now", newImage.name);
                if (newImage instanceof File){
                    currentItem.value.picture = `http://127.0.0.1:8000/media/item_pictures/${newImage.name}`;
                    itemUrl.value = currentItem.value.picture;
                }
                else if(typeof image === "string"){
                    itemUrl.value = newImage;
                }
            }
            else{
                console.log("stopping the watchh --")
                stopWatch();
            }
        });

        const getCurrentItem = async() => {
            /*when it gets the iitem from server it might be in file form rather than url*/
            try{

                const response = await axios({
                    method: 'get',
                    url: `http://127.0.0.1:8000/items/${route.params.itemId}/`, //doesnt need auth
                })
                currentItem.value = {...response.data}
                updatedData.value = {...response.data}
                console.log("currentItem", JSON.stringify(currentItem.value));
                console.log("GETITEM: updated data picture value ", updatedData.value.picture);
                
                const tempDate = new Date(updatedData.value.end_time);
                updatedData.value.end_time = tempDate.toISOString().slice(0,16);
                currentItem.value.end_time = updatedData.value.end_time

                if(updatedData.value.picture){
                    itemUrl.value = currentItem.value.picture;
                    console.log('itemUrl in setup now = :', itemUrl.value);
                }
                console.log("successfully GOT");
            }catch(error){
                console.log("getcurrentItem error", error);
            }
        };

        const onFileChange=(event)=>{
            const file = event.target.files[0];
            const newItemUrl = `http://127.0.0.1:8000/media/${file.name}`;
            console.log("file name is:", file.name);

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
            //SO ON FILE CHANGE, UPDATED PIC IS A FILE TYPE - TO RENDER IT, IT NEEDS TO BE URL
            updatedData.value.picture = file;
            console.log("updatedData pic is now => value: ", updatedData.value.picture);
        };

        const updateItem = async(event) => {
            event.preventDefault();
            console.log("test: title is: ", updatedData.value.title);
            console.log("picture is ", updatedData.value.picture);

            try {
                //does it need the creator id in the request? 
                const changedFields = {'creator': user.value.id};
                //oh wait, the first time the page is loaded, its loaded from GET
                //yeah so .. .still the same 
                for (const key in updatedData.value) {
                    if (updatedData.value[key] !== currentItem.value[key]) {
                        changedFields[key] = updatedData.value[key];
                    }
                }

                const formData = new FormData();
                for (const key in changedFields) {
                    formData.append(key, changedFields[key]);
                }

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

                //items => the viewset without authentication 
                //send form data to http://127.0.0.1:8000/item/add-item/
                const response = await axios({
                        method: 'put',
                        url: `http://127.0.0.1:8000/item/update/${route.params.itemId}/`,
                        data: formData,
                        headers: {
                            'X-CSRFToken': csrfToken,
                            'X-SessionID': sessionId,
                            'Content-type': 'multipart/form-data',
                        },
                        withCredentials: true,
                    })

                    errorMessage.value = '';
                    console.log("SUCCESSFULLY updated ITEM", response);
                    console.log("uppdatedData is ", JSON.stringify(updatedData.value))
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
            getItemId,
            clearCSRFToken,
            updateUser,
            csrfToken,
            clearItem,
            errorMessage,
            itemUrl: imageUrlComputed,
            user,
            csrfToken,
            sessionId,
            currentItem,
            updatedData,
            getImageUrl,
            getCurrentItem,
            stopWatch,
            onFileChange,
            updateItem,

        }
    }
};
</script>