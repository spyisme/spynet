// Snow.js

const IMAGE_COUNT = 300;

// Image URL
const imageUrl = 'https://cdn.discordapp.com/attachments/941430155346345984/1215046527018598450/EXI1HDEWsAYiP9___1_-removebg-preview.png?ex=65fb5342&is=65e8de42&hm=2d5b156cc4e7084fae4ec0ca95ebbdce5bd484071b999aaaa1e5002730c3c321&';

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
    size = 20; // Set the size of your image
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
      this.ctx.drawImage(this.img, this.x, this.y, this.size, this.size);
    }

    reset() {
      this.x = random(CANVAS_WIDTH - this.size);
      this.y = random(CANVAS_HEIGHT - this.size);
      this.vx = clamp((Math.random() - 0.5) * 2, -2, 2);
      this.vy = clamp(random(3), 1, 3);
    }
  }

  // Array for storing all the generated image objects
  let images = [];

  // Generate image objects
  for (let i = 0; i < IMAGE_COUNT; i++) {
    images.push(new ImageObject(ctx, imageUrl));
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
      // reset the image if it goes off the canvas
      if (
        e.x <= canvasOffset.x0 ||
        e.x + e.size >= canvasOffset.x1 ||
        e.y <= canvasOffset.y0 ||
        e.y + e.size >= canvasOffset.y1
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
