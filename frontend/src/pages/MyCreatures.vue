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
            <h1 class="text-4xl font-bold text-gray-800">My Creatures</h1>
        </div>

        <div class="max-w-sm mx-auto mb-4">
            <div v-if="message" class="bg-indigo-100 border border-indigo-300 text-indigo-700 px-4 py-3 rounded relative" role="alert">
                <strong class="font-bold">Info: </strong>
                <span class="block sm:inline">{{ message }}</span>
            </div>
        </div>
        
        <!-- Form to upload image with types png, jpg -->
        <div class="flex justify-center items-center h-20">
            <input type="file" accept="image/png, image/jpeg" @change="handleFileUpload" class="border-2 border-gray-300 p-2 rounded-md" />
        </div>

        <div class="flex justify-center items-center h-20">
            <h1 class="text-4xl font-bold text-gray-800">List of Creatures</h1>
        </div>
        
        <!-- List of creatures file_names -->
        <div class="w-56 mx-auto mt-10">
            <ul class="flex flex-col border-2">
                <li v-for="creature in creatures" :key="creature.id" class="flex justify-center items-center">
                    <router-link class="font-medium text-gray-600 decoration-blue-500 decoration-2 underline-offset-2 hover:underline px-3 lg:px-5 py-2 flex items-center transition duration-150 ease-in-out" 
                    :to="'/file?filename=' + creature.filename + '&signature=' + creature.signature">{{ creature.filename }}</router-link>
                </li>
            </ul>
        </div>
    </div>
        

    </main>
    
    <!-- Site footer -->
    <Footer />    
    
</div>
</template>
  
<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import Header from '../partials/Header.vue'
import Footer from '../partials/Footer.vue'


const router = useRouter();
const isAuth = localStorage.getItem('auth') ? true : false;
const creatures = ref([]);

const message = ref('');

// Fetch files
axios.get(`http://${import.meta.env.VITE_BASE_URL}/files/`, {
    headers: {
        'Authorization': 'Bearer ' + localStorage.getItem('auth')
    }
})
.then(response => {
    creatures.value = response.data;
    console.log(response.data);
})
.catch(error => {
    console.log(error);
});

const handleFileUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    upload(file);
  } else {
    console.log('No file selected');
  }
};

const upload = async (file) => {
    try {
        const formData = new FormData();
        formData.append('file', file);

        const response = await axios.post(`http://${import.meta.env.VITE_BASE_URL}/upload_file/`, formData, {
            headers: {
                'Authorization': 'Bearer ' + localStorage.getItem('auth'),
                'Content-Type': 'multipart/form-data'
            }
        });
        console.log('File uploaded:', response.data);
        message.value = 'File uploaded successfully';
        axios.get(`http://${import.meta.env.VITE_BASE_URL}/files/`, {
            headers: {
                'Authorization': 'Bearer ' +localStorage.getItem('auth')
            }
        })
        .then(response => {
            creatures.value = response.data;
        })
        .catch(error => {
            console.log(error);
        });
    } catch (error) {
        console.log('Upload error:', error);
        message.value = error.response.data.error;
    }
};
</script>
