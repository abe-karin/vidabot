# InsurMinds — VidaBot 🤖

Chatbot de Seguros de Vida que combina LLMs (OpenAI ou Anthropic) com RAG (Retrieval-Augmented Generation) para respostas precisas e atualizáveis.

## 🎯 Sobre o Projeto

VidaBot é um assistente virtual especializado em Seguros de Vida que integra:
- **LLMs (OpenAI / Anthropic / Google Gemini)** para geração de linguagem
- **RAG** para injetar contexto confiável a partir da base de conhecimento
- **Frontend simples** (HTML/JS) para interação via navegador

## 📁 Estrutura do Repositório

```
.
├── app.py                  ← Backend Flask (API + RAG)
├── scripts/
│   └── list_llm_models.py  ← Lista modelos acessíveis pelos provedores
├── requirements.txt        ← Dependências Python
├── faq.txt                 ← Base de conhecimento (RAG)
├── .env.example            ← Template de variáveis de ambiente
├── frontend/
│   └── index.html          ← Interface do chatbot
└── docs/                   ← Diagramas e relatórios
```

## 🚀 Como Rodar Localmente

### 1. Clonar o Repositório
```bash
git clone https://github.com/abe-karin/vidabot.git
cd vidabot
```

### 2. Criar e ativar o ambiente virtual
```bash
python -m venv .venv

# Linux/Mac
source .venv/bin/activate

# Windows (PowerShell)
\.venv\Scripts\Activate.ps1
```

### 3. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 4. Verificar os Modelos Disponíveis

```bash
python scripts/list_llm_models.py
```

O script carrega o `.env`, lista os modelos acessíveis de cada provedor configurado e ignora automaticamente o provedor sem chave.

### 5. Configurar as chaves de API

```bash
# Copiar template
cp .env.example .env

# Editar .env e adicionar sua(s) chave(s)
# Exemplo:
OPENAI_API_KEY=sk-xxxxx
# ou
ANTHROPIC_API_KEY=sk-xxxxx
# e opcionalmente
LLM_PROVIDER=openai  # ou anthropic
```

**Obter chave em:** https://platform.openai.com/api-keys

### 6. Iniciar o Servidor
```bash
python app.py
```

**Acesse:** http://localhost:5000 (por padrão)

## 🔧 Configuração

### Variáveis de Ambiente (.env)

```env
# OpenAI API Key (padrão; não use chaves sk-ant aqui)
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxx
# Anthropic API Key (alternativa)
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxx
# Provedor ativo: openai ou anthropic
LLM_PROVIDER=openai

# Modelos opcionais
OPENAI_MODEL=gpt-3.5-turbo
# Recomendação: prefira `claude-sonnet-4-20250514` quando disponível.
# O `app.py` tentará usar este modelo preferido automaticamente se
# `ANTHROPIC_MODEL` não for definido. Se o modelo preferido não estiver
# acessível, o backend fará fallback para uma versão compatível (por
# exemplo `claude-sonnet-4-6`) e adicionará uma nota técnica curta à
# resposta explicando por que outra versão foi usada.
ANTHROPIC_MODEL=claude-sonnet-4-20250514
# Gemini (opcional)
GEMINI_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxx
GEMINI_MODEL=models/gemini-2.5-flash-lite
```

### Trocar de Provedor ou Modelo

Edite as variáveis de ambiente ou `app.py`:

```env
LLM_PROVIDER=openai
```

Para Anthropic:

```env
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-sua-chave-aqui
ANTHROPIC_MODEL=claude-sonnet-4-6
```

Para Gemini:

```env
LLM_PROVIDER=gemini
GEMINI_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxx
GEMINI_MODEL=models/gemini-2.5-flash-lite
```



## ☁️ Google Gemini — Configuração (conforme `app.py` / `.env.example`)

O projeto suporta Gemini via `GEMINI_API_KEY` (conforme `.env.example`). Configure:

```env
LLM_PROVIDER=gemini
GEMINI_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxx
GEMINI_MODEL=models/gemini-2.5-flash-lite
```

