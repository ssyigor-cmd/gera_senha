# Sistema de Gerenciamento de Senhas

Sistema desktop para controle de fila de atendimento, com suporte a **senhas prioritárias**, **chamada por voz (TTS)**, **impressão de comprovantes**, **persistência de dados** e **dual-screen** (painel do operador + tela do cliente).

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 📋 Funcionalidades

- ✅ **Geração de senhas** (Normal e Prioritária) com prefixos personalizáveis.
- ⭐ **Fila inteligente**: Prioritários sempre atendidos antes dos normais, mantendo ordem de chegada entre eles.
- 📢 **Chamada por voz (TTS)**: Anuncia a senha em português (configurável).
- 🔔 **Sinal sonoro (Beep)** ao chamar o próximo.
- 🖥️ **Tela dupla**: Painel de controle para o operador + tela de exibição para o cliente (última senha e próximos).
- 🖨️ **Impressão de comprovante**: Suporte a impressoras térmicas Windows (fallback para arquivo `.txt`).
- 💾 **Persistência automática**: Dados salvos em JSON a cada ação, com backup automático em caso de corrupção.
- 📊 **Relatórios e Estatísticas**: Relatórios diários em `.txt` com totais, distribuição por tipo, horários e tempo médio de espera.
- ⚙️ **Configurações flexíveis**: Prefixos, som, voz, impressora, tema (Dark/Light) e **nome do estabelecimento** (personalizável).
- 📝 **Sistema de Logs**: Registro detalhado de ações e erros no arquivo `app.log`.

---

## 🖥️ Capturas de Tela (Sugestão)

> *Adicione aqui imagens do sistema em execução.*

---

## 🚀 Como Executar

### 📦 Pré-requisitos
- Python 3.8 ou superior.
- (Opcional) Impressora térmica configurada no Windows.

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
