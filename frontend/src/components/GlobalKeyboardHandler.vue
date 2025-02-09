<script setup lang="ts">
import { onMounted, onBeforeUnmount } from 'vue';
import {useCurrentImageStore} from "@/store/currentImage";

const currentImageStore = useCurrentImageStore();
const {redoRectangle, undoRectangle} = currentImageStore;
const modifier = /(Mac|iPhone|iPod|iPad)/i.test(navigator.platform) ? 'metaKey' : 'ctrlKey';

function handler(event: KeyboardEvent) {
  if (event.keyCode == 90 && event[modifier]) {
    event.preventDefault()
    if (event.shiftKey) {
      redoRectangle();
    } else {
      undoRectangle();
    }
  }
}

onMounted(() => {
  window.addEventListener('keydown', handler);
});

onBeforeUnmount(() => {
  window.removeEventListener('keydown', handler);
});
</script>

<template>
  <div></div>
</template>

<style scoped>
div {
  display: none;
}
</style>
