<script setup lang="ts">
import type { ContainerCreate } from "~/types";
const templates = reactive({
  about: "Pick your template",
  templates: [
    "logos:react",
    "logos:vue",
    "logos:ruby",
    "logos:express",
    "simple-icons:fastapi",
    "logos:php",
  ],
  response: null as any,
});
const { state } = useStore();

const selected = ref("");

const containerCreate = reactive<ContainerCreate>({
  login: state.user!.name,
  repo: "",
  token: state.token!,
  email: state.user!.email as string,
  image: computed(() =>
    selected.value ? (selected.value.split(":").pop() as string) : null
  ) as any,
});

const createRepo = async (body: ContainerCreate) => {
  const { data } = await useFetch("/api/github/workspace", {
    method: "POST",
    body: JSON.stringify(body),
  }).json();
  templates.response = unref(data);
  state.notifications.push({
    message: "Template created",
    status: "success",
  });
};

const toggle = computed(() => {
  return selected.value ? true : false;
});
</script>
<template>
  <div>
    <div
      class="text-center text-2xl font-bold col center gap-4 bg-light px-16 py-8 rounded-lg sh"
      v-if="templates.response"
    >
      <h1
        class="text-lg text-accent font-sans drop-shadow-color-success drop-shadow-sm"
      >
        Your Development Stack is Ready!
      </h1>
      <div class="text-center text-2xl font-bold row center gap-4">
        <a
          :href="templates.response.workspace.url"
          target="_blank"
          class="text-teal-700"
        >
          <Icon icon="logos:visual-studio-code" class="x4 scale" />
        </a>
        <div class="col center p-4">
          <a
            :href="'http://' + templates.response.preview.ip"
            target="_blank"
            class="text-teal-700"
          >
            <img src="/logo.svg" class="x4 scale" />
          </a>
        </div>

        <a
          :href="templates.response.preview.repo"
          target="_blank"
          class="text-teal-700"
        >
          <Icon icon="logos:github-icon" class="x4 scale" />
        </a>
      </div>
    </div>
  </div>
  <section class="grid3">
    <div v-for="template in templates.templates" class="col center gap-8">
      <Icon
        :icon="template"
        class="template-icon"
        @click="selected = template"
        :class="selected === template ? 'animate-bounce' : ''"
      />
      <h1 class="template-name">{{ template.split(":").pop() }}</h1>
    </div>
  </section>
  <Modal v-if="toggle" :title="templates.about" @close="selected = ''">
    <div class="flex flex-col gap-4 action-button">
      <span>
        <input
          class="input-text"
          v-model="containerCreate.repo"
          placeholder="Repository name"
        />
      </span>
      <button
        @click="createRepo(containerCreate)"
        :disabled="!containerCreate.repo"
      >
        Get started
      </button>
    </div>
  </Modal>
</template>
<style scoped>
.template-icon {
  @apply x6 cp scale text-teal-700 m-8;
}

.template-name {
  @apply text-center text-teal-700 m-4 text-lg font-bold;
}
</style>
