// Objeto con los datos profesionales de cada servicio
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

// Función para abrir la pantalla modal profesional
function abrirModal(servicioId) {
    const modal = document.getElementById('serviceModal');
    const modalDataContainer = document.getElementById('modalData');
    const servicio = serviciosData[servicioId];

    if (!servicio) return;

    // Llenar el modal con los datos
    modalDataContainer.innerHTML = `
        <i class="${servicio.icon} modal-icon"></i>
        <h3>${servicio.title}</h3>
        <p>${servicio.description}</p>
        <p class="modal-price"><strong>Valor:</strong> ${servicio.price}</p>
        <div class="modal-actions">
            <button class="btn-info secondary-btn" onclick="cerrarModal()">Cerrar</button>
            <a href="https://t.me/Spa_Rubi_bot" class="coquette-btn-main modal-btn">Agendar este servicio</a>
        </div>
    `;

    // Mostrar el modal
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden'; // Evitar scroll del fondo
}

// Función para cerrar la pantalla modal
function cerrarModal() {
    const modal = document.getElementById('serviceModal');
    modal.style.display = 'none';
    document.body.style.overflow = 'auto'; // Restaurar scroll del fondo
}

// Cerrar el modal al hacer clic fuera del contenido
window.onclick = function(event) {
    const modal = document.getElementById('serviceModal');
    if (event.target == modal) {
        cerrarModal();
    }
}
