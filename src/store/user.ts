import { acceptHMRUpdate, defineStore } from "pinia";
import { User, Notification, Message } from "../types";

export const useStore = defineStore("state", () => {
  const state = reactive({
    notifications: [] as Notification[],
    user: null as User | null,
    token: null as string | null,
    messages: [] as Message[],
    data: null as any,
    githubUser: false as boolean,
  });

  const addMessage = (messages: Message[]) => {
    if (messages.length !== 2) {
      state.notifications.push({
        status: "error",
        message: "Expected 2 messages, got " + messages.length,
      });
      state.messages.unshift(...messages);
      return state.messages;
    }
  };
  return {
    state,
    addMessage,
  };
});

if (import.meta.hot)
  import.meta.hot.accept(acceptHMRUpdate(useStore, import.meta.hot));
