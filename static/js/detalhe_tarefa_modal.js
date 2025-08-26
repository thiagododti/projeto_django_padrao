function abrirModalDetalhes(idModal, idTarefa) {
    const modal = document.getElementById(idModal);
    const content = modal.querySelector(`#${idModal}Content`);

    if (modal && content) {
        // Abre a modal
        modal.classList.remove('hidden');
        modal.classList.add('flex');

        // Força reflow para animação
        void content.offsetWidth;

        content.classList.remove('scale-95', 'opacity-0');
        content.classList.add('scale-100', 'opacity-100');

        // Carrega os detalhes da tarefa via AJAX
        fetch(`/tarefas/detalhes_tarefa/${idTarefa}/`)
            .then(response => {
                if (!response.ok) throw new Error(`Erro ${response.status}`);
                return response.json();
            })
            .then(data => {
                if (data.error) {
                    alert(data.error);
                    return;
                }

                // Preenche os campos da modal
                document.getElementById('titulo_idmodal').textContent = data.titulo || '';
                document.getElementById('descricao_idmodal').textContent = data.descricao || '';
                document.getElementById('tipo_idmodal').textContent = data.tipo || '';
                document.getElementById('prioridade_idmodal').textContent = data.prioridade || '';
                document.getElementById('data_criacao_idmodal').textContent = data.data_criacao || '';
                document.getElementById('data_conclusao_idmodal').textContent = data.data_conclusao || '';
                document.getElementById('horas_estimadas_idmodal').textContent = data.horas_estimadas || '';
                document.getElementById('concluida_idmodal').textContent = data.concluida || '';
                document.getElementById('observacoes_idmodal').textContent = data.observacoes || '';
                document.getElementById('checkin_id_idmodal').textContent = data.checkin_id || '';
                document.getElementById('cliente_tarefa_idmodal').textContent = data.cliente_tarefa || '';
            })
            .catch(error => {
                console.error('Erro ao carregar detalhes da tarefa:', error);
                alert('Não foi possível carregar os detalhes da tarefa.');
            });
    }
}

