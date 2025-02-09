import {defineStore} from "pinia";
import {ref} from "vue";

export interface Rectangle  {
  x: number;
  y: number;
  width: number;
  height: number;
}

export const useCurrentImageStore = defineStore('currentImage', () => {
  const rectangles = ref<Rectangle[]>([]);
  const history = ref<Rectangle[]>([]);
  const canvas = ref<HTMLCanvasElement | null>(null);
  const forceRerender = ref<(() => void) | null>(null);

  function drawRectangle(rectangle: Rectangle) {
    if (!canvas.value) {
      return;
    }

    // Draw a square on the canvas
    const ctx = canvas.value.getContext('2d');
    if (!ctx) {
      return;
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

  function addRectangle(rectangle: Rectangle) {
    rectangles.value.push(rectangle);
    history.value = [];
    drawRectangle(rectangle);
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
  }

  return {
    rectangles,
    history,
    canvas,
    addRectangle,
    undoRectangle,
    redoRectangle,
    forceRerender
  }
});
