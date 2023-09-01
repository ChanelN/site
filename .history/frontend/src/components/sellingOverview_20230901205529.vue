<!--page that only logged in users can access, look at active and sold item, update or delete them
Item id is set in vuex in this template @click-
I need the template to reload or call getUserItems again once delete or update called-->
<template>
    <div class="outer-container">
        <Searchbar :items="items" @inputChanged="handleSearch"/>
        <h2 class="page-title">My Page - Active items:</h2>

        <div class="item-list">
            <!--so when you click on item, it saves itemID in vuex, should change to just pass it as prop-->
            
            <div class="dropdown" @mouseover="showDropdown" @mouseleave="hideDropdown">
                <span> All </span>
                <div v-if="isDropdownVisible" class="dropdown-content" @click.stop> <!--click.stop stops it going to itemPage-->
                        <!--and clicking on sold should alter item list so that it only shows items already sold/expired
                        i need to make new axios request to items/-->
                        <p v-on:click="getAllActive"> all</p>
                        <p v-on:click="getExpiredItems"> expired </p>
                        <p v-on:click="getSoldItems"> Sold </p>
                    </div>
            </div>

            <div class="error-message" v-if="itemList == -1 || dropdownList == -1">
                <p>No results found!</p>
            </div>
            <!--so if they click on all, it should show itemList instead
            dropdown list = -1 means the lists are empty, but dropdownList = 0 means it needs to show itemlist-->
            <div v-if="dropdownList != -1 && dropdownList!=0" v-for="item in dropdownList" :key="item.id" class="user-item" @click="goToItemPage(item.id)">
                <p>drop</p>
                <img :src="item.picture" alt="picture" class="item-card-img" >
                <div class="item-listing">
                    <h2 class="item-title">{{ item.title }}</h2>
                    <p class="item-price">£{{ item.starting_price }}</p>
                    <p class="item-p">{{ item.description }}</p>
                    <p class="item-p">{{ item.end_time }}</p>
                </div>
                <!-- my dropdown option for each item-->
                <div class="dropdown"  @mouseover="showDropdown" @mouseleave="hideDropdown">
                    <span> Options </span>
                    <p class="item-p">{{ item.id }}</p>
                    <div v-if="isDropdownVisible" class="dropdown-content" @click.stop> <!--click.stop stops it going to itemPage-->
                        <router-link :to="{ name: 'item-update', params: { itemId:item.id }}">Update listing</router-link>
                        <!--needs to be a  router view because otherwise hoevering over will try show the whole form, use router params-->
                        <!--<itemUpdate :itemId="item.id" @updateSuccess="handleUpdate"/>-->
                        <!--:itemId is a prop, passed onto deleteItem-->
                        <deleteItem :itemId="item.id" @deleteSuccess="handleDelete"/>
                    </div>
                </div>
            </div>


            <!-- itemList == -1 when the user has searched for an item but there is no match-->
            <div v-if="itemList != -1 || dropdownList == 0" v-for="item in itemList" :key="item.id" class="user-item" @click="goToItemPage(item.id)">
                <img :src="item.picture" alt="picture" class="item-card-img" >
                <div class="item-listing">
                    <h2 class="item-title">{{ item.title }}</h2>
                    <p class="item-price">£{{ item.starting_price }}</p>
                    <p class="item-p">{{ item.description }}</p>
                    <p class="item-p">{{ item.end_time }}</p>
                </div>
                <!-- my dropdown option for each item-->
                <div class="dropdown"  @mouseover="showDropdown" @mouseleave="hideDropdown">
                    <span> Options </span>
                    <p class="item-p">{{ item.id }}</p>
                    <div v-if="isDropdownVisible" class="dropdown-content" @click.stop> <!--click.stop stops it going to itemPage-->
                        <router-link :to="{ name: 'item-update', params: { itemId:item.id }}">Update listing</router-link>
                        <!--needs to be a  router view because otherwise hoevering over will try show the whole form, use router params-->
                        <!--<itemUpdate :itemId="item.id" @updateSuccess="handleUpdate"/>-->
                        <!--:itemId is a prop, passed onto deleteItem-->
                        <deleteItem :itemId="item.id" @deleteSuccess="handleDelete"/>
                    </div>
                </div>
            </div>
        </div>

    </div>
</template>

<script>
import axios from 'axios';
import { useStore } from 'vuex';
import { mapMutations, mapGetters, mapState } from 'vuex';
import Cookies from 'js-cookie';
import { computed, onMounted, onUnmounted, ref , watch, defineComponent, VueElement} from 'vue';
import { useRouter } from 'vue-router';
import deleteItem from './deleteItem.vue';
import itemUpdate from './itemupdate.vue';
import Searchbar from '../components/Searchbar.vue';

