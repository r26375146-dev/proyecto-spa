// Función para mostrar los detalles de los servicios
function mostrarInfo(servicio) {
    if(servicio === 'manicura') {
        alert("💅 Nuestra Manicura Spa incluye limpieza profunda, exfoliación y diseño coquette personalizado. ¡Precio desde $350!");
    } else if (servicio === 'masaje') {
        alert("🌸 Masaje de 60 minutos con aromaterapia floral y música ambiental. ¡Precio especial de apertura: $500!");
    }
}

// Efecto interactivo al pasar el ratón sobre los botones
const botones = document.querySelectorAll('.coquette-btn, .btn-info');
botones.forEach(btn => {
    btn.addEventListener('mouseover', () => {
        btn.style.transform = 'scale(1.05)';
        btn.style.transition = '0.3s';
    });
    btn.addEventListener('mouseout', () => {
        btn.style.transform = 'scale(1)';
    });
});
