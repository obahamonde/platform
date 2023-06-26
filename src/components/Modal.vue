<template>
  <transition name="modal">
    <div
      class="fixed z-10 inset-0 overflow-y-auto bg-black bg-opacity-50"
      @click.self="emit('close')"
    >
      <div class="flex items-center justify-center min-h-screen">
        <div class="bg-white dark:bg-gray-500 rounded-lg shadow-lg p-8">
          <div class="modal-header">
            <slot name="header">
              <!-- Default header content can be placed here -->
            </slot>
          </div>
          <div class="modal-body">
            <slot></slot>
          </div>
          <div class="modal-footer">
            <button class="btn-del my-4" @click="emit('close')">Close</button>
            <slot name="footer"> </slot>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup lang="ts">
const emit = defineEmits(["close"]);
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s;
}

.modal-enter,
.modal-leave-to

/* .modal-leave-active in <2.6 */ {
  opacity: 0;
}

.modal-footer {
  @apply row center;
}
</style>
