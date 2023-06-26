export const useSSE = (url: string) => {
  const { status, data, eventSource, close } = useEventSource(`${url}`);

  const messages = ref<any[]>([]);

  watch(data, (newData) => {
    if (newData) {
      messages.value.push(JSON.parse(newData));
    }
  });

  onUnmounted(() => {
    close();
  });

  return {
    messages,
    status,
    eventSource,
  };
};
