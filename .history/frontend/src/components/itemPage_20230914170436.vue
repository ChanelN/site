<template>
    <!--this is the actual page for specific item everyone sees
    the item info, seller info, bids, and questions posted here
    so once a bid is made starting price changes to current highest bid on main page too--->

    <!--so i want the image as the only thing on the left side of the container
    then all details on right in order of title, time left, current price, description
    change starting price to current bid_price-->
    <div class="outer-container">
        <nav class="separator" v-if="user && user.id == item.creator" >
            <router-link :to="{ name: 'item-update', params: { itemId:itemId }}"> Update listing</router-link>
        </nav>
        
        <nav class="separator" v-if="aunctionHasEnded">
            <p> bidding has ended on this item</p>
        </nav>
        <!--page-container only makes columns, cant have column+row
        i tried to make outer-container the scrollable one, havent tested-->
        <div class="page-container">
            <div class="itempage-left">
                <img class="page-img" :src="item.picture" alt="item pic" v-if="item.picture"/>
            </div> 
            
            <div class="itempage-right">
                <h1>{{ item.title }}</h1>
                <p> Sold by: {{ sellerInfo.email }}</p>
                <hr>

                <h4>Time left:</h4>
                <p>{{ days }}d {{ hours }}h {{ minutes }}m {{ secs }}s || {{ formattedTime }}</p>
                <hr>

                <!--this should all be computed insteaad-->
                <h4 v-if="topBid == null"> Starting price:</h4>
                <!--starting price shoould be changed to hiighest bid-->
                <p v-if="topBid == null" >£{{ item.starting_price }}</p>
                <h4 v-if="topBid&&aunctionHasEnded==true" > Winning bid:</h4>
                <h4 v-if="topBid&&aunctionHasEnded!=true"> Current bid:</h4>
                <p v-if="topBid">£ {{ topBid }}</p>
                
                <button type="submit" @click="verifyUser">Place Bid</button>
                <placeBid :itemObj="item" :highestBid="topBid" v-if="bidForm" @closeOverlay="bidForm = false" @bidPlaced="handleNewBid"/>
                <p v-if="errorMessage" class="error-message"> {{ errorMessage }}</p>
            </div>
        </div>

        <div class="itempage-center">
                <h4>Item description:</h4>
                <p>{{ item.description }}</p>
                <!--need to include details of the items owner
                storing each items user in vuex isnt good- so -- get creator from item model?-->
        </div> 

        <questions :sellerInfo="sellerInfo"/>
    </div>
</template>

<script>
import axios from 'axios';
import { useStore } from 'vuex';
import { mapMutations, mapGetters, mapState } from 'vuex';
import Cookies from 'js-cookie';
import { computed, defineComponent, onBeforeUnmount, onMounted, onUnmounted, ref , watch,} from 'vue';
import { useRouter } from 'vue-router';
import placeBid from './placebid.vue';
import questions from '../components/questions.vue';

