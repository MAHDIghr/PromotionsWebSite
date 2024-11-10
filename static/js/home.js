document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded and parsed');
    
    const products = document.querySelectorAll('.product');
    
    products.forEach(product => {
        product.addEventListener('mouseover', () => {
            product.style.transform = 'scale(1.05)';
            product.style.boxShadow = '0 10px 20px rgba(0,0,0,0.2)';
        });

        product.addEventListener('mouseout', () => {
            product.style.transform = 'scale(1)';
            product.style.boxShadow = '0 4px 8px rgba(0,0,0,0.1)';
        });

        // Carousels
        const carousels = product.querySelectorAll('.carousel');
        
        carousels.forEach(carousel => {
            let currentIndex = 0;
            const items = carousel.querySelectorAll('.carousel-item');
            const totalItems = items.length;
            const nextButton = carousel.querySelector('.carousel-control.next');
            const prevButton = carousel.querySelector('.carousel-control.prev');
            
            function showItem(index) {
                items.forEach((item, i) => {
                    item.classList.toggle('active', i === index);
                });
            }
            
            function nextItem() {
                currentIndex = (currentIndex + 1) % totalItems;
                showItem(currentIndex);
            }
            
            function prevItem() {
                currentIndex = (currentIndex - 1 + totalItems) % totalItems;
                showItem(currentIndex);
            }
            
            nextButton.addEventListener('click', nextItem);
            prevButton.addEventListener('click', prevItem);
            
            showItem(currentIndex);
        });
    });
});
