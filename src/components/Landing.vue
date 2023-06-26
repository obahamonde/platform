<script setup lang="ts">
const { signinWithPopup } = useAuth();
defineProps({
  title: String,
  logo: String,
  hero: String,
  text: String,
});
</script>
<template>
  <main
    class="container w-full px-64 col center mx-auto h-full"
    :style="'background-image: url(' + hero + ')'"
  >
    <img
      :src="logo"
      alt="logo"
      class="x12 m-16 logo"
      @click="signinWithPopup()"
    />
    <h1 class="text-gray-300 font-script text-4xl">{{ title }}</h1>
    <p class="text-light text-xl font-sans m-16">{{ text }}</p>

    <GithubButton />
  </main>
</template>
