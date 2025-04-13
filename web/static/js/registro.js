$(document).ready(function () {
    $('#registroForm').on('submit', function (e) {
        e.preventDefault();
        $('.error-text').text('');
        $('#mensaje').html('');

        let errores = {};

        let nombreCompleto = $('#id_nombre_completo').val().trim();
        let nombreUsuario = $('#id_nombre_usuario').val().trim();
        let email = $('#id_correo_electronico').val().trim();
        let contrasena = $('#id_contrasena').val();
        let repetirContrasena = $('#id_repetir_contrasena').val();
        let fechaNacimiento = $('#id_fecha_nacimiento').val();
        let rol = $('#id_rol').val();
        let terminos = $('#id_terminos').is(':checked');

        if (!nombreCompleto) errores.nombre_completo = "Este campo es obligatorio.";
        if (!nombreUsuario) errores.nombre_usuario = "Este campo es obligatorio.";
        if (!email) {
            errores.correo_electronico = "Este campo es obligatorio.";
        } else {
            let emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) errores.correo_electronico = "Correo electrónico inválido.";
        }

        if (!contrasena) {
            errores.contrasena = "Este campo es obligatorio.";
        } else {
            let contrasenaRegex = /^(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{6,18}$/;
            if (!contrasenaRegex.test(contrasena)) {
                errores.contrasena = "Debe tener 6-18 caracteres, incluir una mayúscula y un número.";
            }
        }

        if (!repetirContrasena) {
            errores.repetir_contrasena = "Este campo es obligatorio.";
        } else if (contrasena !== repetirContrasena) {
            errores.repetir_contrasena = "Las contraseñas no coinciden.";
        }

        if (!fechaNacimiento) {
            errores.fecha_nacimiento = "Este campo es obligatorio.";
        } else {
            let hoy = new Date();
            let nacimiento = new Date(fechaNacimiento);
            let edad = hoy.getFullYear() - nacimiento.getFullYear();
            let m = hoy.getMonth() - nacimiento.getMonth();
            if (m < 0 || (m === 0 && hoy.getDate() < nacimiento.getDate())) edad--;
            if (edad < 13) errores.fecha_nacimiento = "Debes tener al menos 13 años.";
        }

        if (!rol) errores.rol = "Este campo es obligatorio.";
        if (!terminos) errores.terminos = "Debes aceptar los términos.";

        if (Object.keys(errores).length > 0) {
            for (let campo in errores) {
                $('#error-' + campo).text(errores[campo]);
            }
        } else {
            $.ajax({
                type: 'POST',
                url: $(this).data('url'),
                data: $(this).serialize(),
                success: function (response) {
                    if (response.success) {
                        $('#mensaje').html(`<div class="alert alert-success">¡Registro Exitoso! <br>Serás redirigido al inicio de sesión</div>`);
                        $('#registroForm')[0].reset();
                        setTimeout(() => window.location.href = "/login/", 3000);
                    } else {
                        $('#mensaje').html(`<div class="alert alert-danger">${response.error}</div>`);
                    }
                },
                error: function () {
                    $('#mensaje').html(`<div class="alert alert-danger">Ocurrió un error al registrar. Intenta de nuevo.</div>`);
                }
            });
        }
    });
});
