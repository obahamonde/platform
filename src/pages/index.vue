<script setup lang="ts">
const url = ref("");
const sse = ref(null) as Ref<EventSource | null>;
const showBot = ref(false);
const prompt_ = ref("");
watch(url, (newUrl) => {
  if (sse.value) {
    sse.value.close();
  }
  sse.value = new EventSource(`/api/ingest?url=${newUrl}`);
  sse.value.onmessage = (event) => {
    if (JSON.parse(event.data).message) {
      showBot.value = true;
    }

    progress.value = Number(JSON.parse(event.data).progress);
  };
});
const messages = ref([]) as Ref<string[]>;
const progress = ref(0);
const thisProgress = computed(() => {
  return progress.value;
});
const send = async () => {
  const { data } = await useFetch(
    "/api/search?url=" + url.value + "&prompt=" + prompt_.value
  ).text();
  prompt_.value = "";
  messages.value.push(unref(data) as string);
};
</script>
<template>
        <div v-if="!showBot">{{ (thisProgress * 100).toFixed(2) }}%</div>
        <input type="text" class="input-text" v-model="url" />

        <div
          class="br fixed sh p-4 rounded-lg bg-gray-100 max-w-2xl max-h-2xl overflow-scroll"
        >
          <div class="mb-48">
            <div v-for="message in messages" class="mb-4">
              <div v-html="message"></div>
            </div>
          </div>
          <div class="row center gap-4">
            <input
              type="text"
              class="input-text"
              v-model="prompt_"
              @keyup.enter="send"
            />
            <img :src="url + '/favicon.ico'" class="x2" @click="showBot = !showBot" />
          </div>
        </div>
</template>
