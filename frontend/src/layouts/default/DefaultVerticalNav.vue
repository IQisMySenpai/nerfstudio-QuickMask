<script setup lang="ts">
import PoseOverview from "@/components/PoseOverview.vue";
import {ref} from "vue";

const selected = ref(0);
</script>

<template>
  <v-navigation-drawer>
    <v-virtual-scroll
      class="py-2 w-100 h-100"
      :items="['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30']"
    >
      <template v-slot:default="{ item, index }">
        <v-divider
          v-if="index > 0"
        />
        <PoseOverview
          :index="index"
          :active="selected === index"
          @click="selected = index"
        />
      </template>
    </v-virtual-scroll>
  </v-navigation-drawer>
</template>

<style scoped>

</style>
