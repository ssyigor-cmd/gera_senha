![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

#Sistema de Gerenciamento de Senhas

Sistema desktop para controle de fila de atendimento, com suporte a senhas prioritárias, chamada por voz, impressão de comprovantes e tela dupla (operador + cliente).

---

## Funcionalidades

- Geração de senhas (Normal e Prioritária) com prefixos personalizáveis.
- Fila inteligente (prioritários atendidos antes dos normais).
- Chamada por voz (TTS) e sinal sonoro.
- Tela do cliente: última senha chamada e próximos 5.
- Impressão de comprovantes (térmica ou arquivo .txt).
- Persistência automática em JSON.
- Relatórios diários em .txt com estatísticas.
- Configurações ajustáveis: prefixos, som, voz, impressora, tema.
- Sistema de logs para diagnóstico.

---

## Como executar

1. Instale as dependências:
```bash
pip install customtkinter pyttsx3 pypiwin32
Execute:

bash
python gui_app.py
Configuração
O arquivo config.json gerado automaticamente permite ajustar:

Prefixos das senhas

Ativar/desativar som, voz, impressora

Nome da impressora

Tema (dark/light)

Compilando para .exe
bash
pip install pyinstaller
pyinstaller --onefile --windowed --add-data "config.json;." gui_app.py
Estrutura do projeto
gui_app.py – Interface principal

senhas.py – Lógica da fila

banco.py – Persistência de dados

config.py – Gerenciamento de configurações

tts.py – Síntese de voz

impressao.py – Impressão de comprovantes

relatorio.py – Geração de relatórios

logger.py – Sistema de logs

Licença
MIT
