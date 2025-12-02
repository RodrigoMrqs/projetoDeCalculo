# Protótipo — Modelo 1 (Quadrático)

## Como rodar

1. python -m venv venv
2. Ativar o ambiente virtual
3. pip install -r requirements.txt
4. python app.py
5. Acessar http://127.0.0.1:5000/

## O que o sistema faz

- Recebe área total A e parâmetro theta.
- Para cada cultura, calcula L(A) = aA – bA².
- Exibe o lucro de cada cultura e indica a mais rentável.
- Salva o cenário em SQLite.
- Gera gráfico (seaborn + matplotlib).

## Observações

- PyCaret é usado apenas em demonstração opcional.
- Pode ser expandido para otimização multi-cultura.
