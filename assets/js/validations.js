function validarContacto() {
  var details = document.getElementById("details").value.trim();
  var email = document.getElementById("email").value.trim();
  var legal = document.getElementById("legal").checked;
  var missingFields = [];

  if (details === "") {
    missingFields.push("Descripción");
  }
  if (email === "") {
    missingFields.push("Email");
  }
  if (!legal) {
    missingFields.push("Declaración de responsabilidad");
  }

  if (missingFields.length > 0) {
    var message = "Error! Campos obligatorios sin completar:\n";
    message += missingFields.join("\n");
    alert(message);
    return false;
  }

  var messageOk =
    "¡Su consulta ha sido enviada con éxito! En breve le responderemos. Gracias";
  alert(messageOk);
  return true;
}

