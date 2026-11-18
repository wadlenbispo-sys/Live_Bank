# Live_Bank

Aplicacao bancaria web com backend em Python/Flask e interface em HTML/CSS.

## Executar

Instale as dependências do projeto:

```powershell
python -m pip install -r requirements.txt
```

Inicie o servidor na pasta do projeto:

```powershell
python app.py
```

Abra `http://127.0.0.1:5003` no navegador. Os dados ficam salvos em `dados.json`.

## Organizacao

- `app.py`: rotas Flask, validacoes e persistencia.
- `classes.py`: classes de dominio, incluindo `Cliente`, `Agencia` e os tipos de conta.
- `templates/`: paginas HTML.
- `static/css/style.css`: estilos da interface.

O sistema possui uma única agência: código `0001`, em Sergipe/SE. Todas as contas são vinculadas a ela.

Um cliente pode ter várias contas, mas cada conta pertence a um único cliente.
