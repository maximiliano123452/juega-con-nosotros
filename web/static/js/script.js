$(document).ready(function () {

    // RECUPERAR
    $('#recuperarForm').on('submit', function (e) {
        e.preventDefault();

        const email = $('#correo').val().trim();
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (!emailRegex.test(email)) {
            alert("Por favor, ingresa un correo válido.");
        } else {
            alert("Enlace de recuperación enviado a tu correo.");
            $('#recuperarForm')[0].reset();
        }
    });

    // PERFIL
    $('#perfilForm').on('submit', function (e) {
        e.preventDefault();

        const nombre = $('#nombre').val().trim();
        const usuario = $('#usuario').val().trim();
        const email = $('#email').val().trim();
        const direccion = $('#direccion').val().trim();
        const password = $('#password').val();
        const password2 = $('#password2').val();

        let errores = [];

        if (!nombre || !usuario || !email) {
            errores.push("Los campos obligatorios no pueden estar vacíos.");
        }

        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            errores.push("Correo electrónico inválido.");
        }

        if (password || password2) {
            if (password !== password2) {
                errores.push("Las contraseñas no coinciden.");
            }
            if (!/^(?=.*[A-Z])(?=.*\d).{6,18}$/.test(password)) {
                errores.push("La contraseña debe tener entre 6 y 18 caracteres, incluir al menos una mayúscula y un número.");
            }
        }

        if (errores.length > 0) {
            alert(errores.join("\n"));
        } else {
            alert("¡Cambios guardados correctamente!");
            $('#perfilForm')[0].reset();
        }
    });

});
