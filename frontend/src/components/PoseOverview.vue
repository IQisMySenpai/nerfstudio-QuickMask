<script setup lang="ts">
import {computed, PropType} from "vue";
import {frameType} from "@/store/images";

const props = defineProps({
  index: {
    type: Number,
    required: true
  },
  frame: {
    type: Object as PropType<frameType>,
    required: true
  },
  active: {
    type: Boolean,
    default: false
  }
})

const index = computed(() => props.index)
const frame = computed(() => props.frame)
const active = computed(() => props.active)
</script>

<template>
<div
  :class="['pa-3', 'd-flex', 'ga-2', 'align-center', active ? 'bg-grey-darken-3' : '']"
>
  <v-img
    class="flex-0-0-100"
    :max-width="150"
    aspect-ratio="4/3"
    cover
    :src="`/api/image/${index}`"
  >
    <div
      v-if="frame.has_existing_mask || frame.rects.length"
      class="d-flex justify-center align-center ga-2 w-100 h-100 light_bg"
    >
      <v-btn
        v-if="frame.has_existing_mask"
        icon="mdi-filter"
        density="comfortable"
        color="warning"
      />
      <v-btn
        v-if="frame.rects.length"
        icon="mdi-check-bold"
        density="comfortable"
        color="success"
      />
    </div>
  </v-img>
  <div
    class="flex-1-1-100 d-flex align-center justify-center ga-1"
  >
    <span
      class="text-caption"
    >
      #
    </span>
    <span
      class="text-h6"
    >
      {{ index }}
    </span>
  </div>
</div>
</template>

<style scoped>
.light_bg {
  background-color: rgba(255, 255, 255, 0.5);
}
</style>
