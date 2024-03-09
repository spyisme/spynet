// Function to generate a random RGB value
function randomColorValue() {
    return Math.floor(Math.random() * 256);
}

// Function to generate a random RGB color
function getRandomColor() {
    const r = randomColorValue();
    const g = randomColorValue();
    const b = randomColorValue();
    return `rgb(${r}, ${g}, ${b})`;
}

// Set random colors on page load
document.addEventListener('DOMContentLoaded', function () {
    setRandomColors();
});

// Function to set random colors
function setRandomColors() {
    const gradient = `linear-gradient(72deg, ${getRandomColor()} 0%, ${getRandomColor()} 40%, ${getRandomColor()} 100%)`;
    document.body.style.background = gradient;
}

// Change colors on page refresh
window.addEventListener('load', setRandomColors);