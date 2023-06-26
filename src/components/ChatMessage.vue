<script setup lang="ts">
const output = ref("");
const send = (opt: string) => {
  if (opt.length == 0) return;
  alert(opt);
  output.value = "";
};
</script>
<template>
  <section class="row center mx-auto">
    <footer class="row bottom-0 fixed m-8 pl-4 h-14 sh w-1/2 rounded-lg">
      <input
        class="w-full h-full bg-transparent no-outline"
        v-model="output"
        @keyup.enter="send(output)"
        placeholder="Type something..."
      />
      <Icon
        icon="mdi-send"
        class="btn-icon m-2 mt-4 right-2 absolute x2"
        @click="send(output)"
        v-if="output"
      />
    </footer>
  </section>
</template>
