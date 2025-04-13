$(document).ready(function () {
    // LOGIN
    $('#loginForm').on('submit', function (e) {
        e.preventDefault();

        let email = $('#id_correo_electronico').val();
        let password = $('#id_contrasena').val();

        $.ajax({
            type: 'POST',
            url: '/login/ajax/',
            data: {
                'correo_electronico': email,
                'contrasena': password,
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function (response) {
                if (response.success) {
                    $('#mensaje-login').html(`<div class="alert alert-success" role="alert">${response.message}</div>`);
                    setTimeout(() => window.location.href = '/', 2000);
                } else {
                    $('#mensaje-login').html(`<div class="alert alert-danger" role="alert">${response.error}</div>`);
                }
            },
            error: function () {
                $('#mensaje-login').html(`<div class="alert alert-danger" role="alert">Ocurrió un error al iniciar sesión.</div>`);
            }
        });
    });
});