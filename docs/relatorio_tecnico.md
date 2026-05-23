# Relatório Técnico — InsurMinds VidaBot (Resumo)

**Resumo**

VidaBot é um protótipo de assistente para seguros de vida que combina um frontend web, um backend Flask e um mecanismo RAG que injeta trechos de `faq.txt` em prompts enviados a LLMs (OpenAI / Anthropic / Gemini). O objetivo é fornecer respostas rápidas, rastreáveis e atualizáveis.
---

## Introdução

Protótipo para automatizar respostas a perguntas frequentes sobre seguros de vida (carências, sinistros, beneficiários), com foco em precisão e auditabilidade. Implementação orientada a prova de conceito e fácil manutenção.
---

## Arquitetura

Fluxo: Usuário → Frontend (`frontend/index.html`) → `/api/chat` em `app.py` → RAG (busca em `faq.txt`) → LLM (configurado por `.env`) → Resposta.

Diagrama: `docs/arquitetura_rag.svg`.
---

## RAG (implementação)

Busca simples por keywords em `faq.txt` (não usa embeddings). Processo:
1. Carrega e segmenta `faq.txt` em blocos.
2. Extrai keywords e prévia do texto.
3. Scoring simples por presença de keywords e ocorrência de termos; retorna top-3.
4. Injeta os trechos selecionados no `system` prompt.

Limitação principal: recall e robustez inferiores a buscas semânticas baseadas em embeddings.
---

## Integração com LLMs e prompt

O backend monta um `system` prompt que inclui identidade do bot e o contexto RAG. `gerar_resposta_llm()` seleciona provedor por `LLM_PROVIDER` ou inferência por chave e chama a API apropriada (`openai`, `anthropic` ou `google.genai`).

Controles básicos de conformidade (trechos SUSEP) são fixados no `SYSTEM_PROMPT` e há recomendação de encaminhar casos sensíveis para humano.
---

## Tecnologias

- Python 3.11, Flask, python-dotenv
- SDKs: `openai`, `anthropic`, `google.genai`
- Frontend: HTML/CSS/Vanilla JS

Escolhas priorizam simplicidade, portabilidade entre provedores e facilidade de manutenção.
---

## Limitações e próximos passos

- Substituir busca por keywords por embeddings + Vector DB (ChromaDB/FAISS).
- Adicionar instrumentação/métricas e pipeline de avaliação contínua.
- Implementar caching e políticas de fallback para casos sensíveis.
---

## Conclusão

VidaBot é um protótipo funcional e facilmente configurável para demonstração de RAG aplicado a seguros de vida. Para produção, focar em recuperação semântica, monitoramento e controles de compliance.

**Referências:** `faq.txt`, `app.py`, `docs/arquitetura_rag.svg`.

**Relatório completo:** [docs/relatorio_insurminds_vidabot.pdf](docs/relatorio_insurminds_vidabot.pdf)

