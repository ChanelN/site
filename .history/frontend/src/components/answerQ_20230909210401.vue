<template>
    <p v-if="sellerLoggedIn && inputClicked!=true" @click="answerQuestion"> answer Question </p>
    <input type="text" v-show="inputClicked == true" v-model="answerInput">
    <button @click="submitAnswer">Post</button>
</template>

<script>
import axios from 'axios';
import { useStore } from 'vuex';
import { mapMutations, mapGetters, mapState } from 'vuex';
import Cookies from 'js-cookie';
import { computed, defineComponent, onBeforeUnmount, onMounted, onUnmounted, ref , watch,} from 'vue';
import { useRouter } from 'vue-router';

export default defineComponent({
    props:{
        question_id: Number,
        sellerInfo: Object,
    },
    setup(props, context){
        const store = useStore();
        const csrfToken = computed(() => store.state.csrfToken);
        const sessionId = Cookies.get('sessionid');
        const user = computed(() => store.state.user); //current user not item user
        
        const answerInput = ref('');
        const inputClicked = ref(false);


        const sellerLoggedIn = computed(() => {
            console.log("question id prop: ", props.question_id, "user is ," , user.value);
            if (user.value && props.sellerInfo.id == user.value.id){
                return true
            }
            return false
        });
        const answerQuestion = async() => {
            inputClicked.value = true
        };
        const submitAnswer = async() => {           
            try{
                const response = await axios({
                    method:'post',
                    url: `http://127.0.0.1:8000/question/answer/`,
                    data: {
                        'question_id': props.question_id,
                        'creator': user.value.id,
                        'answer': answerInput.value,
                    },
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'X-SessionID': sessionId,
                        'Content-type': 'application/JSON',
                    },
                    withCredentials: true,
                })
            } catch(error){
                console.log(error);
            }
            inputClicked.value = false;
        };

        return{
            sellerLoggedIn,
            answerInput,
            inputClicked,
            answerQuestion,
            submitAnswer,
        }
    }
})
</script>