// JavaScript pour afficher les images une par une
let currentImageIndex = 0;
const images = document.querySelectorAll('.ad-images');

function showNextImage() {
    images[currentImageIndex].classList.remove('active');
    currentImageIndex = (currentImageIndex + 1) % images.length;
    images[currentImageIndex].classList.add('active');
}

setInterval(showNextImage, 3000); // Change d'image toutes les 3 secondes

// JavaScript pour le carrousel des catégories
const categoriesContainer = document.querySelector('.categories');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
let scrollAmount = 0;
const scrollStep = 100; // Ajustez la valeur selon vos besoins

prevBtn.addEventListener('click', () => {
    categoriesContainer.scrollBy({
        left: -scrollStep,
        behavior: 'smooth'
    });
});

nextBtn.addEventListener('click', () => {
    categoriesContainer.scrollBy({
        left: scrollStep,
        behavior: 'smooth'
    });
});
