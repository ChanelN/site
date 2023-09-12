<template>
    <p v-if="sellerLoggedIn&&inputClicked!=true" @click="answerQuestion(question_id)"> answer Question </p>
    <input type="text" v-show="inputClicked == true" v-model="answerInput">
    <button @click="submitAnswer(question_id)">Post</button>
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
    },
    setup(props, context){
        const answerInput = ref('');
        const inputClicked = ref(false);

        const answerQuestion = async(id) => {
            inputClicked.value = true

        };
        const submitAnswer = async(id) => {
            inputClicked.value = true;

            try{
                const response = await axios({
                    method:'post',
                    url: `http://127.0.0.1:8000/question/answer/`,
                    data: {
                        'question_id': id,
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
            answerInput,
            inputClicked,
            answerQuestion,
            submitAnswer,
        }
    }
})
</script>