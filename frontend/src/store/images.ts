import {defineStore} from "pinia";
import {ref} from "vue";
import {Rectangle, useCurrentImageStore} from "@/store/currentImage";

export interface frameType {
  has_existing_mask: boolean,
  rects: Rectangle[],
}

export const useImageStore = defineStore('image', () => {
  const currentImageStore = useCurrentImageStore();
  const dataset_path = ref<string | null>(null);
  const image_count = ref<null | number>(null);
  const frames = ref<null | frameType[]>(null);
  const selected = ref(0);

  function loadFromData(data: {
    path: string,
    framecount: number,
    frames_have_masks: boolean[],
  }) {
    selected.value = 0;
    dataset_path.value = data.path;
    image_count.value = data.framecount;
    frames.value = data.frames_have_masks.map((frame: boolean) => {
      return {
        has_existing_mask: frame,
        rects: [],
      };
    });
  }

  function setDataset(path: string, makeSafetyCopy: boolean = true) {
    fetch('http://localhost:8000/api/set-dataset-path', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        path,
        makeSafetyCopy,
      }),
    }).then(response => response.json()).then(data => {
      if (data.error) {
        console.error(data.error);
        return;
      }

      loadFromData(data);
    })
  }

  function loadDataset() {
    fetch('http://localhost:8000/api/current-dataset', {
      method: 'POST',
    }).then(response => response.json()).then(data => {
      if (data.error) {
        console.error(data.error);
        return;
      }

      loadFromData(data);
    });
  }

  function select(index: number) {
    if (index === selected.value) {
      return;
    }
    frames.value![selected.value].rects = currentImageStore.select(frames.value![index].rects || []);
    selected.value = index;
  }

  function removeExistingMask() {
    frames.value![selected.value].has_existing_mask = false;
  }

  loadDataset();

  return {
    dataset_path,
    image_count,
    frames,
    selected,
    setDataset,
    loadDataset,
    removeExistingMask,
    select,
  };
});
