<script lang="ts" setup>
import DefaultBar from './DefaultBar.vue'
import DefaultView from './DefaultView.vue'
import DefaultVerticalNav from "@/layouts/default/DefaultVerticalNav.vue";
import GlobalKeyboardHandler from "@/components/GlobalKeyboardHandler.vue";
</script>


<template>
  <v-app>
    <DefaultBar />
    <DefaultVerticalNav />

    <DefaultView />
    <GlobalKeyboardHandler />
  </v-app>
</template>
