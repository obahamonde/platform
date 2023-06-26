import { toggleDark } from '../composables/dark';
<script setup lang="ts">
import { isDark, toggleDark } from "../composables/dark";
</script>
<template>
  <button @click="toggleDark()">
    <Icon
      :icon="isDark ? 'mdi-weather-night' : 'mdi-weather-sunny'"
      class="x2 tr m-4 fixed"
    />
  </button>
</template>
