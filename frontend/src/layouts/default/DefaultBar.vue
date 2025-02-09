<script lang="ts" setup>
import {useCurrentImageStore} from "@/store/currentImage";
import {storeToRefs} from "pinia";

const currentImageStore = useCurrentImageStore();
const {rectangles, history} = storeToRefs(currentImageStore);
const {undoRectangle, redoRectangle, clearRectangles} = currentImageStore;
</script>

<template>
  <v-app-bar
    density="comfortable"
  >
    <v-app-bar-title>
      <v-avatar
        size="40"
        class="mr-2"
        :rounded="0"
        border="0"
      >
        <v-img
          src="/logo.png"
          alt="NS QuickMask Logo"
        />
      </v-avatar>
      <router-link
        :to="{ name: 'Home' }"
        class="text-decoration-none text-white"
      >
        NerfStudio QuickMask
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
    <v-btn
      icon="mdi-eraser"
      density="comfortable"
      @click="clearRectangles"
    />
  </v-app-bar>
</template>
