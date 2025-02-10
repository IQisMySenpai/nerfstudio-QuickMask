import {defineStore} from "pinia";
import {ref} from "vue";
import {useImageStore} from "@/store/images";

export interface Rectangle  {
  x: number;
  y: number;
  width: number;
  height: number;
  img_width: number;
  img_height: number;
}

export const useCurrentImageStore = defineStore('currentImage', () => {
  const imagesStore = useImageStore();

  const rectangles = ref<Rectangle[]>([]);
  const history = ref<Rectangle[]>([]);
  const canvas = ref<HTMLCanvasElement | null>(null);

  function drawRectangle(rectangle: Rectangle) {
    if (!canvas.value) {
      return;
    }

    // Draw a square on the canvas
    const ctx = canvas.value.getContext('2d');
    if (!ctx) {
      return;
    }

    if (rectangle.img_width !== canvas.value.width || rectangle.img_height !== canvas.value.height) {
      const scaleX = canvas.value.width / rectangle.img_width;
      const scaleY = canvas.value.height / rectangle.img_height;

      rectangle.x *= scaleX;
      rectangle.y *= scaleY;
      rectangle.width *= scaleX;
      rectangle.height *= scaleY;
      rectangle.img_width = canvas.value.width;
      rectangle.img_height = canvas.value.height;
    }

    ctx.fillStyle = 'rgba(0, 0, 255, 1)';
    ctx.fillRect(rectangle.x, rectangle.y, rectangle.width, rectangle.height);
  }

  function clearCanvas() {
    if (!canvas.value) {
      return;
    }

    const ctx = canvas.value.getContext('2d');
    if (!ctx) {
      return;
    }

    ctx.clearRect(0, 0, canvas.value.width, canvas.value.height);

    // The following lines fix a bug where the canvas would not clear
    ctx.fillStyle = 'rgba(0, 0, 0, 0)';
    ctx.fillRect(0, 0, canvas.value.width, canvas.value.height);
  }

  function drawAllRectangles() {
    rectangles.value.forEach((rectangle) => {
      drawRectangle(rectangle);
    });
  }

  function clearAndDrawAllRectangles() {
    clearCanvas();
    drawAllRectangles();
  }

  function clearRectangles() {
    rectangles.value = [];
    history.value = [];
    clearCanvas();
    save();
  }

  function addRectangle(x: number, y: number, width: number, height: number) {
    if (!canvas.value) {
      return;
    }

    const rectangle: Rectangle = {
      x,
      y,
      width,
      height,
      img_width: canvas.value.width,
      img_height: canvas.value.height,
    };

    rectangles.value.push(rectangle);
    history.value = [];
    drawRectangle(rectangle);
    save();
  }

  function undoRectangle() {
    if (rectangles.value.length <= 0) {
      return;
    }

    const lastRectangle = rectangles.value.pop();
    if (!lastRectangle) {
      return;
    }

    history.value.push(lastRectangle);

    clearAndDrawAllRectangles();
    save();
  }

  function redoRectangle() {
    if (history.value.length <= 0) {
      return;
    }

    const lastHistory = history.value.pop();
    if (!lastHistory) {
      return;
    }

    rectangles.value.push(lastHistory);
    drawRectangle(lastHistory);
    save();
  }

  function select(rects: Rectangle[]) {
    const current = rectangles.value;
    rectangles.value = rects;
    history.value = [];
    clearAndDrawAllRectangles();
    return current;
  }

  function save() {
    if (!canvas.value) {
      return;
    }

    const keepMask = imagesStore.frames![imagesStore.selected].has_existing_mask;
    const rects = rectangles.value;

    fetch(`http://localhost:8000/api/generate-mask/${imagesStore.selected}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        keep_mask: keepMask,
        rectangles: rects
      }),
    }).then(response => response.json()).then(data => {
      if (data.error) {
        console.error(data.error);
        return;
      }
    })
  }

  return {
    rectangles,
    history,
    canvas,
    addRectangle,
    undoRectangle,
    redoRectangle,
    clearRectangles,
    clearAndDrawAllRectangles,
    select,
    save,
  }
});