- `GEMINI_API_KEY`: chave usada pelo backend para autenticar o cliente `google.genai`.
- `GEMINI_MODEL`: modelo a ser utilizado (o padrão em `app.py` é `models/gemini-2.5-flash-lite`).
- `LLM_PROVIDER=gemini` força o uso do provedor Gemini; caso contrário o backend tenta inferir o provedor pela presença das chaves.

O `app.py` lê `GEMINI_API_KEY` e `GEMINI_MODEL` e utiliza `google.genai.Client(api_key=...)` para gerar conteúdo quando o provedor for `gemini`.

Exemplo de requisição ao servidor local (a API do VidaBot encaminha para o provedor configurado):

```bash
curl -X POST http://localhost:5000/api/chat \
        -H "Content-Type: application/json" \
        -d '{"mensagem":"Explique resumidamente o que é um seguro de vida."}'
```


Modelos Anthropic confirmados no ambiente atual:

```text
claude-haiku-4-5-20251001
claude-opus-4-1-20250805
claude-opus-4-5-20251101
claude-opus-4-6
claude-opus-4-7
claude-sonnet-4-5-20250929
claude-sonnet-4-6
```

Se `LLM_PROVIDER` não estiver definido, o backend tenta inferir o provedor pela chave disponível. Se `OPENAI_API_KEY` vier com prefixo `sk-ant-`, ele será tratado como configuração incorreta para OpenAI e o backend pedirá que você use `ANTHROPIC_API_KEY` ou defina `LLM_PROVIDER=anthropic`.

Modelos OpenAI:

```python
# GPT-3.5 Turbo (recomendado - mais barato e rápido)
model="gpt-3.5-turbo"

# GPT-4 (melhor qualidade, mais caro)
model="gpt-4"

# GPT-4 Turbo (equilibrado)
model="gpt-4-turbo-preview"
```

Modelos Anthropic:

```python
model="claude-sonnet-4-6"
```

Recomendação: para máxima compatibilidade e qualidade, defina
`ANTHROPIC_MODEL=claude-sonnet-4-20250514` no seu arquivo `.env` quando
disponível. O backend faz verificação e fallback automático; em caso de
uso de uma versão diferente, será incluída uma pequena nota técnica
na resposta retornada pelo VidaBot explicando o motivo.

## 📚 Como Funciona o RAG

### Fluxo de Informação

```
1. Usuário faz pergunta
        ↓
2. Sistema busca em faq.txt
   (scoring por palavras-chave)
        ↓
3. Seleciona top 3 chunks relevantes
        ↓
4. Injeta contexto no prompt
        ↓
5. Envia para o provedor configurado
        ↓
6. LLM gera resposta baseada no contexto
        ↓
7. Retorna resposta personalizada
```

### Exemplo Prático

**Pergunta do usuário:**
```
"Qual a carência do seguro?"
```

**RAG busca em faq.txt:**
```
✓ Encontrado: "carência de 180 dias para morte natural..."
✓ Score: 85 pontos
✓ Fonte: Base de Conhecimento
```

**Contexto injetado no prompt:**
```
===== CONTEXTO RAG =====
[Base de Conhecimento]: A cobertura por morte natural 
entra em vigor após carência de 180 dias a partir da 
contratação. Neste caso, se o segurado falecer por 
qualquer causa não decorrente de acidente...
========================
```

**LLM responde com base no contexto fornecido:**
```
"A cobertura por morte natural do seguro de vida entra 
em vigor após a carência de 180 dias a partir da 
contratação. Neste caso, se o segurado falecer por 
qualquer causa não decorrente de acidente, os 
beneficiários receberão o capital segurado..."
```

### Vantagens do RAG

✅ **Informações Precisas** - Baseadas em documentos reais da empresa  
✅ **Atualizável** - Basta editar faq.txt  
✅ **Rastreável** - Sabe de onde veio cada informação  
✅ **Sem Alucinações** - LLM usa dados fornecidos, não inventa  
✅ **Específico** - Informações da InsurMinds, não genéricas  

## 📝 Personalizar Base de Conhecimento

Edite o arquivo `faq.txt` para adicionar/modificar informações:

```
Pergunta sobre novo produto ou serviço

Resposta detalhada com todas as informações necessárias.
Pode incluir múltiplos parágrafos, listas e detalhes técnicos.

FONTE: Manual de Produtos 2024

---

Próxima pergunta...
```

