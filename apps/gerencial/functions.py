def get_departamentos_filhos_recursivo(departamentos):
    """
    Retorna todos os IDs dos departamentos recebidos e de seus filhos recursivamente,
    sem gerar N+1 queries.
    """
    from apps.configuracoes.models import Departamento  # ajuste para seu app

    # Coletar todos os IDs iniciais
    ids_iniciais = [d.id for d in departamentos]

    # Buscar todos departamentos de uma vez
    todos = list(Departamento.objects.all().only('id', 'departamento_pai_id'))

    # Criar um mapa pai -> lista de filhos
    filhos_map = {}
    for dep in todos:
        filhos_map.setdefault(dep.departamento_pai_id, []).append(dep.id)

    # Percorrer recursivamente em memória
    ids = set()

    def collect(dep_id):
        if dep_id not in ids:
            ids.add(dep_id)
            for filho_id in filhos_map.get(dep_id, []):
                collect(filho_id)

    for dep_id in ids_iniciais:
        collect(dep_id)

    return list(ids)
