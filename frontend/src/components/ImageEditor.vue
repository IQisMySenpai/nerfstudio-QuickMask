<script setup lang="ts">
import {ref,getCurrentInstance} from "vue";
import { useElementSize } from '@vueuse/core'
import {storeToRefs} from "pinia";
import {useCurrentImageStore} from "@/store/currentImage";
import {useImageStore} from "@/store/images";

const image = ref<HTMLImageElement | null>(null);
const { width: imageWidth, height: imageHeight } = useElementSize(image);

const imagesStore = useImageStore();
const {selected, frames} = storeToRefs(imagesStore);

const currentImageStore = useCurrentImageStore();
const {canvas} = storeToRefs(currentImageStore);
const {addRectangle} = currentImageStore;

let startX: number | null = null;
let startY: number | null = null;

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

  addRectangle(Math.min(startX, endX), Math.min(startY, endY), Math.abs(endX - startX), Math.abs(endY - startY));

  startX = null;
  startY = null;
}
</script>

<template>
<div
  class="position-relative w-100 h-100"
  ref="bounding"
>
  <img
    alt="Selected"
    :src="`/api/image/${selected}`"
    class="bound center"
    ref="image"
  />
  <img
    v-if="frames && frames[selected].has_existing_mask"
    alt="Selected"
    :src="`/api/mask/${selected}`"
    class="bound center"
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
    @mouseleave="endSquare"
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
