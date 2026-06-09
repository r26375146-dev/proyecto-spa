// Esperamos a que todo el HTML cargue
document.addEventListener('DOMContentLoaded', () => {
    
    // Buscamos el botón por su ID
    const botonCita = document.getElementById('btn-cita');

    // Le agregamos la acción al hacer clic
    botonCita.addEventListener('click', () => {
        alert("¡Hola! Gracias por elegir Glow & Elegance. En un momento te contactaremos para confirmar tu cita.");
    });

});