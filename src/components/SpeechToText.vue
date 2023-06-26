<script setup lang="ts">
const { isListening, result, speech } = useSpeech();
const listening = computed(() => isListening.value);
const stop = () => {
  speech.stop();
  result.value = "";
};
</script>
<template>
  <div v-if="speech.isSupported">
    <div v-if="listening">
      <Icon
        class="btn-icon br fixed m-8 mb-28"
        icon="mdi-stop"
        @click="stop()"
      />
    </div>
    <div v-else>
      <Icon
        class="btn-icon br fixed m-8 mb-28"
        icon="mdi-microphone"
        @click="speech.start()"
      />
    </div>
    <slot name="output" :output="result"> </slot>
  </div>
  <div v-else>Speech recognition is not supported in your browser.</div>
</template>
