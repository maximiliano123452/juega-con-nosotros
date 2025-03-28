$(document).ready(function () {
  $("#registroForm").submit(function (event) {
      event.preventDefault(); // EVITA ENVÍO POR DEFECTO

      let nombre = $("#nombre").val().trim();
      let usuario = $("#usuario").val().trim();
      let email = $("#email").val().trim();
      let password = $("#password").val();
      let password2 = $("#password2").val();
      let fechaNacimiento = $("#fechaNacimiento").val();
      let rol = $("#rol").val(); // ✅ NUEVO: Captura del rol
      let terminos = $("#terminos").is(":checked");

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
          alert(errores.join("\n"));
      } else {
          alert("Registro exitoso. ¡Bienvenido!");
          $("#registroForm")[0].reset();
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
});

