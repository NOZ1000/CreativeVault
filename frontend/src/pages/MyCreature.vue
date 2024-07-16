<template>
<div className="flex flex-col min-h-screen overflow-hidden">

    <!-- Site header -->
    <Header />

    <!-- Page content -->
    <main class="grow">

    <div v-if="!isAuth">
        <div class="flex justify-center items-center h-72">
        <h1 class="text-4xl font-bold text-gray-800">Please sign in to view your creatures</h1>
        </div>
    </div>
    <div v-else>

        <div class="flex justify-center items-center h-52">
            <h1 class="text-4xl font-bold text-gray-800">My Creature: </h1>
        </div>

        <div v-if="message" class="max-w-sm mx-auto mb-4">
            <div class="bg-indigo-100 border border-indigo-300 text-indigo-700 px-4 py-3 rounded relative" role="alert">
                <strong class="font-bold">Info: </strong>
                <span class="block sm:inline">{{ message }}</span>
            </div>
        </div>
        <!-- image that fetches throw api -->
        <div class="flex justify-center items-center">
            <img :src="imageURL" class="max-w-sm" />

        </div>
    </div>
        

    </main>
    
    <!-- Site footer -->
    <Footer />    
    
</div>
</template>
  
<script setup>
import axios from 'axios';
import { useRouter } from 'vue-router';
import { useRoute } from 'vue-router';
import Header from '../partials/Header.vue'
import Footer from '../partials/Footer.vue'
import { ref, onMounted } from 'vue';

const isAuth = localStorage.getItem('auth') ? true : false;
const imageURL = ref();

const message = ref('');
const route = useRoute();
const { filename, signature } = route.query;

onMounted(async () => {
  try {
    const response = await axios.get(`http://${import.meta.env.VITE_BASE_URL}/file?filename=${filename}&signature=${signature}`, {
      responseType: 'blob',
    });
    imageURL.value = URL.createObjectURL(response.data);
  } catch (error) {
    console.error('Error fetching image:', error);
    message.value = "Invalid file name or signature";
  }
});
</script>
