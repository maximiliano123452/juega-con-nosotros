$(document).ready(function () {
    
    // VALIDACIÓN DE REGISTRO
    $("#registroForm").submit(function (event) {
      event.preventDefault(); // Evita envío por defecto

      let nombre = $("#nombre").val().trim();
      let usuario = $("#usuario").val().trim();
      let email = $("#email").val().trim();
      let password = $("#password").val();
      let password2 = $("#password2").val();
      let fechaNacimiento = $("#fechaNacimiento").val();
      let rol = $("#rol").val();
      let terminos = $("#terminos").is(":checked");
      let formUrl = $("#registroForm").data("url");

      let errores = [];

      // VALIDAR CAMPOS VACÍOS
      if (!nombre || !usuario || !email || !password || !password2 || !fechaNacimiento || !rol) {
          errores.push("Todos los campos obligatorios deben completarse.");
      }

      // VALIDAR FORMATO EMAIL
      let emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(email)) {
          errores.push("El correo electrónico no es válido.");
      }

      // VALIDAR CONTRASEÑA COINCIDEN
      if (password !== password2) {
          errores.push("Las contraseñas no coinciden.");
      }

      // VALIDAR CONTRASEÑA SEGURA
      let passwordRegex = /^(?=.*[A-Z])(?=.*\d).{6,18}$/;
      if (!passwordRegex.test(password)) {
          errores.push("La contraseña debe tener entre 6 y 18 caracteres, incluir al menos un número y una letra mayúscula.");
      }

      // VALIDAR EDAD MÍNIMA (13 AÑOS)
      let fechaNac = new Date(fechaNacimiento);
      let hoy = new Date();
      let edad = hoy.getFullYear() - fechaNac.getFullYear();
      let mes = hoy.getMonth() - fechaNac.getMonth();
      if (mes < 0 || (mes === 0 && hoy.getDate() < fechaNac.getDate())) {
          edad--;
      }
      if (edad < 13) {
          errores.push("Debes tener al menos 13 años para registrarte.");
      }

      // VALIDAR TÉRMINOS
      if (!terminos) {
          errores.push("Debes aceptar los términos y condiciones.");
      }

      // VALIDAR ROL SELECCIONADO
      if (!rol || rol === "") {
          errores.push("Debes seleccionar un rol de usuario.");
      }

      // MOSTRAR ERRORES O ENVIAR FORMULARIO
      if (errores.length > 0) {
          let errorMessages = errores.join("<br>");
          $("#mensaje").html('<div class="alert alert-danger">' + errorMessages + '</div>');
      } else {
          // Si los datos son correctos, enviamos con AJAX
          let formData = {
              'nombre': nombre,
              'usuario': usuario,
              'email': email,
              'password': password,
              'password2': password2,
              'fechaNacimiento': fechaNacimiento,
              'direccion': $("#direccion").val(),
              'rol': rol,
              'terminos': terminos,
              'csrfmiddlewaretoken': $("input[name='csrfmiddlewaretoken']").val() // Incluir CSRF Token
          };

          $.ajax({
              url: formUrl, // URL que procesa la solicitud
              type: "POST",
              data: formData,
              success: function (response) {
                  // Mostrar mensaje de éxito o error
                  if (response.success) {
                      $("#mensaje").html('<div class="alert alert-success">' + response.message + '</div>');
                      setTimeout(function () {
                          window.location.href = "{% url 'login' %}"; // Redirigir al login después de éxito
                      }, 2000);
                  } else {
                      $("#mensaje").html('<div class="alert alert-danger">' + response.message + '</div>');
                  }
              },
              error: function (xhr, errmsg, err) {
                  // Si hubo un error en el servidor
                  $("#mensaje").html('<div class="alert alert-danger">Hubo un error al registrar el usuario: ' + errmsg + '</div>');
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