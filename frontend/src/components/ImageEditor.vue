<script setup lang="ts">
import {ref,getCurrentInstance} from "vue";
import { useElementSize } from '@vueuse/core'
import {storeToRefs} from "pinia";
import {useCurrentImageStore} from "@/store/currentImage";

const image = ref<HTMLImageElement | null>(null);
const { width: imageWidth, height: imageHeight } = useElementSize(image);

const currentImageStore = useCurrentImageStore();
const {canvas, forceRerender} = storeToRefs(currentImageStore);
const {addRectangle} = currentImageStore;

let startX: number | null = null;
let startY: number | null = null;

const rerenderHack = ref(false);

forceRerender.value = () => {
  const instance = getCurrentInstance();
  instance?.proxy?.forceUpdate();
}

const startSquare = (event: MouseEvent) => {
  if (!canvas.value) {
    return;
  }
  const rect = canvas.value.getBoundingClientRect();
  startX = event.pageX - rect.left;
  startY = event.pageY - rect.top;
}

const endSquare = (event: MouseEvent) => {
  if (startX === null || startY === null || !canvas.value) {
    return;
  }

  const rect = canvas.value.getBoundingClientRect();
  const endX = event.pageX - rect.left;
  const endY = event.pageY - rect.top;

  addRectangle({
    x: Math.min(startX, endX),
    y: Math.min(startY, endY),
    width: Math.abs(endX - startX),
    height: Math.abs(endY - startY)
  });
}
</script>

<template>
<div
  class="position-relative w-100 h-100"
  ref="bounding"
>
  <img
    src="https://cdn.vuetifyjs.com/images/parallax/material.jpg"
    class="bound center"
    ref="image"
  />
  <canvas
    ref="canvas"
    class="position-absolute center"
    :width="imageWidth"
    :height="imageHeight"
    :style="{
      width: `${imageWidth}px`,
      height: `${imageHeight}px`,
      cursor: 'crosshair'
    }"
    @mousedown="startSquare"
    @mouseup="endSquare"
  />
</div>
</template>

<style scoped>
.bound {
  max-height: 90%;
  max-width: 90%;
}

.center {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
</style>
