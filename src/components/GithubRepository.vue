<script setup lang="ts">
import type { GithubRepo } from "~/types";
defineProps<{
  repo: GithubRepo;
}>();
const emit = defineEmits(["upload"]);

const getLanguageIcon = (lang: string | undefined) => {
  switch (lang) {
    case "JavaScript":
      return "logos:javascript";
    case "Python":
      return "logos:python";
    case "TypeScript":
      return "logos:typescript-icon";
    case "Vue":
      return "logos:vue";
    case "HTML":
      return "logos:html-5";
    case "CSS":
      return "logos:css-3";
    case "Shell":
      return "logos:terminal";
    case "C++":
      return "logos:c-plusplus";
    case "C":
      return "logos:c";
    case "C#":
      return "logos:c-sharp";
    case "Java":
      return "logos:java";
    case "PHP":
      return "logos:php";
    case "Ruby":
      return "logos:ruby";
    case "Go":
      return "logos:go";
    case "Rust":
      return "logos:rust";
    case "Dart":
      return "logos:dart";
    case "Kotlin":
      return "logos:kotlin";
    case "Swift":
      return "logos:swift";
    case "Scala":
      return "logos:scala";
    case "R":
      return "logos:r-lang";
    default:
      return "logos:github-octocat";
  }
};

const uploading = ref(false);

const handleUpload = async (repo: GithubRepo) => {
  uploading.value = true;
  emit("upload", repo.name);
};

watchEffect(() => {
  if (uploading.value) {
    // reset after emitting event
    uploading.value = false;
  }
});
</script>
<template>
  <div class="relative flex flex-col shadow-lg m-4 bg-white dark:bg-gray-500 rounded-xl max-w-md mx-4">
    <div class="absolute top-2 right-2 p-2">
      <Icon :icon="getLanguageIcon(repo.language)" class="x2" />
    </div>
    <div class="px-4 py-5 sm:p-6">
      <div class="pb-4">
        <div class="font-bold text-lg">
          {{ repo.name }}
        </div>
        <div class="text-gray-500 text-sm">
          {{ repo.full_name }}
        </div>
      </div>
      <div class="grid grid-cols-3 gap-4 pb-4">
        <div class="flex items-center space-x-2">
          <Icon icon="mdi-star" class="text-yellow-500" />
          <div class="font-bold">{{ repo.stargazers_count }}</div>
        </div>
        <div class="flex items-center space-x-2">
          <Icon icon="mdi-source-fork" class="text-green-500" />
          <div class="font-bold">{{ repo.forks_count }}</div>
        </div>
        <div class="flex items-center space-x-2">
          <Icon icon="mdi-eye" class="text-blue-500" />
          <div class="font-bold">{{ repo.watchers_count }}</div>
        </div>
      </div>
      <div class="pb-4 text-sm">
        <span class="font-bold">Description:</span>
        <span class="pl-2">{{
          repo.description || "No description available"
        }}</span>
      </div>
      <div class="row center gap-4">
        <a :href="repo.html_url" class="text-blue-500 dark:text-lime-300 hover:underline">View on GitHub</a>
        <button @click="handleUpload(repo)" :disabled="uploading"
          class="px-4 py-2 text-white rounded-lg shadow-md bg-gradient-to-r from-green-400 to-blue-500 hover:from-green-500 hover:to-blue-600 disabled:opacity-50">
          {{ uploading ? "Uploading..." : "Upload" }}
        </button>
        <div class="text-gray-500 dark:text-white text-xs">
          Last push: {{ new Date(repo.pushed_at).toLocaleDateString() }}
        </div>
      </div>
    </div>
  </div>
</template>
