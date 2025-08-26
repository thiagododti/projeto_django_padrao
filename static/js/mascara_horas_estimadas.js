document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("id_horas_estimadas");

    input.addEventListener("input", function () {
        let value = input.value.replace(/\D/g, ""); // remove tudo que não for número
        if (value.length > 6) value = value.slice(0, 6); // máximo 6 dígitos

        let formatted = "";
        if (value.length > 0) formatted = value.substring(0, 2);
        if (value.length > 2) formatted += ":" + value.substring(2, 4);
        if (value.length > 4) formatted += ":" + value.substring(4, 6);

        input.value = formatted;
    });

    // completa com zeros ao sair do campo
    input.addEventListener("blur", function () {
        let parts = input.value.split(":");

        // garante sempre 3 partes
        while (parts.length < 3) {
            parts.push("00");
        }

        // completa cada parte com 2 dígitos
        parts = parts.map(p => p.padStart(2, "0"));

        input.value = parts.join(":");
    });
});
