<template>
    <p v-if="sellerLoggedIn&&inputClicked!=true" @click="submitAnswer(question.id)"> answer Q </p>
    <input type="text" v-show="inputClicked == true" v-model="answerInput">
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
        
    }
})
</script>