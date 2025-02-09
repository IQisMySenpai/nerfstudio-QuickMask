<script lang="ts" setup>
import {useCurrentImageStore} from "@/store/currentImage";
import {storeToRefs} from "pinia";

const currentImageStore = useCurrentImageStore();
const {rectangles, history} = storeToRefs(currentImageStore);
const {undoRectangle, redoRectangle} = currentImageStore;
</script>

<template>
  <v-app-bar
    density="comfortable"
  >
    <!--image="https://picsum.photos/1920/1080?random"-->
    <v-app-bar-title>
      <router-link
        :to="{ name: 'Home' }"
        class="text-decoration-none text-white"
      >
        NS QuickMask
      </router-link>
    </v-app-bar-title>
    <v-spacer/>
    <v-btn
      icon="mdi-undo"
      density="comfortable"
      :disabled="rectangles.length <= 0"
      @click="undoRectangle"
    />
    <v-btn
      icon="mdi-redo"
      density="comfortable"
      :disabled="history.length <= 0"
      @click="redoRectangle"
    />
  </v-app-bar>
</template>
