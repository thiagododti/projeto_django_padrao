function abrirModal(id, idTarefa = null) {
    const modal = document.getElementById(id);
    const content = modal.querySelector(`#${id}Content`);

    if (modal && content) {
        modal.classList.remove('hidden');
        modal.classList.add('flex');

        // Força reflow para ativar animação
        void content.offsetWidth;

        content.classList.remove('scale-95', 'opacity-0');
        content.classList.add('scale-100', 'opacity-100');

        // Se um ID de tarefa for fornecido, atualize o campo na modal
        if (idTarefa !== null) {
            const campoTarefa = modal.querySelector('[data-modal-tarefa-id]');
            if (campoTarefa) {
                campoTarefa.value = idTarefa;
            }
        }
    }
}


function fecharModal(id) {
    const modal = document.getElementById(id);
    const content = modal.querySelector(`#${id}Content`);

    if (modal && content) {
        content.classList.remove('scale-100', 'opacity-100');
        content.classList.add('scale-95', 'opacity-0');

        // Espera a animação terminar antes de esconder
        setTimeout(() => {
            modal.classList.remove('flex');
            modal.classList.add('hidden');
        }, 300); // deve bater com duration-300
    }
}