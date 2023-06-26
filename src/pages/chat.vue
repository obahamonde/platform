import { useAuth0 } from '@auth0/auth0-vue';
<script setup lang="ts">
import { useAuth0 } from "@auth0/auth0-vue";
const prompt = ref("");
const thisPrompt = ref("");
const handlePrompt = () => {
  prompt.value = thisPrompt.value;
  setTimeout(() => {
    thisPrompt.value = "";
  }, 100);
};
const { state, addMessage } = useStore();
const { logout } = useAuth0();
const fetchMessages = async () => {
  const response = await fetch("/api/messages?user=" + state.user!.ref!);
  const json = await response.json();
  state.messages = json.reverse();
};
const showModal = ref(false);
onMounted(fetchMessages);
</script>

<template>
  <section class="mt-12">
    <div v-if="prompt.length > 0 && thisPrompt.length === 0" class="mt-12 mx-8">
      <Request
        :url="'/api/completion?user=' + state.user!.ref!"
        :options="{
          method: 'POST',
          body: JSON.stringify({ prompt }),
        }"
      >
        <template #default="{ json }">
          <Message :items="addMessage(json)!" />
        </template>
      </Request>
    </div>
    <Message :items="state.messages" v-else />
    <div
      class="fixed bottom-0 left-0 right-0 bg-gray-800 w-full px-4 py-4 row center"
    >
      <img
        class="x3 rounded-full inline-block m-4 cp"
        :src="state.user!.picture"
        @click="showModal = true"
      />
      <input
        class="w-full px-4 py-2 outline-none rounded-md"
        type="text"
        v-model="thisPrompt"
        @keyup.enter="handlePrompt()"
        placeholder="Type something..."
      />
    </div>
  </section>
  <Modal v-if="showModal" @close="showModal = false">
    <template #header>
      <h3 class="text-lg font-bold">Profile</h3>
    </template>
    <template #body>
      <div class="flex flex-col items-center">
        <img
          class="x4 rounded-full inline-block mr-2"
          :src="state.user!.picture"
        />
        <p class="text-md font-bold">{{ state.user!.name }}</p>
        <p>{{ state.user!.email }}</p>
      </div>
    </template>
    <template #footer>
      <button class="btn-del dark:btn-get" @click="logout()">Logout</button>
    </template>
  </Modal>
</template>
