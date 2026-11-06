// frontend/js/app.js
document.getElementById('fraud-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    // 1. Capturar los valores del formulario HTML
    const monto = parseFloat(document.getElementById('monto').value);
    const dias = parseInt(document.getElementById('dias').value);
    const rucProv = document.getElementById('ruc_prov').value;
    const rucMuni = document.getElementById('ruc_muni').value;

    const placeholder = document.getElementById('placeholder-text');
    const resultCard = document.getElementById('result-card');
    const scoreBadge = document.getElementById('score-badge');
    const dictamenText = document.getElementById('dictamen-text');
    const centralidadText = document.getElementById('centralidad-text');

    const payload = {
        monto_adjudicado: monto,
        dias_proceso: dias,
        ruc_proveedor: rucProv,
        ruc_entidad: rucMuni
    };

    try {
        // 2. CONSTRUCCIÓN DE LA URL SEGÚN EL ENTORNO (PRODUCCIÓN VS LOCAL)
        let urlFinalBackend;

        // Si la web corre en localhost (Live Server), apunta al backend local (puerto 8000)
        if (window.location.hostname === "127.0.0.1" || window.location.hostname === "localhost") {
            const ipLocal = ["127", "0", "0", "1"].join(".");
            const puertoBackend = "8000";
            urlFinalBackend = `http://${ipLocal}:${puertoBackend}/api/predict`;
        } else {
            // Si la web corre en Render, usa la misma URL pública del servidor de forma dinámica
            urlFinalBackend = `${window.location.origin}/api/predict`;
        }

        // Hacer la petición HTTP POST
        const response = await fetch(urlFinalBackend, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error('El servidor respondió con un error al procesar el modelo matemático.');
        }

        const data = await response.json();

        // 3. Renderizar las respuestas en la interfaz web
        placeholder.classList.add('hidden');
        resultCard.classList.remove('hidden');

        const porcentajeRiesgo = (data.score_riesgo * 100).toFixed(2);
        scoreBadge.innerText = `${porcentajeRiesgo}%`;

        scoreBadge.className = "badge";

        if (data.es_anomalo || porcentajeRiesgo > 65) {
            scoreBadge.classList.add('danger');
            dictamenText.innerHTML = `<span class="txt-danger">🚨 ALERTA CRÍTICA:</span> Se detectaron patrones altamente coincidentes con fraccionamiento u acaparamiento de órdenes. Inspección prioritaria recomendada.`;
        } else {
            scoreBadge.classList.add('success');
            dictamenText.innerHTML = `<span class="txt-success">✅ COMPORTAMIENTO NORMAL:</span> Los parámetros se sitúan dentro de las densidades promedio del mercado SEACE.`;
        }

        const porcentajeCentralidad = (data.centralidad_proveedor * 100).toFixed(2);
        centralidadText.innerText = `${porcentajeCentralidad}% de acaparamiento estructural en el grafo histórico de la red municipal.`;

    } catch (error) {
        alert('Ocurrió un error al procesar el análisis: ' + error.message);
    }
});
