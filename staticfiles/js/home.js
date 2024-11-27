// JavaScript pour afficher les images une par une
let currentImageIndex = 0;
const images = document.querySelectorAll('.ad-images');

function showNextImage() {
    images[currentImageIndex].classList.remove('active');
    currentImageIndex = (currentImageIndex + 1) % images.length;
    images[currentImageIndex].classList.add('active');
}

setInterval(showNextImage, 3000); // Change d'image toutes les 3 secondes

