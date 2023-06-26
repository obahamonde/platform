<script setup lang="ts">
import { useUpload } from "~/composables/upload";
const { fileData, dropZoneRef, isOverDropZone, useInputEl } = useUpload();
const emit = defineEmits(["upload"]);
const uploadFile = async () => {
  if (!fileData.value) return;
  const { file } = fileData.value;
  const formdata = new FormData();
  formdata.append("file", file);
  const { data } = await useFetch("/api/image", {
    method: "POST",
    body: formdata,
  }).text();
  emit("upload", data);
  fileData.value = undefined;
};
</script>

<template>
  <div class="text-gray-400 flex gap-4 col center w-full max-w-400px">
    <div
      ref="dropZoneRef"
      @click="useInputEl"
      :multiple="false"
      accept="image/*"
      :class="isOverDropZone ? 'dropzone-on' : 'dropzone-off'"
      class="px-4 py-8 w-full"
      v-if="!fileData"
    >
      {{ isOverDropZone ? "Drop here" : "Drag and drop your picture here" }}
    </div>
    <div v-else>
      <button class="btn-get" @click="uploadFile">Upload</button>
      <button class="btn-del" @click="fileData = undefined">Delete</button>
    </div>
    <div class="col center m-8" v-if="fileData">
      <img :src="fileData.url" class="w-full h-auto" />
    </div>
  </div>
</template>

<style scoped>
.dropzone-off {
  @apply col bg-gray-100 items-center cp;
}

.dropzone-on {
  @apply col bg-gray-800 items-center cp text-white b-dash;
}
</style>
