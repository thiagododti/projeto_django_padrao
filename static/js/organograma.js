// Base e tamanho do node
OrgChart.templates.myTemplate = Object.assign({}, OrgChart.templates.ana);
OrgChart.templates.myTemplate.size = [280, 180];

// Elementos estáticos do cartão
OrgChart.templates.myTemplate.node = `
  <!-- Card background -->
  <rect x="0" y="0" width="280" height="180" rx="12" ry="12" fill="#ffffff" stroke="#e2e8f0" stroke-width="2"></rect>

  <!-- Header -->
  <rect x="0" y="0" width="280" height="50" rx="12" ry="12" fill="#3b82f6"></rect>
  <rect x="0" y="38" width="280" height="12" fill="#3b82f6"></rect>

  <!-- Label "Supervisores:" -->
  <text x="20" y="75" fill="#374151" font-family="Arial, sans-serif" font-size="12" font-weight="bold">
    Supervisores:
  </text>

  <!-- Faixa inferior -->
  <rect x="0" y="170" width="280" height="10" rx="0" ry="0" fill="#e5e7eb"></rect>
`;

// Campos dinâmicos (agora sim {val} funciona)
OrgChart.templates.myTemplate.field_0 =
    '<text x="140" y="28" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="16" font-weight="bold">{val}</text>';

OrgChart.templates.myTemplate.field_1 =
    '<text x="30" y="95" fill="#4b5563" font-family="Arial, sans-serif" font-size="11">{val}</text>';

OrgChart.templates.myTemplate.field_2 =
    '<text x="30" y="110" fill="#4b5563" font-family="Arial, sans-serif" font-size="11">{val}</text>';

OrgChart.templates.myTemplate.field_3 =
    '<text x="30" y="125" fill="#4b5563" font-family="Arial, sans-serif" font-size="11">{val}</text>';
OrgChart.templates.myTemplate.field_4 =
    '<text x="30" y="125" fill="#4b5563" font-family="Arial, sans-serif" font-size="11">{val}</text>';
OrgChart.templates.myTemplate.field_5 =
    '<text x="30" y="125" fill="#4b5563" font-family="Arial, sans-serif" font-size="11">{val}</text>';
OrgChart.templates.myTemplate.field_6 =
    '<text x="30" y="125" fill="#4b5563" font-family="Arial, sans-serif" font-size="11">{val}</text>';

OrgChart.templates.myTemplate.field_10 =
    '<text x="240" y="160" text-anchor="middle" fill="#6b7280" font-family="Arial, sans-serif" font-size="10">Membros: {val}</text>';

var chart = new OrgChart(document.getElementById("tree"), {
    mouseScroll: OrgChart.action.none,
    template: "myTemplate",
    enableSearch: true,
    layout: OrgChart.treeRightOffset,
    collapse: {
        level: 2,
    },
    toolbar: {
        zoom: true,
        fit: true,
        expandAll: true,
    },
    keyNavigation: {
        focusId: 2,
    },
    nodeMouseClick: OrgChart.action.none,
    nodeBinding: {
        field_0: "name",
        field_1: "sup_1",
        field_2: "sup_2",
        field_3: "sup_3",
        field_4: "sup_4",
        field_5: "sup_5",
        field_6: "sup_6",
        field_10: "total_membros",
    },
});
fetch("/organograma/json/")
    .then((response) => response.json())
    .then((data) => {
        chart.load(data);
    });

chart.onNodeClick(async function (args) {
    const nodeId = args.node.id;
    console.log("Buscando membros do departamento:", nodeId);

    try {
        const response = await fetch(`/organograma/membros/${nodeId}/`);
        if (!response.ok) throw new Error("Erro ao buscar dados");

        const data = await response.json();

        const modalId = "membrosModal";
        const modal = document.getElementById(modalId);
        const modalContent = modal.querySelector(`#${modalId}Content`);
        const closeBtns = modal.querySelectorAll("button");

        modalContent.querySelector("h2").textContent = data.departamento;

        // Limpar conteúdo anterior
        modalContent.querySelector("p").innerHTML = "";

        /// Supervisores com flex-wrap
        if (data.supervisores.length > 0) {
            const supervisoresHTML = data.supervisores.map(sup => `
        <div class="flex flex-col items-center mb-4 mr-4 break-words w-32">
            ${sup.photo_url ?
                    `<img src="${sup.photo_url}" alt="${sup.first_name}" class="w-16 h-16 rounded-full mb-2">` :
                    `<div class="w-16 h-16 flex items-center justify-center rounded-full bg-gray-200 text-gray-600 mb-2">
                    <span class="material-icons">person</span>
                </div>`
                }
            <div class="text-center w-full">
                <div class="font-semibold text-gray-800 text-sm">${sup.first_name} ${sup.last_name}</div>
                <div class="text-gray-500 text-xs break-words">${sup.email}</div>
            </div>
        </div>
    `).join('');

            modalContent.querySelector("p").innerHTML += `
        <h3 class="font-semibold text-gray-700 mt-4 mb-2">Supervisores:</h3>
        <div class="flex flex-wrap">
            ${supervisoresHTML}
        </div>
    `;
        }

        // Membros com flex-wrap
        if (data.membros.length > 0) {
            const membrosHTML = data.membros.map(mem => `
        <div class="flex flex-col items-center mb-4 mr-4 break-words w-32">
            ${mem.photo_url ?
                    `<img src="${mem.photo_url}" alt="${mem.first_name}" class="w-16 h-16 rounded-full mb-2">` :
                    `<div class="w-16 h-16 flex items-center justify-center rounded-full bg-gray-200 text-gray-600 mb-2">
                    <span class="material-icons">person</span>
                </div>`
                }
            <div class="text-center w-full">
                <div class="font-semibold text-gray-800 text-sm">${mem.first_name} ${mem.last_name}</div>
                <div class="text-gray-500 text-xs break-words">${mem.email}</div>
            </div>
        </div>
    `).join('');

            modalContent.querySelector("p").innerHTML += `
        <h3 class="font-semibold text-gray-700 mt-4 mb-2">Membros:</h3>
        <div class="flex flex-wrap">
            ${membrosHTML}
        </div>
    `;
        }

        abrirModal(modalId);
        closeBtns.forEach((btn) =>
            btn.addEventListener("click", () => fecharModal(modalId))
        );
    } catch (error) {
        console.error(error);
        alert("Não foi possível carregar os membros do departamento.");
    }
});
