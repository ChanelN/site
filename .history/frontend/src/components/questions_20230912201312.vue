<template>
    <div class="itempage-center">
        <div class="page-container">

            <div class="itempage-left"> 
                <!--show if the current user isn't the same one who posted the item-->
                <form class="form-card" @submit.prevent="submitQuestion" >
                    <h2>send question</h2>
                    <textarea v-model="user_question" class="text-field"></textarea>
                    <button type="submit"> submit</button>  
                </form>
            </div>


            <div class="itempage-right">
                <div>
                    <h3> Customer questions: </h3>
                    <!--https://vuejs.org/guide/essentials/list.html#maintaining-state-with-key-->

                    <div v-for="(question, index) in allQuestions" :key="question.id" class="itempage-center">
                        <h4>Q: {{ question.question }}</h4>
                        <!--question.id is the id from backend, while index is actual index inside of allQuestions-->
                        <!-- rendering the promise ob before it resolved:{{ getAnswer(index) }}  -->
                        <p v-if="answers[index]"> A: {{ answers[index] }} </p>
                        <!--<p v-else> </p>-->
                        <AnswerQ v-else :question_id="question.id" :sellerInfo="sellerInfo" @answered="handleNewAnswer"/>
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
import { stringifyQuery, useRouter } from 'vue-router';
import AnswerQ from '../components/answerQ.vue';


export default defineComponent({
    props:{
        sellerInfo: Object,
    },
    components:{
        AnswerQ,
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

        //same as resolvePromise, but specially for the method getAnswer
        const answeredQuestion = computed(() => {
            return allQuestions.value.map((question, index) => ({
                ...question,
                answer: getAnswer(index),
            }));
        });

        onMounted(async() => {
            console.log("user is", user.value);
            //means wait for each method
            //i need allQuestions to update when new question posted too
            await getAllQuestions();
            await resolvePromise(); 
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
            getAllQuestions();
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
                allQuestions.value = [ ...response.data]; //square brackets=arr
            } catch(error){
                console.log("error", error);
            }
        };

        const resolvePromise = async() => {
            answers.value = await Promise.all(
                allQuestions.value.map((question) => getAnswer(question.id))
            );
        };

        const getAnswer = async(id) => {
            console.log("question id is ", id);

            try{
                const response = await axios.get(`http://127.0.0.1:8000/question/get-answers/${id}/`);
                const answer = response.data.map((answer) => answer.answer).join(', ')
                console.log("answer for id", id, "in getAnswer is: ",  answer);
                return answer;
            } catch(error){
                console.log("error", error);
            }
            
        };
        
        //this method to update answers when new answer posted
        const handleNewAnswer = (payload) => {
            console.log("payload", payload);
            const { question_id, new_answer } = payload;

            console.log("question answered was ", question_id);
            console.log("answer is", new_answer.question_readable);
            
            //getAnswer(questionId);
            const questionIndex = allQuestions.value.findIndex(q => q.id === Number(question_id));
            console.log("answers qIndex = ", answers.value[questionIndex]);
            resolvePromise()

            /*
            
            if (questionIndex !== -1) {
                const updatedQuestion = { ...allQuestions.value[questionIndex] };
                updatedQuestion.answers.push(new_answer);
                // Replace the question in the array with the updated one
                allQuestions.value.splice(questionIndex, 1, updatedQuestion);
                resolvePromise()
            }
            
            if(questionIndex !== -1){
                //change the answer in the index - have to find index of q, then change answers[index]
                answers.value[questionIndex] = new_answer

            }*/
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
            handleNewAnswer,
            resolvePromise,
            answeredQuestion,
        }
    }
});

</script>