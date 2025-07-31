# Projeto Django Padrão

## Descrição

Este é um projeto inicial em Django desenvolvido para facilitar a inicialização de estudos ou projetos reais. A estrutura foi organizada de forma a suportar o desenvolvimento de aplicações robustas, com uma arquitetura bem definida.

## Características Principais

- **Estrutura Organizada**: Todos os apps do projeto estão concentrados na pasta `apps`, evitando a dispersão de pastas na raiz.

- **App de Configurações**: Um aplicativo dedicado para armazenar configurações do projeto, permitindo a personalização de cores através de valores hexadecimais e seletor de cores, tudo integrado ao Django Admin.

- **Extensão de Usuário**: Implementação de um app que estende o modelo de usuário padrão do Django, permitindo adicionar atributos personalizados.

- **Configuração com .env**: O projeto utiliza variáveis de ambiente para armazenar tokens e configurações de debug de forma segura.

## Instalação

1. Clone o repositório:
    ```
    git clone https://github.com/seu-usuario/projeto_django_padrao.git
    cd projeto_django_padrao
    ```

2. Crie e ative um ambiente virtual:
    ```
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```

3. Instale as dependências:
    ```
    pip install -r requirements.txt
    ```

4. Configure o arquivo .env com suas variáveis de ambiente:
    ```
    SECRET_KEY=sua_chave_secreta
    DEBUG=True
    ```

5. Execute as migrações:
    ```
    python manage.py migrate
    ```

6. Inicie o servidor:
    ```
    python manage.py runserver
    ```

## Estrutura do Projeto

```
projeto_django_padrao/
├── apps/
│   ├── configuracoes/  # App para configurações e personalização do projeto
│   ├── usuarios/       # App para extensão do modelo de usuário
│   └── ...
├── projeto_django_padrao/  # Configurações principais do projeto
└── ...
```

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests com melhorias.

## Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).