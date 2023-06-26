<script setup lang="ts">
import type { Request } from "~/types";

const { request, data, error, loading } = useRequest();

const props = defineProps<Request>();

const rxProps = reactive(props);

const fetchData = async () => {
  await request(rxProps);
};

const { state } = useStore();

onMounted(async () => {
  await request(rxProps);
});

watch(rxProps, fetchData);

watchEffect(() => {
  if (error.value) {
    state.notifications.push({
      status: "error",
      message:
        typeof error.value === "string"
          ? error.value
          : JSON.stringify(error.value),
    });
  }
});

const fetching = computed(() => loading.value);
</script>

<template>
  <slot name="default" :res="data"> </slot>
  <slot name="loading" :fetching="fetching"> </slot>
  <slot name="error" :error="error"> </slot>
</template>
