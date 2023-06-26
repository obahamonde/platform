<script setup lang="ts">
const { text, voices, voice, pickVoice, pause, stop, play } = useSynthesis();
const voicesLength = computed(() => voices.value.length);
const currentVoice = ref<string>("");
const toggle = ref<boolean>(false);
</script>
<template>
  <Modal v-if="voicesLength > 0 && toggle">
    <template #body>
      <select
        class="input"
        v-model="currentVoice"
        @change="pickVoice(currentVoice)"
      >
        <option v-for="v in voices" :value="v">
          {{ v }}
        </option>
      </select>
    </template>
    <template #footer>
      <button class="btn-del" @click="toggle = !toggle">Cancel</button>
    </template>
    <p>
      Selected voice: <strong>{{ voice.name }}</strong>
    </p>
  </Modal>
  <footer class="row w-1/2 p-4 sh rounded-lg">
    <div class="row gap-4 m-4">
      <Icon class="btn-icon" icon="mdi-translate" @click="toggle = !toggle" />
      <Icon class="btn-icon" icon="mdi-play" @click="play()" />
      <Icon class="btn-icon" icon="mdi-pause" @click="pause()" />
      <Icon class="btn-icon" icon="mdi-stop" @click="stop()" />
    </div>
    <textarea type="text" v-model="text" class="input w-full"></textarea>
  </footer>
</template>
