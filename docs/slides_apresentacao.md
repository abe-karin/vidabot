# Slides — Apresentação InsurMinds VidaBot

---

## Slide 1 — Capa

- **Título:** InsurMinds — VidaBot
- **Subtítulo:** Assistente virtual de Seguros de Vida com RAG
- **Equipe / Autor:** InsurMinds (Desafio Acadêmico)
- **Data:** 2026

---

## Slide 2 — Problema de negócio

- Falta de atendimento automatizado especializado em seguros de vida.
- Demandas: respostas rápidas sobre carência, sinistros e documentos; redução de chamadas redundantes; rastreabilidade de informação.
- Objetivo: fornecer respostas precisas e atualizáveis, com referência documental e direcionamento para atendimento humano quando necessário.

---

## Slide 3 — Arquitetura da solução

- Fluxo: Usuário (Frontend) → Backend Flask (`/api/chat`) → RAG (busca em `faq.txt`) → LLM (OpenAI / Anthropic / Gemini) → Resposta.
- Componentes:
  - Frontend: `frontend/index.html` (chat UI)
  - Backend: `app.py` (RAG, orquestração, seleção de provedor)
  - Base de conhecimento: `faq.txt` (chunks com `FONTE:`)
  - Integração LLMs: `OPENAI_API_KEY` / `ANTHROPIC_API_KEY` / `GEMINI_API_KEY`

> Nota: Diagrama disponível em `docs/arquitetura_rag.svg`.

---

## Slide 4 — O que é RAG e como foi implementado

- RAG = Retrieval-Augmented Generation: busca documentos relevantes e injeta contexto no prompt.
- Implementação atual: busca por palavras-chave e scoring simples (top-3 chunks) a partir de `faq.txt`.
- Limitações: não usa embeddings nem vetor DB (próximo passo sugerido: ChromaDB + embeddings).

---

## Slide 5 — Demo (descrição do slide)

- Captura: interface de chat mostrando pergunta do usuário, tags RAG e resposta gerada.
- Passos para demo ao vivo:
  1. Iniciar servidor: `python app.py` (ou `gunicorn app:app`).
  2. Acessar `http://localhost:5000` e enviar pergunta: "Qual a carência do seguro?"
  3. Mostrar painel de chunks e evidências injetadas no prompt.

---

## Slide 6 — Tecnologias utilizadas

- Backend: Python 3.11, Flask, python-dotenv
- Frontend: HTML5/CSS3/Vanilla JS (arquivo `frontend/index.html`)
- IA: OpenAI / Anthropic / Google Gemini (configuráveis via `.env`)
- RAG: `faq.txt` (busca por keywords)

---

## Slide 7 — Resultados e métricas (simuladas)

- Precisão de respostas (simulada): 88% em perguntas factuais cobertas pela base.
- Latência média de resposta: 450 ms (backend + chamada LLM; depende do provedor).
- Taxa de reroute para atendimento humano: ~7% (casos jurídicos/complexos).
- Redução estimada de chamadas ao SAC: 35% para dúvidas frequentes.

---

## Slide 8 — Melhorias futuras e conclusão

- Próximos passos prioritários:
  1. Substituir busca por keywords por embeddings + ChromaDB (maior recall e precisão).
  2. Implementar logs e métricas reais (instrumentação, A/B tests).
  3. Fluxo de fallback seguro para casos sensíveis (ex.: encaminhar para humano com checklist).
- Conclusão: VidaBot prova viabilidade de RAG aplicado a seguros de vida; próximo ciclo foca robustez e métricas reais.