export default defineComponent({
    components:{
        placeBid,
        questions,
    },
    setup(props, context){
        const store = useStore();
        const router = useRouter();
        //this checks that we're still on itemPage and we can contnue requesting animationFrame - otherwise stop
        const isCurrentRouterView = computed(() => router.currentRoute.value.fullPath == '/item');

        const {isAuthenticated, getCSRFToken, getItemId} = mapGetters(['getIsAuthenticated', 'getCSRFToken', 'getItemId']);
        const {updateUser, clearItem} = mapMutations(['updateUser', 'clearItem']);

        const csrfToken = computed(() => store.state.csrfToken);
        const sessionId = Cookies.get('sessionid');
        const user = computed(() => store.state.user); //current user not item user
        const itemId = computed(() => store.state.itemId);
        const item = ref({});
        
        const days = ref(0);
        const hours = ref(0);
        const minutes = ref(0);
        const secs = ref(0);
        const formattedTime = ref('');
        const errorMessage = ref('');
        const bidForm = ref(false);

        const topBid = ref(null); //current highest bid price
        const winner_id = ref(null);
        
        const aunctionHasEnded = ref(false);
        const auction_end = ref(null);

        const sellerInfo = ref({});
        const user_question = ref('');

        onMounted(async() =>{
            await getItem();
            await getSeller();
            console.log("isCurrent?", isCurrentRouterView.value);
            
            /*
            issue is that you have to be on the page for the timer to run out
            but actually that's not effective because item should be ended in background
            but the problem was that it waas starting aa new checkAuctionEnd for each item i clicked on
            so if the user clicks on 3 items, there's 3 different timers in the background
            */
            if (isCurrentRouterView.value){
                await calculateTime();
                requestAnimationFrame(calculateTime);

                await getHighestBid();
                requestAnimationFrame(getHighestBid);

                await checkAuctionEnd();
                requestAnimationFrame(checkAuctionEnd);
            }
        });

        onBeforeUnmount(() => {
            if (isCurrentRouterView.value){
                console.log("unmount")
                cancelAnimationFrame(checkAuctionEnd)
                cancelAnimationFrame(calculateTime);
                cancelAnimationFrame(getHighestBid);    
            }
        });


        const calculateTime = async() =>{
            if (aunctionHasEnded.value == true || !isCurrentRouterView.value){
                return; //stop updating the time once auction ends or if we navigated to another page
            }
            //countdown time
            const end_time = new Date(item.value.end_time);
            const now = new Date();
            const timeDifference = end_time - now;
            days.value = Math.floor(timeDifference / (1000 * 60 * 60 * 24));
            hours.value = Math.floor((timeDifference / (1000 * 60 * 60)) % 24);
            minutes.value = Math.floor((timeDifference / 1000 / 60) % 60);
            secs.value = Math.floor((timeDifference / 1000) % 60);
            
            requestAnimationFrame(calculateTime);
        };
        
        const formatDate = () => {
            //formatted the model data
            const end_time = new Date(item.value.end_time);
            console.log(item.value.end_time, end_time);

            const options = {
                day: 'numeric',
                month: 'short',
                hour: 'numeric',
                minute: 'numeric',
            };
            formattedTime.value =  end_time.toLocaleString('en-GB', options);
        };

        const getItem = async() =>{
            console.log("current id in vuex =", itemId.value);
            try{
                const response = await axios({
                    method: 'get',
                    url: `http://127.0.0.1:8000/items/${itemId.value}/`,
                });
                item.value = { ...response.data };
                console.log(JSON.stringify(item.value));
                auction_end.value = new Date(response.data.end_time);

                formatDate();
            }catch(error){
                console.log("getItem error", error);
            }
        };

        const getSeller = async() => {
            try{
                const response = await axios({
                    method: 'get',
                    url: `http://127.0.0.1:8000/users/${item.value.creator}/`,
                });
                console.log("response", response.data);
                sellerInfo.value = { ...response.data}; //if i use [], it says that response data iis not iterable, why is it ok sometimes and not others
            } catch(error){
                console.log(error);
            }
        };

        const updateProfile = async() => {
            router.push('/item-update');
        };

        const handleNewBid = async() => {
            console.log("new");
            requestAnimationFrame(getHighestBid);
        };

        const getHighestBid = async() => {
            //this view in Item filters based on bid_price, in Bid view now that i'm setting field won to True for current highest,
            //i can jus filter for this instead
            try{
                const response = await axios({
                    method: 'get',
                    url: `http://127.0.0.1:8000/item/highest-bid/${itemId.value}/`,
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'X-SessionID': sessionId,
                        'Content-type': 'application/JSON',
                    },
                    withCredentials: true,
                })
                console.log("response", response.data );
                console.log("NEW HIGHEST BID IS", response.data.highest_bid, typeof response.data.highestBid);
                console.log("current", item.value.starting_price);
                if (response.data.highest_bid > item.value.starting_price){
                    topBid.value = response.data.highest_bid;
                    winner_id.value = response.data.bidder;
                    console.log("NEW topp price", winner_id.value);
                }
            } catch(error){
                console.log("can't get highest bid", error);
            }
        };

        const verifyUser = async() => {
            //if logged in, they can bid, if not -> login
            if(user.value){
                bidForm.value = true
            }
            else{
                router.push('/login');
            }  
        };

        //this method is called once the time ends, but what if there were no bids
        //IT UPDATES THE ITEM OBJ ITSELF WITH WINNER- SO IT NEEDS GETHIGHESTBID
        const updateBidWinner = async() => {
            //make a request, to update field sold=True (sold=True means that the auction has fully ended now)
            // while won=True only means its the current highest bidder, i should rename the field
            console.log("winner_id", winner_id.value);
            try{
                if(winner_id.value){
                    const response = await axios({
                        method: 'put',
                        url: `http://127.0.0.1:8000/item/update/${itemId.value}/`,
                        data: {
                            creator: sellerInfo.value.id,
                            winner_id: winner_id.value,
                            is_sold: true,
                        },
                        headers: {
                            'X-CSRFToken': csrfToken,
                            'X-SessionID': sessionId,
                            'Content-type': 'application/JSON',
                        },
                        withCredentials: true,
                    });   
                    console.log("successfully updated winner id in Item");
                }
            } catch(error){
                console.log("error updating Bid sold", error);
            }         
        };

        const checkAuctionEnd = async() => {
            const now = new Date();
            console.log("CHECK AUCTION END", auction_end.value);
            if (!isCurrentRouterView.value){
                return; //stop updating if we navigated to another view
            }
            else if (now >= auction_end.value){
                aunctionHasEnded.value = true;
                console.log("ended", aunctionHasEnded.value);
                
                cancelAnimationFrame(checkAuctionEnd);
                //i need to now update the item instance so that Item field sold = yes, need to make new field to store winner ID too.
                await updateBidWinner();
                sendWinnerEmail();
                return;
            }
            else{
                //only if not over
                requestAnimationFrame(checkAuctionEnd);
            }
        };
        
        const sendWinnerEmail = async() => {
            //view to send is in Item - its a function not class urkl is item/winner/
            console.log("winner_id", JSON.stringify(winner_id.value));
            if(winner_id.value != null){
                const email = await axios({
                    method: 'post',
                    url: 'http://127.0.0.1:8000/item/winner/',
                    data: {
                        subject: `You're the winner of ${item.value.title}`,
                        message: 'Congrats! You were the highest bidder.',
                        from_email: sellerInfo.value.email,
                        recipient: 'chanel.kim.ngo@gmail.com' //to test only,
                    }, 
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'X-SessionID': sessionId,
                        'Content-type': 'application/JSON',
                    },
                    withCredentials: true,
                })
                console.log("SENT EMAIL");
            }
        };

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
            } catch(error){
                console.log("error", error);
            }
        };

        return{
            store,
            isAuthenticated,
            getCSRFToken,
            getItemId,
            updateUser,
            clearItem,
            csrfToken,
            sessionId,
            user,
            itemId,
            item,
            getItem,
            router,
            updateProfile,
            days,
            hours,
            minutes,
            secs,
            formattedTime,
            errorMessage,
            bidForm,
            getHighestBid,
            topBid,
            verifyUser,
            handleNewBid,
            checkAuctionEnd,
            winner_id,
            aunctionHasEnded,
            sellerInfo,
            getSeller,
            user_question,
            submitQuestion,
        }
    }
});
</script>