export default defineComponent({
    components:{
        deleteItem,
        Searchbar,
    },
    setup(props, context){
        const store = useStore();
        const router = useRouter();
        const {isAuthenticated, getCSRFToken} = mapGetters(['getIsAuthenticated', 'getCSRFToken']);
        const {updateUser, setItem} = mapMutations(['updateUser', 'setItem']);
        const csrfToken = computed(() => store.state.csrfToken);
        const sessionId = Cookies.get('sessionid');
        const user = computed(() => store.state.user);

        const items = ref([]) //list of items only owned by this person
        const isDropdownVisible = ref(false);
        const filtered = ref([]);

        const itemsCopy = ([]);
        const expiredItems = ref([]);
        const soldItems = ref([]);
        const dropdownClicked = ref(false);

        onMounted(()=>{
            getUserItems();
        });

        const getUserItems = async() =>{
            try{
                const response = await axios({
                    method: 'get',
                    url: "http://127.0.0.1:8000/item/auctionItems/",
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'X-SessionID': sessionId,
                        'Content-type': 'application/JSON',
                    },
                    withCredentials: true,
                })
                const currentItems = [ ...response.data]

                for(const item of currentItems){
                    const picture_path = item.picture;
                    console.log("path" , picture_path);
                    const fullPictureUrl = `http://127.0.0.1:8000${picture_path}`;
                    item.picture = fullPictureUrl;
                };
                console.log("currentItems", JSON.stringify(currentItems))
                items.value = currentItems
                
                console.log("retrieved user items", JSON.stringify(items.value));
            }catch(error){
                console.log("error");
            }
        };

        const goToItemPage = async(itemId) => {
            //have to get specific itemId
            console.log("iitemid", itemId);
            store.commit('setItem', itemId); //set in vuex
            router.push('/item');
        };

        const showDropdown = () => {
        isDropdownVisible.value = true;
        };

        const hideDropdown = () => {
        isDropdownVisible.value = false;
        };
        
        const handleDelete = (deletedItemId) => {
            items.value = items.value.filter(item => item.id !== deletedItemId);
        };

        const handleSearch = async(filteredValue) => {
            console.log("context vallue is", filteredValue);
            filtered.value = filteredValue;
        };

        const itemList = computed(() => {
            //if there are items
            if(!filtered.value.length == 0){
                return filtered.value;
            }
            //if theres no input - should show the entire list again
            else if(filtered.value != -1 && filtered.value.length == 0){
                return items.value;
            }
            //if theres input but no matching result
            else if(filtered.value == -1 ){
                return -1;
            }
        });

        const dropdownList = computed(() => {
            // if there are items in the GET request
            if( dropdownClicked.value){
                if(expiredItems.value.length != 0){
                    return expiredItems.value;
                }
                if(soldItems.value.length != 0){
                    return soldItems.value;
                }
                if(itemsCopy.values.length != 0){
                    return 0;
                }
                //but at the beginning when you first don't chose anything, then of course these will be empty
                else if (expiredItems.value.length == 0 || soldItems.value.length == 0){
                    return -1
                }
            }
            else{
                return;
            }
            console.log("dropdown is currenttly", dropdownList.value);
        });

        const getAllActive = async() => {
            dropdownClicked.value = true;
            itemsCopy.value = [...items.value];
        };

        const getExpiredItems = async() => {
            dropdownClicked.value = true;
            const response = await axios({
                method: 'get',
                    url: "http://127.0.0.1:8000/item/expiredItems/",
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'X-SessionID': sessionId,
                        'Content-type': 'application/JSON',
                    },
                    withCredentials: true,
            })
            expiredItems.value = [...response.data]
            for(const item of expiredItems.value){
                console.log("item", item);
                const picture_path = item.picture;
                console.log("path" , picture_path);
                const fullPictureUrl = `http://127.0.0.1:8000${picture_path}`;
                item.picture = fullPictureUrl;
            };
        };

        const getSoldItems = async() => {
            dropdownClicked.value = true;
            const response = await axios({
                method: 'get',
                    url: "http://127.0.0.1:8000/item/soldItems/",
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'X-SessionID': sessionId,
                        'Content-type': 'application/JSON',
                    },
                    withCredentials: true,
            })
            soldItems.value = [...response.data]
            for(const item of soldItems.value){
                console.log("item", item);
                const picture_path = item.picture;
                console.log("path" , picture_path);
                const fullPictureUrl = `http://127.0.0.1:8000${picture_path}`;
                item.picture = fullPictureUrl;
            };
        };
        /* if my update is directly used
        const handleUpdate = (updatedItem) => {
            const index = items.value.findIndex(item => item.id === updatedItem.id);
      
            if (index !== -1) {
                // Update the item in the items list with the updated data
                //dont use this.$set inside of setup
                //this.$set(items.value, index, updatedItem);
                items.value[index] = updatedItem;
            }
        };
        */
        return{
            store,
            router,
            isAuthenticated,
            getCSRFToken,
            updateUser,
            csrfToken,
            sessionId,
            user,
            items,
            goToItemPage,
            isDropdownVisible,
            showDropdown,
            hideDropdown,
            handleDelete,
            handleSearch,
            itemList,
            getExpiredItems,
            getSoldItems,
            soldItems,
            expiredItems,
            dropdownList,
            getAllActive,
        }
    }
});
</script>