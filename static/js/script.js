const observer = new IntersectionObserver((entries) => {

    entries.forEach((entry) => {
        console.log(entry)
        if(entry.isIntersecting) {
            entry.target.classList.add('show');
        }

    });

});


const hiddenElements = document.querySelectorAll('.hidden');
hiddenElements.forEach((el) => observer.observe(el));



document.addEventListener('DOMContentLoaded', function() {
  var cartContent = document.querySelector('.cart-content');
  var toggleButton = document.querySelector('.toggle-cart');

  toggleButton.addEventListener('click', function() {
    // Проверяем видимость содержимого корзины
    if(cartContent.style.display === 'none') {
      // Если содержимое скрыто, отображаем его
      cartContent.style.display = 'block';
      toggleButton.textContent = '-';
    } else {
      // Если содержимое отображается, скрываем его
      cartContent.style.display = 'none';
      toggleButton.textContent = '+';
    }
  });
});