O sistema automaticamente:
- ✅ Carrega as novas informações ao iniciar
- ✅ Busca quando relevante para a pergunta
- ✅ Injeta no contexto do LLM
- ✅ Gera respostas baseadas no conteúdo
- ✅ Permite consultar quais modelos estão disponíveis via `scripts/list_llm_models.py`

## 🌐 Deploy (Render / Heroku / similar)

Para deploy em plataformas como Render ou Heroku, configure as variáveis de ambiente e use um processo de produção, por exemplo `gunicorn`.

Build / Start examples:

```
pip install -r requirements.txt
gunicorn app:app
```

Configure as environment variables na plataforma: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY` (se usar), `LLM_PROVIDER`.

## 💰 Custos

Os valores de API mudam com frequência — consulte as páginas oficiais antes de calcular orçamento:

- [Preços da API da OpenAI](https://openai.com/api/pricing/)
- [Preços da Anthropic](https://www.anthropic.com/pricing)
- [Preços Gemini / IA Studio (Google)](https://aistudio.google.com/api-keys)

Recomendação: escolha o modelo com melhor custo-desempenho para seu caso e consulte os links acima para tarifas atualizadas.

## 🛠️ Tecnologias

### Backend
- Python 3.11+
- Flask
- python-dotenv

### Frontend
- HTML5, CSS3, JavaScript (Vanilla)

### IA & RAG
- OpenAI / Anthropic / Google (Gemini) (configuráveis via `.env`)
- RAG baseado em `faq.txt`

## 📊 Arquitetura do Sistema

```
┌─────────────┐
│   Usuário   │
└──────┬──────┘
       │ Pergunta
       ↓
┌─────────────────────────────────────┐
│         Frontend (HTML/JS)          │
│  - Interface de chat                │
│  - Envio de mensagens               │
│  - Exibição de respostas            │
└──────────────┬──────────────────────┘
               │ POST /api/chat
               ↓
┌─────────────────────────────────────┐
│       Backend Flask (app.py)        │
│                                     │
│  1. Recebe pergunta                 │
│  2. Busca RAG em faq.txt            │
│  3. Monta contexto                  │
│  4. Chama OpenAI API                │
│  5. Retorna resposta                │
└──────────────┬──────────────────────┘
               │
       ┌───────┴────────┐
       ↓                ↓
┌─────────────┐  ┌─────────────┐
│   faq.txt   │  │  OpenAI API │
│ (Base RAG)  │  │  (GPT-3.5)  │
└─────────────┘  └─────────────┘
```

## 🧪 Testes rápidos

Rodar localmente:

```bash
source .venv/bin/activate
pip install -r requirements.txt
python app.py
# ou para produção local:
# gunicorn app:app
```

Exemplo de requisição à API:

```bash
curl -X POST http://localhost:5000/api/chat \
        -H "Content-Type: application/json" \
        -d '{"mensagem": "Qual a carência do seguro?"}'
```

RAG endpoint (se disponível):

```bash
curl http://localhost:5000/api/rag
```

## 🤝 Contribuindo

1. Faça fork do repositório
2. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
3. Faça commits pequenos e com mensagens claras
4. Abra um Pull Request descrevendo a mudança

## 🆘 Suporte

### Problemas Comuns

**Erro: "Import openai could not be resolved"**
```bash
pip install openai
```

**Erro: "Invalid API key"**
- Verifique se copiou a chave completa
- Confirme que está no arquivo `.env`
- Gere nova chave em: https://platform.openai.com/api-keys

**Erro: "Rate limit exceeded"**
- Aguarde 1 minuto
- Considere fazer upgrade do plano OpenAI

**Erro: "Insufficient quota"**
- Seus créditos acabaram
- Adicione créditos em: https://platform.openai.com/account/billing

### Links Úteis

- **OpenAI Docs:** https://platform.openai.com/docs
- **OpenAI Status:** https://status.openai.com/
- **Flask Docs:** https://flask.palletsprojects.com/
- **Render Docs:** https://render.com/docs

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais (Desafio InsurMinds). Consulte o autor para outros usos.

---

**Desenvolvido para o Desafio InsurMinds 2026** 🚀
