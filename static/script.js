/* =========================================
   1. ANIMACIONES, EFECTOS Y RELOJ
   ========================================= */

// FUNCIÓN DEL RELOJ (Blindada)
function iniciarReloj() {
    const elementoReloj = document.getElementById('real-time-clock');
    if (!elementoReloj) return; // Si no encuentra el reloj, se detiene
    
    function actualizar() {
        const ahora = new Date();
        let horas = ahora.getHours();
        let minutos = ahora.getMinutes();
        let segundos = ahora.getSeconds();
        let ampm = horas >= 12 ? 'PM' : 'AM';
        
        horas = horas % 12;
        horas = horas ? horas : 12; 
        minutos = minutos < 10 ? '0' + minutos : minutos;
        segundos = segundos < 10 ? '0' + segundos : segundos;
        
        elementoReloj.textContent = horas + ':' + minutos + ':' + segundos + ' ' + ampm;
    }
    
    actualizar(); // Ejecuta la hora inmediatamente al abrir la página
    setInterval(actualizar, 1000); // Actualiza cada segundo
}

document.addEventListener('DOMContentLoaded', function() {
    
    // Arrancamos el reloj
    iniciarReloj();

    // Efecto Pegajoso (Sticky) para la Barra de Navegación
    const navbar = document.getElementById('navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // Animación de revelado al hacer scroll
    const revealElements = document.querySelectorAll('.reveal');
    const revealOptions = {
        threshold: 0.15,
        rootMargin: "0px 0px -50px 0px"
    };

    const revealOnScroll = new IntersectionObserver(function(entries, observer) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
                observer.unobserve(entry.target);
            }
        });
    }, revealOptions);

    revealElements.forEach(el => revealOnScroll.observe(el));
});

/* =========================================
   2. FUNCIONALIDAD DEL SISTEMA (MODALES)
   ========================================= */
// (Aquí dejas el resto de tu código de los modales exactito como estaba)
