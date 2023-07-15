window.onload = function() {
  let hamburger = document.getElementById('hamburger');
  let menu = document.getElementById('menu');

  hamburger.addEventListener('click', function(){
    menu.classList.toggle('open');
    hamburger.innerHTML = menu.classList.contains('open') ? '&#10005;' : '&#9776;';
  });
};


