<template>
  <div className="flex flex-col min-h-screen overflow-hidden">

    <!-- Site header -->
    <Header />

    <!-- Page content -->
    <main class="grow">

      <Hero />
      <!-- <Inspiration /> -->
      <!-- <Carousel /> -->
      <Creatives />
      <!-- <Pricing /> -->
      <!-- <Testimonials /> -->
      <!-- <Faqs /> -->
      <!-- <Blog /> -->
      <Cta />

    </main>
    
    <!-- Site footer -->
    <Footer />    

  </div>
</template>

<script setup>
import Header from '../partials/Header.vue'
import Hero from '../partials/Hero.vue'
import Creatives from '../partials/Creatives.vue'
import Cta from '../partials/Cta.vue'
import Footer from '../partials/Footer.vue'



</script>