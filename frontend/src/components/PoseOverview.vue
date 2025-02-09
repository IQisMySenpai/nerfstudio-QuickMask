<script setup lang="ts">

import {computed} from "vue";

const props = defineProps({
  index: {
    type: Number,
    required: true
  },
  active: {
    type: Boolean,
    default: false
  }
})

const index = computed(() => props.index)
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
    src="https://cdn.vuetifyjs.com/images/parallax/material.jpg"
  ></v-img>
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

</style>
