const slider = document.querySelector('.slider');
const prevButton = document.querySelector('.prev-button');
const nextButton = document.querySelector('.next-button');
const slideWidth = document.querySelector('.image-widget').offsetWidth;
let currentPosition = 0;

prevButton.addEventListener('click', () => {
  currentPosition += slideWidth;
  if (currentPosition > 0) {
    currentPosition = -(slideWidth * (slider.children.length - 1));
  }
  slider.style.transform = `translateX(${currentPosition}px)`;
});

nextButton.addEventListener('click', () => {
  currentPosition -= slideWidth;
  if (currentPosition < -(slideWidth * (slider.children.length - 1))) {
    currentPosition = 0;
  }
  slider.style.transform = `translateX(${currentPosition}px)`;
});