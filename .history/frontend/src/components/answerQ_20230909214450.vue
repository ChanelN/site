<template>
    <p v-if="sellerLoggedIn && inputClicked!=true" @click="answerQuestion"> answer Question </p>
    <input type="text" v-show="inputClicked == true" v-model="answerInput">
    <button v-show="inputClicked == true" @click="submitAnswer">Post</button>
    <img v-show="inputClicked == true" src="../assets/exit.png" class="exit" @click="exitInput"/>
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
    emits: ['answered'],
    setup(props, context){
        const store = useStore();
        const csrfToken = computed(() => store.state.csrfToken);
        const sessionId = Cookies.get('sessionid');
        const user = computed(() => store.state.user); //current user not item user
        
        const answerInput = ref('');
        const inputClicked = ref(false);

        onMounted(() => {
            console.log("question id prop: ", props.question_id, "user is ," , user.value);
        });

        const sellerLoggedIn = computed(() => {
            if (user.value && props.sellerInfo.id == user.value.id){
                return true
            }
            return false
        });
        const answerQuestion = async() => {
            inputClicked.value = true;
        };
        const exitInput = async() =>{
            inputClicked.value = false;
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
                context.emit('answered', {question_id: props.question_id, new_answer:response.data});
            } catch(error){
                console.log(error);
            }
            inputClicked.value = false;
        };

        return{
            sellerLoggedIn,
            answerInput,
            exitInput,
            inputClicked,
            answerQuestion,
            submitAnswer,
        }
    }
})
</script>