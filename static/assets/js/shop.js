document.addEventListener('DOMContentLoaded', (event) => {
    const modal = new bootstrap.Modal(document.getElementById('productModal'));
    
    document.querySelectorAll('.btn-primary').forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            
            const card = this.closest('.card');
            const title = card.querySelector('.card-title').innerText;
            const price = card.querySelector('.card-text').innerText;
            const imageSrc = card.querySelector('img').src;
            
            document.getElementById('productModalLabel').innerText = title;
            document.getElementById('productModalPrice').innerText = price;
            document.getElementById('productModalImage').src = imageSrc;
            
            modal.show();
        });
    });
});