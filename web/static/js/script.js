$(document).ready(function () {
    
    $('#registroForm').on('submit', function (e) {
        e.preventDefault();

        // Limpiar errores anteriores
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

        // Validaciones
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

        // Mostrar errores
        if (Object.keys(errores).length > 0) {
            for (let campo in errores) {
                $('#error-' + campo).text(errores[campo]);
            }
        } else {
            // Si no hay errores, enviar por AJAX
            $.ajax({
                type: 'POST',
                url: $(this).data('url'),
                data: $(this).serialize(),
                success: function (response) {
                    $('#mensaje').html('<div class="alert alert-success">¡Registro Exitoso! <br>Serás Redirigido al Inicio de Sesión</div>');
                    $('#registroForm')[0].reset();
                
                    // Redirigir al login luego de 3 segundos
                    setTimeout(function () {
                        window.location.href = "/login/";
                    }, 3000);
                },
                error: function () {
                    $('#mensaje').html('<div class="alert alert-danger">Ocurrió un error al registrar. Intenta de nuevo.</div>');
                }
            });
        }
    });
  
    // VALIDACIÓN DE LOGIN
    $("#loginForm").submit(function (event) {
        event.preventDefault();
  
        let email = $("#emailLogin").val().trim();
        let password = $("#passwordLogin").val();
        let errores = [];
  
        // VALIDAR EMAIL
        let emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            errores.push("El correo electrónico no es válido.");
        }
  
        // VALIDAR CONTRASEÑA
        if (password.length < 6) {
            errores.push("La contraseña debe tener al menos 6 caracteres.");
        }
  
        if (errores.length > 0) {
            alert(errores.join("\n"));
        } else {
            alert("Inicio de sesión exitoso.");
            $("#loginForm")[0].reset();
        }
    });
  
    // Validación de recuperar.html

    $("#recuperarForm").submit(function (e) {
          e.preventDefault();
          const email = $("#correo").val().trim();
          const emailRegex = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;
          
          if (!emailRegex.test(email)) {
            alert("Por favor, ingresa un correo válido.");
          } else {
            alert("Enlace de recuperación enviado a tu correo.");
            $("#recuperarForm")[0].reset();
          }
    });

    // Validación de perfil.html
    $("#perfilForm").submit(function (e) {
        e.preventDefault();

        const nombre = $("#nombre").val().trim();
        const usuario = $("#usuario").val().trim();
        const email = $("#email").val().trim();
        const direccion = $("#direccion").val().trim();
        const password = $("#password").val();
        const password2 = $("#password2").val();

        let errores = [];

        if (!nombre || !usuario || !email) {
          errores.push("Los campos obligatorios no pueden estar vacíos.");
        }

        const emailRegex = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;
        if (!emailRegex.test(email)) {
          errores.push("Correo electrónico inválido.");
        }

        if (password || password2) {
          if (password !== password2) {
            errores.push("Las contraseñas no coinciden.");
          }
          if (!/^(?=.*[A-Z])(?=.*\\d).{6,18}$/.test(password)) {
            errores.push("La contraseña debe tener entre 6 y 18 caracteres, incluir al menos una mayúscula y un número.");
          }
        }

        if (errores.length > 0) {
          alert(errores.join("\\n"));
        } else {
          alert("¡Cambios guardados correctamente!");
          $("#perfilForm")[0].reset();
        }
      });




});