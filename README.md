# Omenortep-AI

Este repositório contém o plano de execução técnica e os recursos para o projeto de **Fine-Tuning e Eficiência On-Premises**, focado na especialização de modelos de linguagem para o domínio técnico de engenharia e petróleo.

## 🎯 Objetivo
Desenvolvimento de um **SLM (Small Language Model)** especializado em jargões técnicos, operando localmente no **Windows** com hardware otimizado, garantindo privacidade e precisão sem dependência de bases externas (RAG).

## 🚀 Tecnologias Utilizadas

### 🤖 IA e Fine-Tuning
- **Modelo Base:** `unsloth/phi-3-mini-4k-instruct-bnb-4bit` (Phi-3-mini).
- **Abstração:** **Unsloth** (Aceleração e eficiência de VRAM).
- **Técnica:** **QLoRA** (Fine-tuning de baixa precisão).
- **Plataforma:** **Google Colab** (Treinamento assistido).

### 🖥️ Deploy e Interface
- **Inferência:** **Ollama** (Servidor de LLM local).
- **Interface:** **Open WebUI** (Gradio-style UI via Docker).
- **Formato:** **GGUF** (Quantização 4-bit balanceada).
- **Orquestração:** **Docker Compose** no Windows.

### 📋 Extração e MLOps
- **OCR:** **Tesseract OCR** ([Download Binários Windows](https://github.com/UB-Mannheim/tesseract/wiki)) ou **Docling**.
- **Linguagem:** **Python 3.10+**.
- **Tracking:** **MLflow** via **DagsHub** (Experiment Tracking).
- **Monitoramento:** **Evidently AI** (Métricas Semânticas e Drift).

### ⚙️ Hardware Target
- **GPU:** NVIDIA GeForce GTX 1650 (4 GB VRAM).
---

## 🛠️ Instalação e Requisitos

### Pré-requisitos
- **NVIDIA GPU:** GTX 1650 (4GB) com drivers atualizados.
- **Docker Desktop:** Instalado no Windows.
- **Python 3.10+**: Com `venv` configurado.
- **Ollama**: [Baixar Executável Windows](https://ollama.com/download/windows).

### Setup Rápido (Local)
1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/RichardMan13/Omenortep-AI.git
    cd Omenortep-AI
    ```
2.  **Variáveis de Ambiente:** Copie o `.env.example` para `.env` e preencha suas credenciais do **DagsHub**.
3.  **Ambiente Virtual:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    pip install -r requirements.txt
    ```
4.  **Interface UI (Open WebUI):**
    ```bash
    docker compose up -d
    ```
5.  **Acesse:** [http://localhost:3000](http://localhost:3000)

---

## ⚙️ Configuração do Ambiente (.env)

Para garantir o rastreamento das métricas no DagsHub e a correta execução dos scripts, crie um arquivo `.env` na raiz do projeto (baseado no `.env.example`):

```bash
# MLflow / DagsHub Credentials
MLFLOW_TRACKING_URI=https://dagshub.com/RichardMan13/Omenortep-AI.mlflow
MLFLOW_TRACKING_USERNAME=RichardMan13
MLFLOW_TRACKING_PASSWORD=seu_token_aqui
```

---

## 🛠️ Plano de Execução Técnica

### Fase 1: Curadoria e Preparação do Dataset
O sucesso de um modelo especializado depende da qualidade dos dados e da abrangência da extração.

*   **Fontes de Dados:** Manuais, normas e publicações técnicas via [Hub de Conhecimento IBP](https://www.ibp.org.br/hub-de-conhecimento/publicacoes/).
*   **Extração de Dados:** 
    *   Uso de bibliotecas de web scraping.
    *   **Pipeline de OCR:** Processamento de PDFs técnicos e manuais antigos (digitalizações) para conversão em texto puro.
*   **Estruturação (JSONL):** O dataset seguirá o padrão Alpaca/ShareGPT para instruções técnicas.
*   **Data Augmentation:** Modelos robustos (GPT-4o/Claude) gerarão variações de perguntas sobre os textos puros para maior diversidade.

### Fase 2: Fine-Tuning com Unsloth (Google Colab)
O **Unsloth** será usado para acelerar o treino e garantir compatibilidade com o hardware final.

*   **Configuração do Ambiente:**
    *   **Hardware de Treino:** T4 GPU (Google Colab).
    *   **Modelo Base:** `unsloth/phi-3-mini-4k-instruct-bnb-4bit` (escolhido por sua altíssima eficiência em 4-bits).
*   **Processo de Treino (LoRA/QLoRA):**
    *   `max_seq_length`: 2048.
    *   `lora_alpha`: 16.
    *   `learning_rate`: 2e-4.

### Fase 3: Exportação e Quantização GGUF
*   **Fusão de Pesos:** Geração direta do formato GGUF via Unsloth.
*   **Quantização (Q4_K_M):** Otimizada para rodar em GPUs com VRAM limitada.
*   **Persistência:** O arquivo `.gguf` será a base para a execução local.

### Fase 4: Deploy Local no Windows
O modelo sairá da nuvem para o hardware do usuário no ambiente **Windows**.

*   **Hardware de Destino:** **NVIDIA GeForce GTX 1650 (4 GB VRAM)**.
*   **Ollama Modelfile:**
    ```dockerfile
    FROM ./model_omenortep_ai-q4_k_m.gguf
    PARAMETER temperature 0.2
    # Economia de VRAM agressiva (GTX 1650 4GB)
    PARAMETER num_ctx 2048
    # Prompt Engineering de Sistema
    SYSTEM "Você é um Engenheiro Sênior de Perfuração experiente. Responda de forma técnica, precisa e profissional, utilizando o jargão específico da indústria de petróleo e gás."
    ```
*   **Orquestração:** Ollama nativo ou via Docker no Windows, com interface **Open WebUI**.

### Fase 5: Avaliação e Refinamento
Validação rigorosa para garantir a utilidade real do modelo.

*   **Golden Dataset:** Criação de um conjunto de teste com "respostas perfeitas" revisadas por especialistas.
*   **Métricas de Qualidade:** Uso de **ROUGE** e **BERTScore** para medir a aderência do modelo às respostas do Golden Dataset.

### Fase 6: Governança e MLOps (MLflow & Evidently)
Implementação de rastreamento e monitoramento profissional com foco em automação.

*   **MLflow (Experiment Tracking & Artefatos):**
    *   **Infraestrutura:** Uso do **DagsHub** para tracking remoto e armazenamento centralizado do arquivo `.gguf`.
    *   **Padronização:** Nomenclatura no formato `vX.X-Phi3-Contexto` (ex: `v1.0-Phi3-Basic`).
    *   **Logs:** Registro completo de hiperparâmetros, curvas de treino e métricas de perda.
*   **Evidently AI (Monitoramento de Qualidade):**
    *   **Métricas Ativas:** ROUGE, BERTScore, **Similarity Score** e **Length Drift**.
    *   **Relatórios:** Geração automática de relatórios HTML após cada ciclo de **50 novas interações** de teste ou uso real.
*   **Gestão de Feedback & Trigger:**
    *   **Pasta `/feedback`:** Repositório local para logs de erro e correções enviadas por usuários.
    *   **Trigger de Retreinamento:** Parametrizado para disparar um novo ciclo de Fine-Tuning caso o **Similarity Score** médio caia abaixo de **0.82** (ajustável).

| Métrica | Local (Omenortep-AI) | API Paga (GPT-4o) |
| :--- | :--- | :--- |
| **Infra** | GTX 1650 (4GB) / Windows | Nuvem Robusta |
| **Governance** | MLflow (DagsHub) + Evidently | Proprietária/Nula |
| **Monitoramento** | Similarity & Length Drift | Nula (Feedback Manual) |
| **Latência** | ~20-30 t/s (Estimado) | Variável |
| **Custo (1M tokens)** | $0.00 (Energia Local) | ~$5.00 - $15.00 |

---

## 📜 Padrões de Desenvolvimento (Governança)

Como definido no `GEMINI.md`, todo desenvolvimento deve seguir:

1.  **Type Hinting:** Todo código Python deve vir com tipagem estrita (`from typing import ...`).
2.  **Linguagem:**
    *   **Explicações/Comentários:** Português (BR).
    *   **Código/Variáveis:** Inglês Técnico.
3.  **Estética:** Proibição de emojis em variáveis, logs técnicos ou comentários.
4.  **Tracking:** Treinamentos via Colab/Local devem usar `mlflow.start_run()`.

---

## ✅ Checklist de Execução

### 1. Preparação (Fase 1)
- [x] Criar estrutura de pastas (`/data`, `/scripts`, `/models`, `/knowledge`, `/feedback`).
- [x] Mapear diretórios de manuais técnicos (PDFs) para `/data/raw`.
- [x] Implementar script de extração com suporte a OCR em `/scripts/ocr_extract.py`.
- [x] Estruturar o dataset inicial em `/data/processed/processed_knowledge.jsonl`.
- [x] Geração Sintética (Data Augmentation) para preencher o campo `output` (100 pairs via GPT-4o).
- [x] Separar dataset de treino (80) e benchmark (20) em `/data/processed/training_data.jsonl`.

### 2. Fine-Tuning & Tracking (Fase 2, 3 & 6)
- [x] Configurar conta no **DagsHub** e obter as credenciais do MLflow.
- [ ] Configurar ambiente no Google Colab com Unsloth e MLflow.
- [ ] Realizar o treinamento com a nomenclatura `v1.0-Phi3-Basic`.
- [ ] Exportar arquivo `.gguf` para o MLflow Artifacts no DagsHub.

### 3. Validação & Monitoramento (Fase 5 & 6)
- [x] Criar o **Golden Dataset** em `/knowledge/golden_dataset.json` (20 pares técnicos).
- [ ] Gerar relatório do **Evidently AI** comparando Baseline vs. Golden Dataset.
- [ ] Validar métricas de **Similarity Score** e **Length Drift**.

### 4. Deploy (Fase 4)
- [ ] Instalar Ollama no Windows (Nativo ou Docker).
- [ ] Configurar o `Modelfile` com o System Prompt do Engenheiro Sênior.
- [ ] Integrar a coleta de logs da interface à pasta `/feedback/logs`.

### 5. Operação
- [ ] Monitorar uso de VRAM na GTX 1650 (alvo: < 3.5GB).
- [ ] Executar script de relatório HTML a cada 50 novas perguntas.
- [ ] Verificar gatilho de retreinamento (Trigger < 0.82 Similarity).

---