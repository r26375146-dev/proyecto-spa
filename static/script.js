/* =========================================
   1. ANIMACIONES, EFECTOS Y RELOJ
   ========================================= */

document.addEventListener('DOMContentLoaded', function() {
    
    // A. El Reloj en Tiempo Real
    function actualizarReloj() {
        const elementoReloj = document.getElementById('real-time-clock');
        if(elementoReloj) {
            const ahora = new Date();
            let horas = ahora.getHours();
            let minutos = ahora.getMinutes();
            let segundos = ahora.getSeconds();
            let ampm = horas >= 12 ? 'PM' : 'AM';
            
            horas = horas % 12;
            horas = horas ? horas : 12; // La hora '0' debe ser '12'
            minutos = minutos < 10 ? '0' + minutos : minutos;
            segundos = segundos < 10 ? '0' + segundos : segundos;
            
            const horaTexto = horas + ':' + minutos + ':' + segundos + ' ' + ampm;
            elementoReloj.textContent = horaTexto;
        }
    }
    // Ejecutar el reloj cada segundo
    setInterval(actualizarReloj, 1000);
    actualizarReloj(); // Llamada inicial para que no aparezca en blanco

    // B. Efecto Pegajoso (Sticky) para la Barra de Navegación
    const navbar = document.getElementById('navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // C. Animación de revelado al hacer scroll (Intersection Observer)
    const revealElements = document.querySelectorAll('.reveal');
    
    const revealOptions = {
        threshold: 0.15,
        rootMargin: "0px 0px -50px 0px"
    };

    const revealOnScroll = new IntersectionObserver(function(entries, observer) {
        entries.forEach(entry => {
            if (!entry.isIntersecting) {
                return;
            } else {
                entry.target.classList.add('active');
                observer.unobserve(entry.target);
            }
        });
    }, revealOptions);

    revealElements.forEach(el => {
        revealOnScroll.observe(el);
    });
});


/* =========================================
   2. FUNCIONALIDAD DEL SISTEMA (MODALES)
   ========================================= */

const serviciosData = {
    'manicura': {
        icon: 'fas fa-hand-sparkles',
        title: 'Detalles de Manicura Spa Profundo',
        description: '💅 Nuestra Manicura Spa es una experiencia completa de cuidado. Incluye limpieza profunda de cutículas, exfoliación con sales florales, hidratación intensiva con aceites esenciales y un diseño coquette personalizado con acabado de alta gama. ¡Perfecto para brillar!',
        price: 'Desde $350 MXN (el precio final depende del diseño y técnica)'
    },
    'masaje': {
        icon: 'fas fa-spa',
        title: 'Inmersión en Masaje Relajante',
        description: '🌸 Disfruta de un masaje de 60 minutos diseñado para disipar el estrés. Utilizamos técnicas de relajación profunda, aromaterapia floral con aceites esenciales premium y música ambiental suave en un entorno de máxima elegancia. ¡Un oasis de paz!',
        price: 'Precio especial de apertura: $500 MXN'
    }
};

function abrirModal(servicioId) {
    const modal = document.getElementById('serviceModal');
    const modalDataContainer = document.getElementById('modalData');
    const servicio = serviciosData[servicioId];

    if (!servicio) return;

    modalDataContainer.innerHTML = `
        <i class="${servicio.icon} modal-icon" style="font-size: 3rem; color: #FF1493; margin-bottom: 15px;"></i>
        <h3 style="color: #C71585; font-family: 'Playfair Display', serif;">${servicio.title}</h3>
        <p style="color: #4A4A4A; line-height: 1.6;">${servicio.description}</p>
        <p class="modal-price" style="color: #FF1493; font-weight: bold; margin: 20px 0;"><strong>Valor:</strong> ${servicio.price}</p>
        <div class="modal-actions" style="display: flex; gap: 15px; justify-content: center; margin-top: 25px;">
            <button class="coquette-btn-secondary" onclick="cerrarModal()" style="width: auto;">Cerrar ❌</button>
            <a href="#reservas" onclick="cerrarModal()" class="coquette-btn-main">Agendar Cita 🎀</a>
        </div>
    `;

    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden'; 
}

function cerrarModal() {
    const modal = document.getElementById('serviceModal');
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
}

window.onclick = function(event) {
    const modales = document.querySelectorAll('.modal-overlay');
    modales.forEach(modal => {
        if (event.target == modal) {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    });
}
