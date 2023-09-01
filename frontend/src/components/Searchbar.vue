<template>
    <input type="text" class="searchbar" v-model="input" v-on:input="filteredList()" placeholder="Search ..." />
</template>

<script>
import { defineComponent, ref } from 'vue';

export default defineComponent ({
    props: {
        items: Array,
    },
    setup(props, context){
        /*it will just emit filtered list */
        const input = ref("");
        const filtered = ref({});

        const filteredList = async() => {
            filtered.value = [] //do this so it clears every input - doesn't save ids frm lastt search
            
            console.log("input is ", input.value)
            if (input.value.length > 0){
                //input is compared to both item title and description
                console.log("items", props.items);
                filtered.value = props.items.filter(item => item.title.includes(input.value) || item.description.includes(input.value));
                if (filtered.value.length > 0){
                    context.emit("inputChanged", filtered.value);
                }
                else{
                    context.emit("inputChanged" , -1)
                }
            }
            else{
                context.emit("inputChanged", []);
            }      
        };

        return{
            input,
            filtered,
            filteredList,
        }
    },
});
</script>