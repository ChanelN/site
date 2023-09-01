<template>
    <button @click="deleteItem">Remove listing</button>
</template>

<script>
import axios from 'axios';
import { mapMutations, mapGetters, mapState } from 'vuex';
import Cookies from 'js-cookie';
import { computed, defineComponent, onMounted, onUnmounted, ref} from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

/* this gets passed the itemid number from the sellingOverview page*/
export default defineComponent({
    props:{
        itemId: Number,
    },
    setup(props, context){
        const store = useStore();
        const router = useRouter();
        const {isAuthenticated, getCSRFToken} = mapGetters(['getIsAuthenticated', 'getCSRFToken']);
        const {updateUser, setItem} = mapMutations(['updateUser', 'setItem']);
        const csrfToken = computed(() => store.state.csrfToken);
        const sessionId = Cookies.get('sessionid');
        const user = computed(() => store.state.user);
        //const itemId = computed(() => store.state.itemId);

        /*where do you set the item id? , might not be correct one*/ 
        const deleteItem = async() =>{
            try{
                console.log(props.itemId);
                const response = await axios({
                    method: 'delete',
                    url: `http://127.0.0.1:8000/item/delete/${props.itemId}/`,
                    headers: {
                        'X-CSRFToken': csrfToken.value,
                        'X-SessionID': sessionId,
                        'Content-type': 'application/JSON',
                    },
                    withCredentials: true,
                })
                context.emit('deleteSuccess', props.itemId );
            } catch(error){
                console.log("cant delete", error);
            }
        };

        return{
            store,
            router,
            isAuthenticated,
            getCSRFToken,
            updateUser,
            setItem,
            csrfToken,
            sessionId,
            user,
            deleteItem,
        }
    },
});
</script>