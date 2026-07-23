![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

````markdown
# Sistema de Senhas

Sistema desktop para gerenciar fila de atendimento com senhas normais e prioritárias.

## Como usar

1. Instale as dependências:
   pip install customtkinter pyttsx3 pypiwin32

2. Execute:
   python gui_app.py

## Funcionalidades

- Gerar senhas Normal e Prioritária
- Chamar próximo com voz e beep
- Tela para o cliente mostrar a senha atual
- Impressão de comprovante (térmica ou .txt)
- Salva os dados automaticamente
- Relatórios e estatísticas
- Ajustes de prefixo, som, tema e impressora

## Arquivos principais

- gui_app.py : Interface gráfica
- senhas.py : Lógica da fila
- banco.py : Salvar/carregar dados
- config.py : Configurações
- tts.py : Voz (Text-to-Speech)
- impressao.py : Impressão
- relatorio.py : Estatísticas
- logger.py : Logs de erro

## Gerar executável

pip install pyinstaller
pyinstaller --onefile --windowed --add-data "config.json;." gui_app.py

## Licença

MIT
