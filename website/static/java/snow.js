// Snow.js

const IMAGE_COUNT = 3;

// Image URLs
const imageUrls = [
  'https://pbs.twimg.com/media/EXI1HDEWsAYiP9_.jpg',
  'https://pbs.twimg.com/media/EXI1HDEWsAYiP9_.jpg',

  'https://pbs.twimg.com/media/EXI1HDEWsAYiP9_.jpg',

];

function startAnimation() {
  const CANVAS_WIDTH = window.innerWidth;
  const CANVAS_HEIGHT = window.innerHeight;
  const MIN = 0;
  const MAX = CANVAS_WIDTH;

  const canvas = document.getElementById("canvas");
  const ctx = canvas.getContext("2d");

  canvas.width = CANVAS_WIDTH;
  canvas.height = CANVAS_HEIGHT;

  function clamp(number, min = MIN, max = MAX) {
    return Math.max(min, Math.min(number, max));
  }

  function random(factor = 1) {
    return Math.random() * factor;
  }

  // All the properties for ImageObject
  class ImageObject {
    width = 0;
    height = 0;
    x = 0;
    y = 0;
    vx = 0;
    vy = 0;
    img = new Image();

    constructor(ctx, imageUrl) {
      this.ctx = ctx;
      this.img.src = imageUrl;
      this.reset();
    }

    draw() {
      this.ctx.drawImage(this.img, this.x, this.y, this.width, this.height);
    }

    reset() {
      this.width = 50; // Set the width of your image
      this.height = 50; // Set the height of your image
      this.x = random(CANVAS_WIDTH - this.width);
      this.y = random(CANVAS_HEIGHT - this.height);
      this.vx = clamp((Math.random() - 0.5) * 0.4, -0.4, 0.4);
      this.vy = clamp(random(1.5), 0.1, 0.8);
    }
  }

  // Array for storing all the generated image objects
  let images = [];

  // Generate image objects
  for (let i = 0; i < IMAGE_COUNT; i++) {
    images.push(new ImageObject(ctx, imageUrls[i]));
  }

  // Clear canvas
  function clearCanvas() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
  }

  // start and end coordinates of canvas
  let canvasOffset = {
    x0: ctx.canvas.offsetLeft,
    y0: ctx.canvas.offsetTop,
    x1: ctx.canvas.offsetLeft + ctx.canvas.width,
    y1: ctx.canvas.offsetTop + ctx.canvas.height
  };

  function animate() {
    clearCanvas();

    images.forEach((e) => {
      // reset the image if it collides on the border
      if (
        e.x <= canvasOffset.x0 ||
        e.x + e.width >= canvasOffset.x1 ||
        e.y <= canvasOffset.y0 ||
        e.y + e.height >= canvasOffset.y1
      ) {
        e.reset();
      }

      // Move image
      e.x += e.vx;
      e.y += e.vy;
      e.draw();
    });

    requestAnimationFrame(animate);
  }

  animate();
}

startAnimation();

window.addEventListener("resize", startAnimation);
