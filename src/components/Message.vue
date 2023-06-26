<script setup lang="ts">
import { Message } from '~/types'
const props = defineProps<{
  items: Message[]
}>()
const { state } = useStore()
</script>
<template>
 <p :class="item.author === state.user!.ref ? 'text-right' : ''" v-for="item in props.items" class="m-8  bg-gray-200 dark:bg-gray-500 rounded-lg px-4 py-2">
        <img class="x3 rounded-full inline-block m-4 cp"
            :src="item.author === state.user!.ref ? state.user!.picture : 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/ChatGPT_logo.svg/1200px-ChatGPT_logo.svg.png'"
          />
        <div>
          <p class="p-4" v-html="item.content"></p>
        </div>
      </p>
</template>