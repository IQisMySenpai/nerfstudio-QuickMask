<script setup lang="ts">
import PoseOverview from "@/components/PoseOverview.vue";
import {storeToRefs} from "pinia";
import {useImageStore} from "@/store/images";

const imagesStore = useImageStore();
const {frames, selected} = storeToRefs(imagesStore);
const {select} = imagesStore;
</script>

<template>
  <v-navigation-drawer
    v-if="frames"
  >
    <v-virtual-scroll
      class="w-100 h-100"
      :items="frames"
    >
      <template v-slot:default="{ item, index }">
        <v-divider
          v-if="index > 0"
        />
        <PoseOverview
          :index="index"
          :active="selected === index"
          :frame="item"
          @click="select(index)"
        />
      </template>
    </v-virtual-scroll>
  </v-navigation-drawer>
</template>

<style scoped>

</style>
