<script setup lang="ts">
import { ref } from 'vue'
const count = ref(0)
</script>
<template>
   <div className='container'>
          <h1>Vue</h1>
          <img src="https://cdn.worldvectorlogo.com/logos/vue-js-1.svg" alt="react" className="logo" />
          <p>{{ count }}</p>
          <button @click="count++">Click me</button>
          </div>
</template>