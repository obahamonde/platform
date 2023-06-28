<script setup lang="ts">
const modal = ref(false);
const send = async (output: string) => {
  if (output.length == 0) return;
  alert(output);
  modal.value = false;
};
const chat = ref(false);
const footer = ref(false);
const toggleChat = () => {
  chat.value = !chat.value;
  if (chat.value) {
    modal.value = false;
  }
};
watch(
  () => modal.value,
  (val) => {
    if (val) {
      chat.value = false;
    }
  }
);
watch(
  () => chat.value,
  (val) => {
    if (val) {
      modal.value = false;
    }
  }
);
</script>
<template>
  <Icon icon="logos:openai-icon" class="x4 dark:invert btn-icon br fixed m-8" @click="modal = !modal" />

  <SpeechToText v-if="modal">
    <template #output="{ output }">
      <section class="row center mx-auto">
        <footer class="row bottom-0 fixed m-8 px-8 py-4 sh w-1/2 rounded-lg" v-if="output">
          {{ output }}
          <Icon icon="mdi-send" class="btn-icon right-2 absolute x2" @click="send(output)" v-if="output" />
        </footer>
      </section>

      <Icon icon="mdi-chat" class="btn-icon br fixed m-8 mb-28 mr-16" @click="toggleChat" />
    </template>
  </SpeechToText>
  <Upload />
  <ChatMessage v-if="chat" />
</template>
