<!--this will be an overlay on top of the itemPage
it will take and place new bid price - in itemPage it tries to recieve highest bid? -->
<template>
    <div class="overlay">
      <div class="form-card">
        <!--<button @click="closeOverlay">Close</button>-->
        <img src="../assets/exit.png" class="exit" @click="closeOverlay"/>
        <h2 class="headline">Place bid</h2>
        <hr>
        <h3>enter your max bid:</h3>
        <h4 v-if="highestBid"> £{{ highestBid}} or more</h4>
        <h4 v-else="itemObj.starting_price"> £{{ itemObj.starting_price }}</h4>
        <form @submit.prevent="placeBid">
            <!--step allows me to input decimal numbers-->
            <input type="number" class="text-field" step=".01" v-model="bid_price" required>
            <button type="submit" :disabled="bidHighEnough" class="login-btn">Place bid</button>
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
import Cookies from 'js-cookie';
import {defineComponent, ref, computed, onBeforeMount} from 'vue';

export default defineComponent({
    props: {
        itemObj: Object,
        highestBid: Number,
    },
    setup(props, context){
        const store = useStore();
        const errorMessage = ref('');
        const bid_price = ref(null); //this is user input

        const csrfToken = computed(() => store.state.csrfToken);
        const sessionId = Cookies.get('sessionid');
        const user = computed(() => store.state.user);

        const bidHighEnough = computed(() => {
            if(props.highestBid){
                return bid_price.value !== null && bid_price.value < props.highestBid;
            }
            return bid_price.value !== null && bid_price.value < props.itemObj.starting_price;
        });


        //everytime i close the overlat, the GET ITEM is called again in itemPage?
        //i also need another field to store the highest current bid - not the same as starting_price
        const closeOverlay = async() => {
            console.log(JSON.stringify(props.itemObj));
            //have to emit to the itemPage
            context.emit('closeOverlay')
        };

        //i think i now need to update the item starting price so i can retrieve in home page
        //but how would i know whose bid it is
        const placeBid = async() => {
            console.log("trying to pplace biid");
            console.log("creator id", props.itemObj.creator);
            console.log("current bidder", user.value.id);
            console.log("item", props.itemObj.id, bid_price.value);

            //this method is what sends the axios request 
            //it also needs to check input field that its not lower than
            //current highest bid
            try{
                const response = await axios({
                    method: 'post',
                    url: `http://127.0.0.1:8000/bidding/place-bid/`,
                    data:{
                        creator: props.itemObj.creator,
                        bidder: user.value.id,
                        item: props.itemObj.id,
                        bid_price: bid_price.value,
                    },
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'X-SessionID': sessionId,
                        'Content-type': 'application/JSON',
                    }, 
                    withCredentials: true,
                })
                console.log("success", JSON.stringify(response.data));   
                context.emit('bidPlaced');
                closeOverlay();
            } catch(error){
                if(error.response.data){
                    errorMessage.value = error.response.data.non_field_errors[0];
                }       
                else{
                    console.log("error", error);
                }
            }
        };

        return{
            store,
            errorMessage,
            bid_price,
            csrfToken,
            sessionId,
            user,
            bidHighEnough,
            closeOverlay,
            placeBid,
        }
    }
});
</script>

<style>
.overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color:  rgba(0, 0, 0, 0.6); /*tthis sets grey transparentt background*/
    display: flex;
    align-items: center;
    justify-content: center;
}
</style>