<template>
    <div class="itempage-center">
        <div class="page-container">
            <div class="itempage-left"> 
                <!--show if the current user isn't the same one who posted the item-->
                <form class="form-card" @submit.prevent="submitQuestion" >
                    <p> {{ sellerInfo}}</p>
                    <p> {{ user.id }}</p>
                    <h2>send question</h2>
                    <textarea v-model="user_question" class="text-field"></textarea>
                    <button type="submit"> submit</button>  
                </form>
            </div>

            <div class="itempage-right">
                <div>
                    <h3> Customer questions: </h3>
                    <!--https://vuejs.org/guide/essentials/list.html#maintaining-state-with-key-->
                    <div v-for="question in allQuestions" :key="question.id">
                        <h4>Q: {{ question.question }}</h4>
                        <p v-if="getAnswer(question.id) == true"> A: {{ answers }}</p>
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
import { computed, defineComponent, onBeforeUnmount, onMounted, onUnmounted, ref , watch,} from 'vue';
import { useRouter } from 'vue-router';

export default defineComponent({
    props:{
        sellerInfo: Object,
    },
    setup(props, context){
        const store = useStore();
        const router = useRouter();

        const csrfToken = computed(() => store.state.csrfToken);
        const sessionId = Cookies.get('sessionid');
        const user = computed(() => store.state.user); //current user not item user
        const itemId = computed(() => store.state.itemId);

        const user_question = ref('');
        const allQuestions = ref([]);
        const answers = ref([]);

        onMounted(async() => {
            console.log("get q's", itemId.value);
            getAllQuestions();
        });

        const submitQuestion = async() => {
            while (user_question.value.length == 0){
                console.log("empty field")
                return;
            }
            
            console.log("current user", user.value.id)
            console.log("quest", user_question.value)
            console.log("item", itemId.value)
            try{
                const response = await axios({
                method: 'post',
                url: 'http://127.0.0.1:8000/question/ask-question/',
                data: {
                    creator: user.value.id,
                    question: user_question.value,
                    item: itemId.value,
                },
                headers: {
                    'X-CSRFToken': csrfToken,
                    'X-SessionID': sessionId,
                    'Content-type': 'application/JSON',
                },
                withCredentials: true,
            })
            console.log("success", JSON.stringify(response.data));
            user_question.value="";
            } catch(error){
                console.log("error", error);
            }
        };

        const getAllQuestions = async() => {
            console.log("get all questions");
            try{
                const response = await axios({
                    method: 'get',
                    url: `http://127.0.0.1:8000/question/item-questions/${itemId.value}/`,
                });
                allQuestions.value = { ...response.data};
            } catch(error){
                console.log("error", error);
            }
        };

        const getAnswer = async(id) => {
            console.log("question id is ", id);

            const response = await axios.get(`http://127.0.0.1:8000/question/get-answers/${id}/`);
            answers.value = [ ...response.data];
            
            if (answers.value.length != 0){
                return true
            }
            return false
        };

        return{
            user,
            itemId,
            user_question,
            submitQuestion,
            allQuestions,
            getAllQuestions,
            getAnswer,
            answers,
        }
    }
});

</script>