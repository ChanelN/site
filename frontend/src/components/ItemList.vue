<!-- code for the homescreen to browse and see all current items available to bid on-->
<template>
    <div class="outer-container">
        <Searchbar :items="items" @inputChanged="handleSearch"/>

        <h2 class="page-title"> Home </h2> 
        <!--2 diff item-lists. 1 for filtering input, 1 for regular showing
            when you click back on home in nav, i want it to clear the searchbar
            tthe reason why i cant just use item instead of filtered, 
            if i clear the filtered list, theres no default items page
        <div class = "item-list" v-if="!filtered.length == 0">
            <div v-for="item in filtered" :key="item.id" class="item-card" @click="goToItemPage(item.id)">
                <img class="item-card-img" :src="item.picture" alt="picture" >
                <h2>{{ item.title }}</h2>
                <p>£{{ item.starting_price }}</p>
            </div>
        </div>-->
        <!-- value of -1 means that the filtered list is empty because theres no matching results-->
        <div class="item-list">
            <div class="error-message" v-if="filtered == -1">
                <p>No results found!</p>
            </div>

            <div v-if="itemList != -1" v-for="item in itemList" :key="item.id" class="item-card" @click="goToItemPage(item.id)">
                <img class="item-card-img" :src="item.picture" alt="picture" >
                <h2>{{ item.title }}</h2>
                <p>£{{ item.starting_price }}</p>
            </div>
        </div>
        
    </div>
</template>
<!--
jnj
-->
<script>
import axios from 'axios';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
import { mapGetters } from 'vuex';
import Cookies from 'js-cookie';
import { computed, onMounted, onUnmounted, ref , watch,} from 'vue';
import Searchbar from '../components/Searchbar.vue';

export default {
    setup() {
        const store = useStore();
        const router = useRouter();
        const { isAuthenticated } = mapGetters(['getIsAuthenticated']);
        const csrfToken = computed(() => store.state.csrfToken);
        const sessionId = Cookies.get('sessionid');
        const items = ref([]);
        const topBid = ref(null);
        //const input = ref("");
        const filtered = ref([]);

        const itemList = computed(() => {
            if(!filtered.value.length == 0){
                return filtered.value;
            }
            else if(filtered.value != -1 && filtered.value.length == 0){
                return items.value;
            }
            else if(filtered.value == -1){
                return -1;
            }
        });

        onMounted(() => {
            getItems();
        });
        onUnmounted(() => {
            console.log("item list unmounted");
        });
        const getItems = async () => {
            try {
                //const response = await axios.get('http://127.0.0.1:8000/items/');
                const response = await axios.get('http://127.0.0.1:8000/item/activeItems/');
                // the items don't have the beginning url - but this code is copied from sellingOverview
                items.value = [...response.data];
                for(const item of items.value){
                    const picture_path = item.picture;
                    const fullPictureUrl = `http://127.0.0.1:8000${picture_path}`;
                    item.picture = fullPictureUrl;
                };
                /*
                search the diff between using
                items.value = { ...response.data}
                and
                items.value = [ ...response.data]
                */
                console.log("home items", JSON.stringify(items.value));
            }
            catch (error) {
                console.log("homeItems error", error);
            }
        };
        
        const handleSearch = async(filteredValue) => {
            console.log("context vallue is", filteredValue);
            filtered.value = filteredValue;
        };
        
        const goToItemPage = async (itemId) => {
            //have to get specific itemId - now using router params not vuex
            console.log("iitemid", itemId);
            store.commit('setItem', itemId); //set in vuex
            router.push('/item');
        };
        return {
            isAuthenticated,
            items,
            topBid,
            csrfToken,
            sessionId,
            goToItemPage,
            filtered,
            handleSearch,
            itemList,
        };
    },
    components: { Searchbar }
};
</script>