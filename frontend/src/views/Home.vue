<script lang="ts" setup>
import ImageEditor from "@/components/ImageEditor.vue";
import {storeToRefs} from "pinia";
import {useImageStore} from "@/store/images";
import {ref} from "vue";

const imagesStore = useImageStore();
const {frames, dataset_path} = storeToRefs(imagesStore);
const {setDataset} = imagesStore;

const current_path = ref<string>("");
const makeSafetyCopy = ref<boolean>(true);
</script>

<template>
  <ImageEditor
    v-if="frames && dataset_path"
  />
  <div
    class="d-flex justify-center align-center w-100 h-100"
    v-else
  >
    <v-card>
      <v-card
        width="500"
      >
        <v-card-title>
          Load Nerfstudio Dataset
        </v-card-title>
        <v-card-text>
          <v-text-field
            v-model="current_path"
            label="Dataset Path"
            variant="outlined"
            suffix="/transforms.json"
          />
          <v-switch
            v-model="makeSafetyCopy"
            label="Make a safety copy of current transform and masks"
            color="primary"
          />
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn
            color="primary"
            variant="elevated"
            @click="setDataset(current_path, makeSafetyCopy)"
          >
            Load
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-card>
  </div>
</template>

<style scoped>
</style>
